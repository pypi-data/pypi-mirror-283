"Digo Device Setuup"

from __future__ import annotations

import asyncio
import logging
import os
from aiohttp import web
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import DigoDevice

logger = logging.getLogger(__name__)

class DigoDeviceSetup:
    def __init__(self, device: "DigoDevice") -> None:
        self._device = device
        self._runner = None
        self._site = None

    async def handle_info(self, request):
        response = {
            "id": self._device.bid,
            "model": self._device.model,
            "firmware": self._device.firmware,
            "hardware": self._device.hardware,
            "mac": self._device.mac,
        }
        return web.json_response(response)

    async def handle_setup(self, request):
        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"status": False, "message": "Invalid JSON"}, status=400)
        from .device import DigoDevice
        self._device.setup_data(data)
        return web.json_response({"status": True, "message": "Success", "error_code": 0})

    async def start_server(self):
        app = web.Application()
        app.router.add_get('/api/info', self.handle_info)
        app.router.add_post('/api/setup', self.handle_setup)
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, "0.0.0.0", 1901)
        await self._site.start()

    async def stop_server(self):
        if self._site:
            await self._site.stop()
            await self._runner.cleanup()