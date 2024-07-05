# Python Modules
import logging
from typing import Optional

# 3rd Party Modules

from sleepguard.monitors import MonitorCriteria
from sleepguard.monitors.base import UtilizationMonitor
from sleepguard.monitors.cpu import CpuLoadMonitor, CpuUtilizationMonitor
from sleepguard.monitors.gpu import GpuUtilizationMonitor
from sleepguard.monitors.net import NetUtilizationMonitor

# Project Modules


log = logging.getLogger(__name__)


class UtilizationMonitorFactory:
    """
    A factory class for creating :class:`~monitors.base.UtilizationMonitor`
    instances.
    """

    @staticmethod
    def from_criteria(
            criteria: MonitorCriteria,
            raise_on_error: bool = False
    ) -> Optional[UtilizationMonitor]:
        """
        Create an instance of a :class:`~monitors.base.UtilizationMonitor`
        from the given ``criteria``.

        :param criteria: The ``MonitorCriteria`` to used to create the instance.
        :param raise_on_error: If ``True``, an exception will be raised if
               the instance cannot be created, for example an unsupported
               GPU is detected when using the ``GpuUtilizationMonitor``.
               Otherwise, ``None`` is returned.
        :return:
        """
        if criteria.system_resource == "cpu_load":
            monitor_cls = CpuLoadMonitor
        elif criteria.system_resource == "cpu_util":
            monitor_cls = CpuUtilizationMonitor
        elif criteria.system_resource == "gpu_util":
            has_gpu = len(GpuUtilizationMonitor.get_device_types()) > 0
            if has_gpu or raise_on_error:
                monitor_cls = GpuUtilizationMonitor
            else:
                return None
        elif criteria.system_resource == "net_util":
            monitor_cls = NetUtilizationMonitor
        else:
            raise ValueError("Unsupported system resource type")

        return monitor_cls(**criteria.as_kwargs())
