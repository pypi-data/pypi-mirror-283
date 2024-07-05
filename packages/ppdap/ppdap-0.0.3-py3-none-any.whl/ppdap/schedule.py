"""Support for DigoBridge schedule."""
import logging
import time

logger = logging.getLogger(__name__)


class DigoSchedule:
    """Class representing a schedule."""

    def __init__(self) -> None:
        """Initialize an empty schedule."""
        self.schedules_: dict[str, dict] = {}

    def get_schedules(self) -> list[dict]:
        """Return a list of all schedules."""
        return list(self.schedules_.values())

    def add_schedules(self, schedules: list[dict]) -> bool:
        """Add a list of schedules to the existing schedules.

        Each schedule is a dictionary with keys: 'code', 'enable', 'time', 'repeat', 'notify', 'target'.
        """
        for item in schedules:
            if (
                "code" not in item
                or "enable" not in item
                or "time" not in item
                or "repeat" not in item
                or "notify" not in item
                or "target" not in item
            ):
                continue
            self.schedules_[item["code"]] = item
        return True

    def edit_schedules(self, schedules: list[dict]) -> bool:
        """Edit existing schedules with the provided list of schedules.

        Each schedule is a dictionary with keys: 'code', 'enable', 'time', 'repeat', 'notify', 'target'.
        """
        for item in schedules:
            if "code" not in item:
                continue
            if item["code"] not in self.schedules_:
                continue
            if "enable" in item:
                self.schedules_[item["code"]]["enable"] = item["enable"]
            if "time" in item:
                self.schedules_[item["code"]]["time"] = item["time"]
            if "repeat" in item:
                self.schedules_[item["code"]]["repeat"] = item["repeat"]
            if "notify" in item:
                self.schedules_[item["code"]]["notify"] = item["notify"]
            if "target" in item:
                self.schedules_[item["code"]]["target"] = item["target"]

        return True

    def delete_schedules(self, schedules: list[dict]) -> None:
        """Delete the provided list of schedules from the existing schedules.

        Each schedule is a dictionary with a key: 'code'.
        """
        for item in schedules:
            if "code" not in item:
                continue
            if item["code"] in self.schedules_:
                del self.schedules_[item["code"]]

    def check(self) -> list[dict]:
        """Return a list of schedules that are enabled, match the current time, and either repeat or are one-time."""
        ret: list[dict] = []
        t = time.localtime()
        current_time = time.strftime("%H%M", t)
        for item in self.schedules_.values():
            if (
                item["enable"] is True
                and (item["repeat"] == 0 or (item["repeat"] & (1 << t.tm_wday)) != 0)
                and item["time"] == current_time
            ):
                ret.append(item)
                if item["repeat"] == 0:
                    item["enable"] = False
        return ret
