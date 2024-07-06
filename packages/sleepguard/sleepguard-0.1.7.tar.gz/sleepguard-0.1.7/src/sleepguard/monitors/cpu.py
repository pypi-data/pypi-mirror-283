# Python Modules
import logging
import os

# 3rd Party Modules
import psutil

# Project Modules
from sleepguard.monitors import debug
from sleepguard.monitors.base import UtilizationMonitor


log = logging.getLogger(__name__)


class CpuLoadMonitor(UtilizationMonitor):
    """
    Keeps track of the average CPU load over the given ``threshold_period``.
    """

    _index_lookup = {
        1: 0,
        5: 1,
        15: 2
    }

    def __init__(
            self,
            poll_period: float,
            log_history_size: int,
            threshold: float,
            *args,
            **kwargs
    ):
        # Note the poll period is ignored.
        if log_history_size not in (1, 5, 15):
            raise ValueError(
                f"The CPU load average threshold period must be 1 or 5 or 15. "
                f"Got: {log_history_size}"
            )

        super().__init__(poll_period, log_history_size, threshold, *args, **kwargs)

        self._load_index = self._index_lookup[int(log_history_size)]

    def run(self):
        # Just exit the loop, since we aren't the ones actually monitoring
        # things.
        self.stop()

    @debug
    def get_instantaneous_value(self) -> float:
        """
        Returns the current load average reported by the OS.

        :return:
        """
        return os.getloadavg()[self._load_index]

    def get_average_utilization(self) -> float:
        """
        Get the load average over the ``threshold_period``.

        :return:
        """
        return self.get_instantaneous_value()


class CpuUtilizationMonitor(UtilizationMonitor):
    """
    Keeps track of the average CPU percent utilization over the given
    ``threshold_period``.
    """
    def __init__(
            self,
            poll_period: float,
            log_history_size: int,
            threshold: float,
            *args,
            **kwargs
    ):
        super().__init__(poll_period, log_history_size, threshold, *args, **kwargs)

    @debug
    def get_instantaneous_value(self) -> float:
        return max(psutil.cpu_percent(percpu=True))
