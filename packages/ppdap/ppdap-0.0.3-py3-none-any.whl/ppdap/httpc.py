"Digo Http Client."
import logging

import requests

from .const import HTTP_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class DigoHttpClient:
    """Class representing DigoHttpClient."""

    def __init__(
        self,
        host: str,
        port: int,
        tenant_id: str,
        token: str,
    ) -> None:
        """Initialize the DigoHttpClient class."""
        self._http_host = host
        self._http_port = port
        self._tenant = tenant_id
        self._token = token

    @property
    def http_host(self) -> str:
        """Return the host."""
        return self._http_host

    @property
    def http_port(self) -> int:
        """Return the port."""
        return self._http_port

    def post(self, path: str, data: dict) -> dict:
        """Post data to Digo."""
        if self._http_port == -1:
            url = f"https://{self._http_host}{path}"
        else:
            url = f"http://{self._http_host}:{self._http_port}{path}"
        headers = {
            "Identifier": self._tenant,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        _LOGGER.debug("Post to %s: %s", url, data)
        response = requests.post(url, json=data, headers=headers, timeout=HTTP_TIMEOUT)
        return response.json() if response.status_code == 200 else None

    def get(self, path: str, param: dict = None) -> dict:
        """Get data from Digo."""
        if self._http_port == -1:
            url = f"https://{self._http_host}{path}"
        else:
            url = f"http://{self._http_host}:{self._http_port}{path}"
        headers = {
            "Identifier": self._tenant,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        response = requests.get(
            url, params=param, headers=headers, timeout=HTTP_TIMEOUT
        )
        return response.json() if response.status_code == 200 else None
