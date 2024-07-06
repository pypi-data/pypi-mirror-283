# Python Modules
import abc
import logging
import statistics
import time
import threading

from collections import deque

# 3rd Party Modules

# Project Modules
from sleepguard.monitors import debug


log = logging.getLogger(__name__)


class UtilizationMonitor(threading.Thread, abc.ABC):
    """
    A base class for all system utilization monitoring threads.
    """
    def __init__(
            self,
            poll_period: float,
            log_history_size: int,
            threshold: float,
            *args,
            **kwargs
    ):
        """

        :param poll_period: The number of seconds between logging the system
               resource.
        :param log_history_size: The number of values to store in the
               resource utilization logs. The average utilization will
               be calculated from these values.
        :param threshold: The value at which sleep will be inhibited if the
               average utilization value exceeds it.
        """
        super().__init__(*args, **kwargs)

        if poll_period <= 0:
            raise ValueError("poll_period must be greater than zero")

        if log_history_size <= 0:
            raise ValueError("log_history_size must be greater than zero")

        if threshold < 0:
            raise ValueError("threshold must be positive")

        self._poll_period = poll_period
        self._log_history_size = log_history_size
        self._threshold = threshold
        self._logs = deque(maxlen=log_history_size)
        self._is_stopped = threading.Event()
        self._lock = threading.Lock()

    def stop(self):
        """
        Terminate the execution of this monitor.
        """
        self._is_stopped.set()

    @property
    def is_stopped(self) -> bool:
        """
        Checks if the thread is stopped.

        :return:
        """
        return self._is_stopped.is_set()

    @property
    def is_running(self) -> bool:
        """
        Checks if the thread is running (not stopped).

        :return:
        """
        return not self._is_stopped.is_set()

    @property
    def poll_period(self) -> float:
        """
        How often the value of the system resource is polled.

        :return:
        """
        return self._poll_period

    @property
    def threshold(self) -> float:
        """
        The value at which sleep will be inhibited if the average utilization
        value exceeds it.

        :return:
        """
        return self._threshold

    def run(self):
        """
        The main thread loop.

        :return:
        """
        while not self.is_stopped:
            value = self.get_instantaneous_value()
            with self._lock:
                self._logs.appendleft(value)

            log.debug(f"Sleeping for poll_period: {self._poll_period}")
            time.sleep(self._poll_period)

    @abc.abstractmethod
    def get_instantaneous_value(self) -> float:
        """
        Return the instantaneous value of the monitored system resource.

        :return:
        """
        pass

    def get_current_logs(self) -> list[float]:
        """
        Get the current logged values as a list.

        :return:
        """
        with self._lock:
            return list(self._logs)

    @debug
    def get_average_utilization(self) -> float:
        """
        Get the average utilization of the monitored resource over the
        ``threshold_period``.

        :return:
        """
        logs = self.get_current_logs()
        if not logs:
            return 0.0

        return statistics.mean(logs)

    def is_above_threshold(self) -> bool:
        """
        Returns true if the value from ``get_average_utilization`` is above the
        ``threshold``.

        :return:
        """
        return self.get_average_utilization() > self.threshold
