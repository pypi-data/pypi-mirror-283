# Python Modules
import logging
import os
import time

# 3rd Party Modules
import psutil

from sleepguard.monitors import debug
# Project Modules
from sleepguard.monitors.base import UtilizationMonitor


log = logging.getLogger(__name__)


class NetUtilizationMonitor(UtilizationMonitor):
    """
    Keeps track of the average total number of bytes sent and received per
    second over the given ``threshold_period``.
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

        # psutil.net_io will return the total number of bytes since the system
        # started. To get a snapshot we need to calculate the difference
        # between the current and previous value, which is initialized here
        # at the start of the monitor.
        self._previous_value = self._get_total_bytes()

    def run(self):
        # We're going to sleep here before starting the loop otherwise the
        # first instantaneous value reading will likely be 0.
        time.sleep(self.poll_period)

        super().run()

    @debug
    def get_instantaneous_value(self) -> float:
        total_bytes = self._get_total_bytes()
        bytes_per_second = (total_bytes - self._previous_value) / self._poll_period

        with self._lock:
            self._previous_value = total_bytes

        return bytes_per_second

    @staticmethod
    def _get_total_bytes() -> int:
        net_io = psutil.net_io_counters()
        if net_io is None:
            return 0

        total_bytes = net_io.bytes_sent + net_io.bytes_recv

        return total_bytes
