# Python Modules
import logging

from typing import Literal

from sleepguard.monitors import debug
# 3rd Party Modules

# Project Modules
from sleepguard.monitors.base import UtilizationMonitor


log = logging.getLogger(__name__)


GpuType = Literal["amd", "nvidia"]


class GpuUtilizationMonitor(UtilizationMonitor):
    """
    Keeps track of the average GPU percent utilization over the given
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

        self.device_types = self.get_device_types()

        if not self.device_types:
            raise ValueError("No GPU devices found.")
        else:
            log.debug(f"Found GPU devices: {self.device_types}")

    @staticmethod
    def get_device_types() -> list[GpuType]:
        """
        Get the list of available GPU types installed on the system.

        :return:
        """
        devices: list[GpuType] = []
        try:
            import GPUtil

            if GPUtil.getGPUs():
                devices.append("nvidia")
        except Exception as e:
            log.debug(f"Unable to find any NVIDIA GPUs: {e}")

        try:
            import pyadl
            if pyadl.ADLManager.getInstance().getDevices():
                devices.append("amd")
        except Exception as e:
            log.debug(f"Unable to find any AMD GPUs: {e}")

        return devices

    @debug
    def get_instantaneous_value(self) -> float:
        """
        Returns the max utilization over all the detected GPU devices.

        :return:
        """
        values = [self._get_utilization(t) for t in self.device_types] or [0]

        return max(values)

    def _get_utilization(self, device_type: GpuType) -> float:
        if device_type == "amd":
            return self._get_amd_utilization()
        elif device_type == "nvidia":
            return self._get_nvidia_utilization()
        else:
            raise NotImplementedError(f"Unsupported gpu type: {device_type}")

    @staticmethod
    def _get_amd_utilization() -> float:
        import pyadl

        devices = pyadl.ADLManager.getInstance().getDevices()

        return max([d.getCurrentUsage() for d in devices])

    @staticmethod
    def _get_nvidia_utilization() -> float:
        import GPUtil

        gpus = GPUtil.getGPUs()

        return max([gpu.load * 100 for gpu in gpus])
