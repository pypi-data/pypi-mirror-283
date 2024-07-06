"Digo Connections."

import asyncio
from collections.abc import Callable
import logging
from typing import Any

from .const import MQTT_CONNECTED, MQTT_DISCONNECTED
from .httpc import DigoHttpClient
from .mqttc import DigoMqttClient
from .utils import callback

_LOGGER = logging.getLogger(__name__)


class DigoConnection(DigoHttpClient, DigoMqttClient):
    """Class representing DigoConnection."""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        mqtt_host: str,
        mqtt_port: int,
        http_host: str,
        http_port: int,
        tenant_id: str,
        client_id: str,
        token: str,
    ) -> None:
        """Initialize the DigoConnection class."""
        DigoHttpClient.__init__(self, http_host, http_port, tenant_id, token)
        DigoMqttClient.__init__(
            self,
            loop,
            mqtt_host,
            mqtt_port,
            client_id,
            tenant_id,
            token,
            False,
        )
        self._loop = loop
        self._task: asyncio.Future = None
        self._signals: dict[str, Any] = {}

    async def async_start(self) -> None:
        """Connect to the Digo server asynchronously."""
        if self.connected:
            _LOGGER.debug("Already connected to Digo")
        elif self._task is not None:
            _LOGGER.debug("Connection task already running")
        else:
            self._task = self.async_connect()
            await self._task
            self._task = None

    async def async_stop(self) -> None:
        """Disconnect from the Digo server asynchronously."""
        if not self.connected:
            _LOGGER.debug("Already disconnected from Digo")
        elif self._task is not None:
            _LOGGER.debug("Disconnection task already running")
        else:
            self._task = self.async_disconnect()
            await self._task
            self._task = None

    def connect_signal(self, signal: str, job: Callable[[], None]) -> None:
        """Connect a signal to a callback."""
        if signal not in self._signals:
            self._signals[signal] = {}
        self._signals[signal][job] = None

    def disconnect_signal(self, signal: str, job: Callable[[], None]) -> None:
        """Disconnect a signal from a callback."""
        if signal in self._signals and job in self._signals[signal]:
            del self._signals[signal][job]

    @callback
    def send_signal(self, signal: str, *args: Any) -> None:
        """Send a signal to all connected callbacks."""
        if signal in self._signals:
            for job in self._signals[signal]:
                job(*args)

    def mqtt_on_connected(self) -> None:
        """Call when connected to MQTT.

        This method is called from the MQTT thread.
        """
        self.loop.call_soon_threadsafe(self.send_signal, MQTT_CONNECTED)

    def mqtt_on_disconnected(self) -> None:
        """Call when disconnected from MQTT.

        This method is called from the MQTT thread.
        """
        self.loop.call_soon_threadsafe(self.send_signal, MQTT_DISCONNECTED)
