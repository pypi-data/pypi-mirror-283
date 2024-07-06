Sleep Guard
===========

Other tools such as `Caffeine <https://launchpad.net/caffeine>`__ for Linux and `Caffeinate <https://ss64.com/mac/caffeinate.html>`__ for the Mac will keep your system awake, but require explicit action by the user.
If you are like me, I often start a long running process, but forget to actually take the explicit action and come back to a sleeping system with no work done.

``sleepguard`` is a program that monitors several system resources and prevents the computer from sleeping automatically if it detects significant activity (as defined by the user).

Dependencies
============

Primary
-------
Installed by default.

`wakepy <https://github.com/fohrloop/wakepy>`__
    A cross platform library for keeping the system awake.
`psutil <https://github.com/giampaolo/psutil>`__
    A cross platform library for retrieving various system attributes.
`platformdirs <https://github.com/platformdirs/platformdirs>`__
    A cross platform library for finding the appropriate location to store user data and configuration files.
`simple-parsing <https://github.com/lebrice/SimpleParsing>`__
    A library for enhanced type-safe command line parsing.

Extras
--------

`pyadl <https://github.com/nicolargo/pyadl>`__
    A library for retrieving information about AMD GPUs.
`gputil <https://github.com/anderskm/gputil>`__
    A library for retrieving information about NVIDIA GPUs.

Installation
============

.. code-block::

    pip install sleepguard

To enable GPU monitoring you must install one (or both) of the optional variants: ``amd`` for AMD or ``nvidia`` for NVIDIA cards.

.. code-block::

    pip install sleepguard[amd,nvidia]

Basic Usage
===========

The main application is implemented in the :mod:`sleepguard.guard` module and can be run like any other python application.
This will start an infinite loop that periodically polls the desired system resources and will prevent the system from sleeping [1]_ if any of the values are above their configured thresholds.

.. code-block::

    python -m sleepguard.gaurd

System Monitors
===============

Each monitor has 3 parameters controlling its behavior:

poll_period
    The number of seconds to wait before querying the given system resource.
log_history_size
    The number of query results to keep.
    For example, if ``poll_period=2`` and ``log_history_size=30``, then one minute's worth of data will be tracked.
    Older entries are purged to make room for newer entries.
threshold
    When the average value of the entries of the logged values is above this value, the system is considered active and ``sleepguard`` will keep the system awake.
    This value is dependent on both the resource being monitored and the user's needs.

There are 4 supported system monitors.

1. :class:`~sleepguard.monitors.cpu.CpuLoadMonitor` is used to monitor `the average CPU load <https://en.wikipedia.org/wiki/Load_(computing)>`__.
2. :class:`~sleepguard.monitors.cpu.CpuUtilizationMonitor` is used to monitor the percent CPU utilization of the system.
   The CPU utilization is the fraction of the current CPU usage relative to its total capacity represented as a percentage (from 0-100).
   Each time the monitor polls the CPU utilization it considers each logical core separately and logs the maximum utilization.
3. :class:`~sleepguard.monitors.gpu.GpuUtilizationMonitor` is used to monitor the percent GPU utilization.
   This is similar to the ``CpuUtilizationMonitor`` but for GPUs.
   In theory, it should support any number of AMD or NVIDIA GPUs, but has only been tested with a single NVIDIA GPU.
   Other GPUs are not supported.
   Setting the threshold for the GPU appears to be the most system dependent.
   Newer and more powerful GPUs seem to have higher idle usage.
   So, it may be necessary to set the GPU utilization to a relatively high value (e.g., 30-50%) to ensure the system will sleep.
   This should be fine since most applications that necessitate staying awake (e.g., machine learning) would use significantly more than this.
4. :class:`~sleepguard.monitors.net.NetUtilizationMonitor` is used to monitor the number of bytes per second sent and received on all active network interfaces.

By default all supported monitors are enabled.


.. [1] For at least KDE and Gnome, the idle timer is reset when activity is detected.
       If not other activity is detected, this will cause sleep to be disabled for the number of minutes configured in DE's power management settings.
       It is also the likely behavior for other desktop environments, but is untested.

Configuration
=============

The :class:`~sleepguard.guard.SleepGuardConfiguration` class defines the available configuration options.
The primary method of specifying the configuration is through a declarative YAML file.
The script will look for a configuration file named ``sleepguard.yaml`` in in any path returned by ``platformdirs.site_config_dir('sleepguard', multipath=True)`` or ``platformdirs.user_config_dir('sleepguard')``.
For example, ``/home/username/.config/sleepguard/sleepguard.yaml``.

You can also specify the location to a configuration file on the command line with the ``--config-path`` option.
If no config file is found or specified on the command line, a default config file will be installed in the user's config directory as described above.
It is also possible to specify individual config options on the command line (see the `Full Usage`_ below), which will override any values set in the loaded configuration file.

The full set of configuration options is given in the default configuration file:

.. literalinclude:: ../../src/sleepguard/resources/default_configuration.yaml
   :language: yaml


Full Usage
==========
.. code-block:: none

    usage: guard.py [-h] [--config-path [Path]] [--monitor-criteria List]
                    [--poll_period [int]] [--burn_in [int]] [--log_level [int]]
                    [--log_format [str]] [--syslog_address [str]]

    Prevent the system from sleeping when the system is active.

    options:
      -h, --help            show this help message and exit

    ProgramOptions ['options']:
      Command line arguments for the program.

      --config-path [Path], --config_path [Path]
                            The path to a configuration file. (default: None)

    SleepGuardConfiguration ['options.configuration']:

      Override file based configuration values from the command line.

      --monitor-criteria List, --monitor_criteria List
                            (default: [])
      --poll_period [int], --poll-period [int]
                            The number of seconds the script will check to see if
                            the monitored system resources are above their
                            respective thresholds. (default: None)
      --burn_in [int], --burn-in [int]
                            The monitored statistics will sensitive to outliers
                            early in the monitoring, so we will not start guarding
                            until after the burn in period to allow some data
                            points to be acquired. (default: None)
      --log_level [int], --log-level [int]
                            The python log level to use (as an integer) (default:
                            None)
      --log_format [str], --log-format [str]
                            The log format. (default: None)
      --syslog_address [str], --syslog-address [str]
                            The address of the syslog server. (default: None)

