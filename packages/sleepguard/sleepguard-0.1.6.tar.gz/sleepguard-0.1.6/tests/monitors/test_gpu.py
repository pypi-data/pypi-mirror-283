# Python Modules
import logging

# 3rd Party Modules

# Project Modules
from sleepguard.monitors.gpu import GpuUtilizationMonitor


log = logging.getLogger("test_gpu_monitors")


def test_gpu_util_monitor():
    import time
    monitor = GpuUtilizationMonitor(0.25, 1, 1)
    monitor.start()

    assert monitor.is_stopped is False

    try:
        for i in range(3):
            current_value = monitor.get_instantaneous_value()
            average_value = monitor.get_average_utilization()
            assert 0 < current_value <= 100
            assert 0 <= average_value <= 100
            time.sleep(monitor.poll_period)
    except Exception as e:
        log.error(f"Error: {e}")
    finally:
        monitor.stop()
