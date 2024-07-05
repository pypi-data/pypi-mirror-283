# Python Modules
import logging

# 3rd Party Modules

# Project Modules
from sleepguard.monitors.net import NetUtilizationMonitor

log = logging.getLogger("test_net_monitors")


def test_net_util_monitor():
    import time
    monitor = NetUtilizationMonitor(5, 10, 1)
    monitor.start()

    assert monitor.is_stopped is False

    try:
        for i in range(60):
            average_value = monitor.get_average_utilization()
            assert average_value >= 0
            time.sleep(monitor.poll_period)
    finally:
        monitor.stop()
