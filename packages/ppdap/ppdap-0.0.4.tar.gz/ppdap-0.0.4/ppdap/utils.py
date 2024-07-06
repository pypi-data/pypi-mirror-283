"""Utility functions for the Digo Accessory Protocol component."""
import datetime as dt
import secrets

DEFAULT_TIME_ZONE: dt.tzinfo = dt.timezone.utc  # noqa: UP017


def callback(func):
    """Decorate a function to make it non-blocking."""
    setattr(func, "_dap_callback", True)
    return func


def set_default_time_zone(time_zone: dt.tzinfo) -> None:
    """Set a default time zone to be used when none is specified.

    Async friendly.
    """
    # pylint: disable-next=global-statement
    global DEFAULT_TIME_ZONE  # noqa: PLW0603

    assert isinstance(time_zone, dt.tzinfo)

    DEFAULT_TIME_ZONE = time_zone


def get_timestamp(time_zone: dt.tzinfo | None = None) -> int:
    """Return the current timestamp from 01/01/2000."""
    return int(dt.datetime.now(time_zone or DEFAULT_TIME_ZONE).timestamp() - 946684800)


def generate_transcode() -> str:
    """Generate a transcode."""
    return secrets.token_hex(16)
