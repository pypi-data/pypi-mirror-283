# Python Modules
import logging

from sleepguard.monitors import DEFAULT_CPU_LOAD_LOG_HISTORY_SIZE, DEFAULT_CPU_LOAD_THRESHOLD, \
    DEFAULT_CPU_UTIL_THRESHOLD, \
    DEFAULT_GPU_UTIL_THRESHOLD, DEFAULT_NET_UTIL_THRESHOLD, MonitorCriteria

# 3rd Party Modules

# Project Modules


DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)-15s [%(name)s]:%(lineno)d %(levelname)s %(message)s"
DEFAULT_MONITOR_CRITERIA: list[MonitorCriteria] = [
    MonitorCriteria(
        system_resource="cpu_load",
        threshold=DEFAULT_CPU_LOAD_THRESHOLD,
        log_history_size=DEFAULT_CPU_LOAD_LOG_HISTORY_SIZE,
    ),
    MonitorCriteria(system_resource="cpu_util", threshold=DEFAULT_CPU_UTIL_THRESHOLD),
    MonitorCriteria(system_resource="gpu_util", threshold=DEFAULT_GPU_UTIL_THRESHOLD),
    MonitorCriteria(system_resource="net_util", threshold=DEFAULT_NET_UTIL_THRESHOLD)
]
