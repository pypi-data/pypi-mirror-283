"Digo Device Setup."

from __future__ import annotations

import json
import logging
import socket
from typing import TYPE_CHECKING

from aiohttp import web

from .const import SETUP_PORT_DEFAULT, SETUP_PORT_MAX

if TYPE_CHECKING:
    from .device import DigoDevice

logger = logging.getLogger(__name__)


class DigoDeviceSetup:
    """Class representing the setup for DigoDevice."""

    def __init__(self, device: DigoDevice) -> None:
        """Initialize the DigoDeviceSetup class."""
        self._device = device
        self._runner = None
        self._site = None

    async def handle_info(self, request):
        """Handle the info request."""
        response = {
            "id": self._device.bid,
            "model": self._device.model,
            "firmware": self._device.firmware,
            "hardware": self._device.hardware,
            "mac": self._device.mac,
        }
        return web.json_response(response)

    async def handle_setup(self, request):
        """Handle the setup request."""
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response(
                {"status": False, "message": "Invalid JSON"}, status=400
            )

        # from .device import DigoDevice  # noqa: F401

        self._device.setup_data(data)
        return web.json_response(
            {"status": True, "message": "Success", "error_code": 0}
        )

    async def start_server(self):
        """Start the server."""
        app = web.Application()
        port = self._find_aviable_port()
        app.router.add_get("/api/info", self.handle_info)
        app.router.add_post("/api/setup", self.handle_setup)
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, "0.0.0.0", port)
        await self._site.start()
        qr = f"""{{"host":"host_ip:{port}","model":"{self._device.model}"}}"""
        logger.info(
            "Please generate QR code: %s\r\nAnd using QR scan on the Digo App to add accessories",
            qr,
        )

    async def stop_server(self):
        """Stop the server."""
        if self._site:
            await self._site.stop()
            await self._runner.cleanup()

    def _find_aviable_port(self) -> int:
        """Find an available port."""
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.setblocking(False)
        test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        for port in range(SETUP_PORT_DEFAULT, SETUP_PORT_MAX + 1):
            try:
                test_socket.bind(("", port))
                return port
            except OSError:
                if port == SETUP_PORT_MAX:
                    raise
                continue
        raise RuntimeError("unreachable")
