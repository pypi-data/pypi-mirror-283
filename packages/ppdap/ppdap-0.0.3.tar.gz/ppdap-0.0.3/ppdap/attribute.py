"""Define the Digo Attribute class."""

from collections.abc import Callable
import logging
from typing import Any, Optional, cast

logger = logging.getLogger(__name__)


class DigoAttribute:
    """Define the Digo Attribute class."""

    TYPE_BOOLEAN = "boolean"
    TYPE_INETGER = "int"
    TYPE_DOUBLE = "double"
    TYPE_STRING = "string"
    TYPE_DICT = "dict"
    TYPE_SUPPORTED = [TYPE_BOOLEAN, TYPE_INETGER, TYPE_DOUBLE, TYPE_STRING, TYPE_DICT]

    def __init__(
        self,
        key: str,
        value_type: str,
        value: Any,
        setter_callback: Callable[[str, Any, Any], None],
    ) -> None:
        """Initialize the Digo Attribute class."""
        value_type = value_type.lower()
        if value_type == self.TYPE_BOOLEAN:
            self._vtype = bool
        elif value_type == self.TYPE_INETGER:
            self._vtype = int
        elif value_type == self.TYPE_DOUBLE:
            self._vtype = float
        elif value_type == self.TYPE_STRING:
            self._vtype = str
        elif value_type == self.TYPE_DICT:
            self._vtype = dict
        else:
            self._vtype = str
            logger.warning("Value type must be %s.", self.TYPE_SUPPORTED)

        self._key = key
        self.value = value
        self.setter_callback = setter_callback
        self.children: list["DigoAttribute"] = []
        self.parent: Optional["DigoAttribute"] = None
        self.update_callback: Callable[[dict], None] = None

    @property
    def key(self) -> str:
        """Return the key."""
        return self._key

    @property
    def value(self) -> Any:
        """Return the value."""
        return self._value

    @property
    def vtype(self):
        """Return the value type."""
        return self._vtype

    @value.setter
    def value(self, value: Any) -> None:
        """Set the value but not update to cloud."""
        if not isinstance(value, self._vtype):
            if self._vtype == bool:
                value = True if value == "on" else False
            elif self._vtype in [int, float, str]:
                if value is not None:
                    value = self._vtype(value)
                else:
                    value = self._vtype()
            elif not isinstance(value, dict):
                value = {}
        self._value = value

    def add_attr(self, attribute: "DigoAttribute") -> None:
        """Add a child attribute."""
        if self.vtype == dict:
            attribute.parent = self
            self.children.append(attribute)
        else:
            logger.error("Attribute %s is not a dict type.", self.key)

    def export_value(self) -> dict:
        """Export the value."""
        return {self.key: self.value}

    def import_value(self, value: Any, user: str) -> None:
        """Update the value from cloud and call the callback."""
        if self.parent:
            value_dict = cast(dict, value)
            value_change = {}
            for child in self.parent.children:
                if child.key in value_dict:
                    child.value = value_dict.pop(child.key)
                    value_change[child.key] = child.value
            if self.parent.setter_callback:
                self.parent.setter_callback(self.parent.key, value_change, user)
        else:
            self._value = value
            if self.setter_callback:
                self.setter_callback(self.key, self.value, user)

    def set_value(self, value: Any) -> None:
        """Set the value and update to cloud."""
        if self.vtype == dict:
            value_dict = cast(dict, value)
            value_change = {}
            for child in self.children:
                if child.key in value_dict:
                    child.value = value_dict[child.key]
                    value_change[child.key] = child.value
            if self.update_callback:
                self.update_callback(value_change)
        else:
            self.value = value
            if self.update_callback:
                self.update_callback({self.key: self.value})
