"""Define the Digo Storage class."""

import json
import logging
import os
from typing import Any

from atomicwrites import AtomicWriter

from .utils import callback

_LOGGER = logging.getLogger(__name__)


class DigoStore:
    """Define the Digo Storage class."""

    def __init__(self, path: str = None) -> None:
        """Initialize the Digo Storage class."""
        self.data: dict[str, Any] = {}
        self._path = path

    def load(self) -> dict[str, Any]:
        """Load the storage."""
        self._read()
        return self.data

    def save(self) -> None:
        """Save the storage."""
        self._write()

    async def async_load(self) -> dict[str, Any]:
        """Load the storage."""
        _LOGGER.debug("Load data: %s", self.data)
        return self.data

    async def async_save(self) -> None:
        """Save the storage."""
        _LOGGER.debug("Save data: %s", self.data)

    async def async_remove(self) -> None:
        """Remove the storage."""
        self.data = {}
        _LOGGER.debug("Remove data")

    @callback
    def async_save_delay(self, delay: float = 0) -> None:
        """Save the storage with delay."""
        _LOGGER.debug("Save delay (%s): %s", delay, self.data)

    def _write(self) -> None:
        """Write data to the storage."""
        contents = json.dumps(self.data)
        _LOGGER.debug("Write data: %s", contents)
        try:
            with AtomicWriter(self._path, overwrite=True).open() as fdesc:
                if hasattr(os, "fchmod"):
                    os.fchmod(fdesc.fileno(), 0o644)
                fdesc.write(contents)
        except OSError as error:
            _LOGGER.exception("Saving file failed: %s", self._path)
            raise ValueError(error) from error

    def _read(self) -> None:
        """Read data from the storage."""
        try:
            with open(self._path, encoding="utf-8") as fdesc:
                self.data = json.load(fdesc)
        except OSError:
            _LOGGER.warning("Reading file failed: %s", self._path)
