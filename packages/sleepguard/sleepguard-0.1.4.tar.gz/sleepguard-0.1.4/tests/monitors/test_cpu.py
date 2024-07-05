# Python Modules
import logging

# 3rd Party Modules

# Project Modules
from sleepguard.monitors.cpu import CpuLoadMonitor, CpuUtilizationMonitor

log = logging.getLogger("test_cpu_monitors")


def test_cpu_load_monitor():
    log.debug(f"testing cpu_load_monitor")
    monitor = CpuLoadMonitor(0.5, 60, 1)
    monitor.start()

    assert monitor.is_stopped is True
    assert monitor.get_instantaneous_value() > 0


def test_cpu_util_monitor():
    import time
    monitor = CpuUtilizationMonitor(0.25, 1, 1)
    monitor.start()

    assert monitor.is_stopped is False

    try:
        for i in range(3):
            current_value = monitor.get_instantaneous_value()
            average_value = monitor.get_average_utilization()
            assert 0 < current_value <= 100
            assert 0 <= average_value <= 100
            time.sleep(monitor.poll_period)
    except:
        pass
    finally:
        monitor.stop()
