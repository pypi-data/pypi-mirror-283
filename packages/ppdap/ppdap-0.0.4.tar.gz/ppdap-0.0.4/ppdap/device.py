"""Define the DigoDevice class."""
import asyncio
from collections.abc import Callable
import json
import logging
from typing import Any

from .attribute import DigoAttribute
from .connection import DigoConnection
from .const import MQTT_CONNECTED, NOTIFY_MSG_SCHDED_01, NOTIFY_TITLE_DI
from .mqttc import ReceiveMessage
from .schedule import DigoSchedule
from .storage import DigoStore
from .utils import callback, generate_transcode, get_timestamp
from .setup import DigoDeviceSetup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DigoDevice:
    """Represents a DigoDevice object for communication with a Digo device."""

    def __init__(
        self,
        model: str,
        firmware: int,
        hardware: int,
        mac: str,
        bid: str,
        uuid: str,
        profile_id: int,
        owner: str,
        tenant_id: str,
        loop: asyncio.AbstractEventLoop,
        path: str,
        connection: DigoConnection | None = None,
        super_id: str | None = None,
        mqtt_host: str | None = None,
        mqtt_port: int | None = None,
        http_host: str | None = None,
        http_port: int | None = None,
        token: str | None = None,
    ) -> None:
        """Initialize the DigoDevice class.

        Args:
            model (str): The model of the device.
            firmware (int): The firmware version of the device.
            hardware (int): The hardware version of the device.
            mac (str): The MAC address of the device.
            mqtt_host (str): The MQTT host for communication.
            mqtt_port (int): The MQTT port for communication.
            http_host (str): The HTTP host for communication.
            http_port (int): The HTTP port for communication.
            bid (str): The box ID of the device.
            uuid (str): The UUID of the device.
            profile_id (int): The profile ID of the device.
            owner (str): The owner of the device.
            tenant_id (str): The tenant ID of the device.
            super_id (str, optional): The ID of the super device. Defaults to None.
            token (str): The token for authentication.
            connection (DigoConnection | None, optional): The connection object for communication. Defaults to None.
            loop (asyncio.AbstractEventLoop | None, optional): The event loop for asynchronous operations. Defaults to None.
        """
        if not bid:
            if not mac:
                raise ValueError("MAC or BID must be provided")
            else:
                bid = mac.replace(":", "")
        if not path:
            path = ""
        self._loop = loop
        self._uuid = uuid
        self._bid = bid
        self._mac = mac
        self._model = model
        self._firmware: int = int(firmware)
        self._hardware: int = int(hardware)
        self._profile_id = profile_id
        self._owner = owner
        self._tenant_id = tenant_id
        self._super_id = super_id
        if token and connection is None:
            self.connection = DigoConnection(
                loop,
                mqtt_host,
                mqtt_port,
                http_host,
                http_port,
                tenant_id,
                f"DEV#$#{uuid}#$#{bid}",
                token,
            )
        else:
            self.connection = connection
        self._services: list[str] = []
        self._settings: list[str] = []
        self._schedule = DigoSchedule()
        self._store = DigoStore(f"{path}/{bid}.json")
        self._common_services: list[DigoAttribute] = []
        self._setting_services: list[DigoAttribute] = []
        self._timer: asyncio.TimerHandle | None = None
        self._unsub: Callable | None = None
        self._setup: DigoDeviceSetup = None
        self._tc: str = None

    async def start(self):
        """Start the device."""
        if self.connection is None:
            self._store.load()
            if self._store.data:
                self._create_connection()
        if self.connection is None:
            self._setup = DigoDeviceSetup(self)
            await self._setup.start_server()
        elif self._super_id is None:
            if self.connection.connected is False:
                await self.connection.async_start()
            self._unsub = await self.connection.async_subscribe(
                self.get_command_topic(), self._mqtt_handle_message
            )
            self.connection.connect_signal(MQTT_CONNECTED, self._on_mqtt_connect)
        if self._timer:
            self._timer.cancel()
            self._timer = self._loop.call_later(1, self._schedule_handle)
        
    async def stop(self):
        """Stop the device."""
        if self._setup:
            await self._setup.stop_server()
        elif self._super_id is None and self.connection is not None:
            if self._unsub:
                self._unsub()
                self._unsub = None
            if self.connection.connected is True:
                await self.connection.async_stop()
            self.connection.disconnect_signal(MQTT_CONNECTED, self._on_mqtt_connect)
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def setup_data(self, data: dict):
        """Setup the data."""
        self._store.data["setup"] = data
        self._loop.create_task(self.async_setup_data())

    async def async_setup_data(self):
        """Setup the data asynchronously."""
        await self._loop.run_in_executor(None, self._store.save)
        self._create_connection()
        if self.connection is not None:
            await self.connection.async_start()
            self._unsub = await self.connection.async_subscribe(
                self.get_command_topic(), self._mqtt_handle_message
            )
            self.connection.connect_signal(MQTT_CONNECTED, self._on_mqtt_connect)

    @property
    def bid(self) -> str:
        """Return the box ID."""
        return self._bid

    @property
    def uuid(self) -> str:
        """Return the UUID."""
        return self._uuid

    @property
    def model(self) -> str:
        """Return the model."""
        return self._model

    @property
    def firmware(self) -> int:
        """Return the firmware version."""
        return self._firmware

    @property
    def hardware(self) -> int:
        """Return the hardware version."""
        return self._hardware

    @property
    def mac(self) -> str:
        """Return the MAC address."""
        return self._mac

    @property
    def is_sub(self) -> bool:
        """Return if the device is a sub device."""
        return True if self._super_id else False

    def get_state_topic(self):
        """Get the state topic."""
        if self._super_id:
            return f"v1/iot/devices/{self._super_id}/response"
        else:
            return f"v1/iot/devices/{self._uuid}/response"

    def get_command_topic(self):
        """Get the command topic."""
        if self._super_id:
            return f"v1/iot/devices/{self._super_id}/request"
        else:
            return f"v1/iot/devices/{self._uuid}/request"

    def get_upload_path(self):
        """Get the upload path."""
        return "/gw/device-common-service/api/v1/device/upload"

    def get_notify_path(self):
        """Get the notify path."""
        return "/gw/device-common-service/api/v1/device/notify"

    def get_update_path(self):
        """Get the update path."""
        return "/gw/ota-service/api/v1/device/ota/check-update"

    def add_common_service(self, attribute: DigoAttribute):
        """Add attributes."""
        if attribute.vtype == dict:
            for child in attribute.children:
                child.update_callback = self._update_common_service
                self._common_services.append(child)
        else:
            self._common_services.append(attribute)
        attribute.update_callback = self._update_common_service

    def add_setting_service(self, attribute: DigoAttribute):
        """Add setting attributes."""
        if attribute.vtype == dict:
            raise ValueError("Setting attribute cannot be dict type.")
        attribute.update_callback = self._update_setting_service
        self._setting_services.append(attribute)

    def _get_common_service(self, key: str) -> DigoAttribute | None:
        """Get the attributes."""
        for attr in self._common_services:
            if attr.key == key:
                return attr
        return None

    def _get_setting_service(self, key: str) -> DigoAttribute | None:
        """Get the attributes."""
        for attr in self._setting_services:
            if attr.key == key:
                return attr
        return None

    def _update_common_service(self, value: dict) -> None:
        """Update the attributes."""
        self._loop.create_task(
            self._mqtt_publish("command", generate_transcode(), value)
        )

    def _update_setting_service(self, value: dict) -> None:
        """Update the setting attributes."""
        self._loop.create_task(
            self._mqtt_publish("command", generate_transcode(), {"settings": value})
        )

    def mqtt_publish(self, method: str, tc: str = None, value: dict = None) -> None:
        """Publish data to MQTT."""
        if tc is None:
            tc = generate_transcode()
        self._loop.create_task(self._mqtt_publish(method, tc, value))

    def reboot_device(self):
        """Reboot the device."""
        raise NotImplementedError()

    def reset_device(self):
        """Reset the device."""
        raise NotImplementedError()

    @callback
    def async_mqtt_handle_message(self, jmsg: dict) -> None:
        """Handle the message."""
        if "method" in jmsg and "tc" in jmsg:
            method = jmsg["method"]
            self._tc = jmsg["tc"]
            user = self._tc.split("$")[0]

            if method == "get_status":
                self._loop.create_task(self._report_status())
            elif method == "get_extend_status":
                self._loop.create_task(self._report_ex_status())
            elif method == "command":
                if "settings" in jmsg["values"]:
                    self._setting_command(jmsg["values"]["settings"], user)
                else:
                    self._service_command(jmsg["values"], user)
            elif method == "get_schedule":
                ret = self._schedule.get_schedules()
                self._loop.call_soon(self._mqtt_publish, "get_schedule", self._tc, ret)
            elif method == "add_schedule":
                ret = self._schedule.add_schedules(jmsg["values"]["schedules"])
                self._loop.call_soon(self._mqtt_publish, "add_schedule", self._tc)
            elif method == "edit_schedule":
                ret = self._schedule.edit_schedules(jmsg["values"]["schedules"])
                self._loop.call_soon(self._mqtt_publish, "edit_schedule", self._tc)
            elif method == "del_schedule":
                ret = self._schedule.delete_schedules(jmsg["values"]["schedules"])
                self._loop.call_soon(self._mqtt_publish, "del_schedule", self._tc)
            elif method == "reboot":
                self.reboot_device()
            elif method == "reset":
                self.reset_device()
            else:
                logger.debug("Unknown method: %s", method)

    def _service_command(self, services: dict, user: str):
        """Handle service command."""
        keys = list(services.keys())
        for key in keys:
            if not services:
                break
            if (value := services[key]) is not None:
                if attr := self._get_common_service(key):
                    if attr.parent:
                        attr.import_value(services, user)
                    else:
                        attr.import_value(value, user)
        # for key, value in services.items():
        #     if attr := self._get_common_service(key):
        #         attr.import_value(value, user)

    def _setting_command(self, settings: dict, user: str):
        """Handle setting command."""
        for key, value in settings.items():
            if attr := self._get_setting_service(key):
                attr.import_value(value, user)

    @callback
    def _on_mqtt_connect(self):
        """Handle MQTT connect."""
        if self._setup:
            self._loop.create_task(self._setup.stop_server())
        self._loop.create_task(self._report_status())
        self._loop.create_task(self._report_ex_status())

    @callback
    def _schedule_handle(self):
        """Process schedule event."""
        self._timer = self._loop.call_later(60, self._schedule_handle)

        ret = self._schedule.check()
        for item in ret:
            logger.info("Device %s schedule: %s", self._uuid, item)
            self._service_command(item["target"])
            if item["notify"]:
                self._loop.create_task(
                    self._http_post(
                        self.get_notify_path(),
                        generate_transcode(),
                        "notify",
                        {
                            "title": NOTIFY_TITLE_DI,
                            "code": NOTIFY_MSG_SCHDED_01,
                            "value": 0,
                        },
                    )
                )

    def _mqtt_handle_message(self, msg: ReceiveMessage) -> None:
        """Handle MQTT message."""
        try:
            jmsg = json.loads(msg.payload)
        except json.JSONDecodeError:
            logger.info("Mqtt payload is not valid JSON")
        else:
            self._loop.call_soon_threadsafe(self.async_mqtt_handle_message, jmsg)

    async def _report_status(self):
        """Get the status."""
        values: dict = {}
        if not self._tc:
            self._tc = generate_transcode()
        for attr in self._common_services:
            values.update(attr.export_value())
        await self._mqtt_publish("status", self._tc, values)

    def _get_ssid(self) -> str:
        """Get the SSID.

        Overridden by DigoDevice types.
        """
        return ""

    def _get_ip(self) -> str:
        """Get the IP address.

        Overridden by DigoDevice types.
        """
        return ""

    def _get_signal(self) -> int:
        """Get the signal.

        Overridden by DigoDevice types.
        """
        return -1

    async def _report_ex_status(self):
        """Get the extended status."""
        value = {
            "fw": self._firmware,
            "hw": self._hardware,
            "pid": f"{self._model}.{self._bid}",
            "signal": self._get_signal(),
            "rst": None,
            "ip": self._get_ip(),
            "ssid": self._get_ssid(),
            "mac": self._mac,
        }

        settings: dict = {}
        if not self._tc:
            self._tc = generate_transcode()
        for attr in self._setting_services:
            settings.update(attr.export_value())
        if settings:
            value["settings"] = settings

        task1 = self._mqtt_publish("extend_status", self._tc, value)
        task2 = self._http_post(
            self.get_upload_path(), self._tc, "extend_status", value
        )
        await asyncio.gather(task1, task2)

    def _info(self) -> dict:
        """Get the information about the device."""
        return {
            "tenant_id": self._tenant_id,
            "device_id": self._uuid,
            "device_profile_id": self._profile_id,
            "device_owner": self._owner,
            "box_id": self._bid,
        }

    async def _mqtt_publish(self, method: str, tc: str, value: dict = None) -> None:
        """Publish data to MQTT."""
        data = {
            "ts": get_timestamp(),
            "tc": tc,
            "info": self._info(),
            "method": method,
            "success": True,
        }
        if value is not None:
            data["values"] = value
        await self.connection.async_publish(self.get_state_topic(), json.dumps(data))

    async def _http_post(
        self, path: str, tc: str, method: str, value: dict = None
    ) -> dict:
        """Post data to Digo."""
        data = {
            "ts": get_timestamp(),
            "tc": tc,
            "info": self._info(),
            "method": method,
            "success": True,
        }
        if value is not None:
            data["values"] = value
        return await self._loop.run_in_executor(None, self.connection.post, path, data)
    
    def _create_connection(self):
        """Create the connection."""
        sdata: dict[str, Any] = self._store.data.get("setup", {})
        info: dict = sdata.get("info") if sdata else None
        logger.debug("Device setup data: %s", sdata)
        if info:
            mqtt_host = sdata.get("host")
            mqtt_port = sdata.get("port")
            http_host = sdata.get("host_http")
            http_port = sdata.get("port_http")
            token = info.get("token")
            self._tenant_id = info.get("tenant_id")
            self._uuid = info.get("device_id")
            self._profile_id = info.get("device_profile_id")
            self._owner = info.get("owner")
            self.connection = DigoConnection(
                self._loop,
                mqtt_host,
                mqtt_port,
                http_host,
                http_port,
                self._tenant_id,
                f"DEV#$#{self.uuid}#$#{self._bid}",
                token,
            )
        else:
            logger.error("Device setup data missing")
