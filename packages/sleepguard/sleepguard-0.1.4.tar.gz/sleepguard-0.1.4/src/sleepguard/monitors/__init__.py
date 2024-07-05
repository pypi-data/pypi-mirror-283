"""
Utility methods and classes for monitoring system utilization.
"""

# Python Modules
import functools
import logging
from collections import UserDict

from dataclasses import dataclass
from typing import Callable, Literal, get_args

# 3rd Party Modules
import psutil

# Project Modules

log = logging.getLogger(__name__)


SystemResource = Literal["cpu_load", "cpu_util", "gpu_util", "net_util"]
"""
The valid types of system resources to monitor.
"""


DEFAULT_POLL_PERIOD = 2
DEFAULT_BURN_IN = 60
DEFAULT_LOG_HISTORY_SiZE = 60
DEFAULT_CPU_LOAD_LOG_HISTORY_SIZE = 1
DEFAULT_CPU_LOAD_THRESHOLD = 2.0
DEFAULT_CPU_UTIL_THRESHOLD = 25
DEFAULT_GPU_UTIL_THRESHOLD = 40
DEFAULT_NET_UTIL_THRESHOLD = 8192


def debug(fn: Callable):
    """
    A decorator that logs the given member function's return value.
    '
    :param fn:
    :return:
    """
    @functools.wraps(fn)
    def _wrapper(self, *args, **kwargs):
        cls_name = self.__class__.__name__
        method_name = fn.__name__
        value = fn(self, *args, **kwargs)

        log.debug(f"{cls_name}.{method_name} -> {value}")

        return value

    return _wrapper


class MonitorCriteria(UserDict):
    """
    The criteria used for monitoring a given system resource and determining
    if it should prevent the system from sleeping.

    .. note::
       This is implemented as a dictionary because ``simple-parsing`` does
       not support lists of dataclasses.
    """
    # system_resource: SystemResource
    # """
    # The system resource to monitor.
    # """
    #
    # threshold: float
    # """
    # If the average value of this resource over the `threshold_period` is
    # above this value then the system will be inhibited from sleeping for
    # `inhibit_duration` seconds.
    # """
    #
    # poll_period: int = DEFAULT_POLL_PERIOD
    # """
    # The system resource will be monitored and logged every `poll_period`
    # seconds.
    # """
    #
    # log_history_size: float = DEFAULT_LOG_HISTORY_SiZE
    # """
    # The maximum number of values to store in the monitor logs, which will be
    # used to calculate the average resource utilization.
    # """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setdefault("poll_period", DEFAULT_POLL_PERIOD)
        self.setdefault("log_history_size", DEFAULT_LOG_HISTORY_SiZE)

        valid_keys = ("system_resource", "threshold", "poll_period", "log_history_size")
        required_keys = ("system_resource", "threshold")

        if not all(k in valid_keys for k in self.keys()):
            raise ValueError(
                f"One or more of the MonitorCriteria keys are invalid. "
                f"They must be one of {valid_keys}"
            )

        if not all(rk in self.keys() for rk in required_keys):
            raise ValueError(f"MonitorCriteria is missing a required key: {required_keys}")

        if self.system_resource not in get_args(SystemResource):
            raise ValueError(f"Invalid system resource: {self.system_resource}")

    @property
    def system_resource(self) -> SystemResource:
        return self.data.get("system_resource")

    @system_resource.setter
    def system_resource(self, value: SystemResource):
        self.data["system_resource"] = value

    @property
    def threshold(self) -> float:
        return self.data.get("threshold")

    @threshold.setter
    def threshold(self, value: float):
        self.data["threshold"] = value

    @property
    def poll_period(self) -> float:
        return self.data.get("poll_period")

    @poll_period.setter
    def poll_period(self, value: float):
        self.data["poll_period"] = value

    @property
    def log_history_size(self) -> int:
        return self.data.get("log_history_size")

    @log_history_size.setter
    def log_history_size(self, value: int):
        self.data["log_history_size"] = value

    def as_kwargs(self) -> dict[str, int | float]:
        """
        Return the criteria as ``kwargs`` suitable for constructing a
        :class:`~monitors.base.UtilizationMonitor` instance.

        :return:
        """
        return {
            "poll_period": self.poll_period,
            "log_history_size": self.log_history_size,
            "threshold": self.threshold,
        }
