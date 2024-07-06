"""
A script that monitors several types of activity and prevents the system from
sleeping if the average activity level is above a threshold over a specified
period of time.
"""

# Python Modules
from __future__ import annotations

import dataclasses
import logging
import logging.handlers
import os
import pathlib
import shutil
import signal
import sys
import time

from dataclasses import dataclass, field
from importlib.resources import as_file, files
from pprint import pformat
from typing import Any, Iterable, Optional


# 3rd Party Modules
import platformdirs

from simple_parsing import ArgumentParser, DashVariant, Serializable
from simple_parsing.utils import Dataclass
from wakepy import keep

# Project Modules
from sleepguard import resources
from sleepguard import DEFAULT_LOG_FORMAT, DEFAULT_LOG_LEVEL, DEFAULT_MONITOR_CRITERIA
from sleepguard.monitors import DEFAULT_BURN_IN, DEFAULT_POLL_PERIOD, MonitorCriteria
from sleepguard.monitors.base import UtilizationMonitor
from sleepguard.monitors.factory import UtilizationMonitorFactory


APP_NAME = "sleepguard"

system_monitors: list[UtilizationMonitor] = []


@dataclass(kw_only=True)
class ProgramOptions(Dataclass):
    """
    General options for the program.
    """

    config_path: Optional[pathlib.Path] = field(default=None)
    """
    The path to a configuration file. This will override any other
    configuration files found in supported locations.
    """

    configuration: Optional[SleepGuardConfiguration] = field(default=None)
    """
    Override individual configuration options specified in the loaded 
    configuration file.
    """


@dataclass(kw_only=True)
class SleepGuardConfiguration(Serializable):
    monitor_criteria: list[MonitorCriteria] = field(default_factory=list)

    poll_period: Optional[int] = None
    """
    The number of seconds the script will check to see if the monitored
    system resources are above their respective thresholds.
    """

    burn_in: Optional[int] = None
    """
    The monitored statistics will sensitive to outliers early in the monitoring,
    so we will not start guarding until after the burn in period to allow
    some data points to be acquired.
    """

    log_level: Optional[int] = None
    """
    The python log level to use (as an integer)
    """

    log_format: Optional[str] = None
    """
    The log format.
    """

    syslog_address: Optional[str] = None
    """
    The address of the syslog server.
    """

    def __post_init__(self):
        self.monitor_criteria = [MonitorCriteria(c) for c in self.monitor_criteria]


def merge_configurations(configurations: list[SleepGuardConfiguration]) -> SleepGuardConfiguration:
    """
    Merge multiple configuration values into a single configuration value by
    prioritizing the most local configuration values.

    :param configurations:
    :return:
    """
    final_monitor_criteria: dict[str, MonitorCriteria] = dict()
    final_fields: dict[str, Any] = dict()

    # Loop through each configuration in priority order
    for current_config in configurations:
        merge_monitor_criteria(current_config, final_monitor_criteria)
        merge_fields(current_config, final_fields)

    return SleepGuardConfiguration(
        monitor_criteria=list(final_monitor_criteria.values()),
        **final_fields
    )


def merge_monitor_criteria(
        current_config: SleepGuardConfiguration,
        final_monitor_criteria: dict[str, MonitorCriteria]
):
    """
    Update the monitor criteria from the current configuration.

    :param current_config:
    :param final_monitor_criteria:

    :return:
    """

    current_monitor_criteria = current_config.monitor_criteria

    for criteria in current_monitor_criteria:
        final_criteria = final_monitor_criteria.get(criteria.system_resource)
        if final_criteria is None:
            final_criteria = criteria
            final_monitor_criteria[criteria.system_resource] = final_criteria
        else:
            if criteria.system_resource is not None:
                final_criteria.system_resource = criteria.system_resource
            if criteria.threshold is not None:
                final_criteria.threshold = criteria.threshold
            if criteria.poll_period is not None:
                final_criteria.poll_period = criteria.poll_period
            if criteria.log_history_size is not None:
                final_criteria.log_history_size = criteria.log_history_size


def merge_fields(
        current_config: SleepGuardConfiguration,
        final_fields: dict[str, Any]
):
    """

    :param current_config:
    :param final_fields:
    :return:
    """
    # All the fields except the `monitor_criteria` which is handled separately.
    fields = [
        f
        for f in dataclasses.fields(SleepGuardConfiguration)
        if f.name != "monitor_criteria"
    ]
    for config_field in fields:
        value = getattr(current_config, config_field.name)
        if value is not None:
            final_fields[config_field.name] = value


def assign_defaults(config: SleepGuardConfiguration) -> SleepGuardConfiguration:
    """
    Assign default values for configuration values that have not been set.

    :param config:
    :return:
    """
    if config.poll_period is None:
        sys.stdout.write(f"No poll_period was specified. Using: {DEFAULT_POLL_PERIOD}\n")
        config.poll_period = DEFAULT_POLL_PERIOD
    if config.burn_in is None:
        sys.stdout.write(f"No burn_in was specified. Using: {DEFAULT_BURN_IN}\n")
        config.burn_in = DEFAULT_BURN_IN
    if config.log_level is None:
        sys.stdout.write(f"No log_level was specified. Using: {DEFAULT_LOG_LEVEL}\n")
        config.log_level = DEFAULT_LOG_LEVEL
    if config.log_format is None:
        sys.stdout.write(f"No log_format was specified. Using: {DEFAULT_LOG_FORMAT}\n")
        config.log_format = DEFAULT_LOG_FORMAT

    if not config.monitor_criteria:
        sys.stdout.write(f"No monitor_criteria were specified. Using: the defaults.\n")
        config.monitor_criteria = DEFAULT_MONITOR_CRITERIA

    return config


def load_configuration(options: Optional[ProgramOptions]) -> SleepGuardConfiguration:
    """
    Load the project settings.

    :return:
    """
    if options is not None:
        config_path = options.config_path
        command_line_config = options.configuration

        # If a config path is given on the command line, use it.
        if config_path is not None:
            sys.stdout.write(f"Using the config file specified on the command line: {config_path}\n")
            return SleepGuardConfiguration.load(config_path)
    else:
        command_line_config = None

    # Get a list of the existing configuration files.
    config_paths = get_existing_configuration_files()

    if config_paths:
        # Get the highest priority config file
        config_path = config_paths[-1]
        sys.stdout.write(f"Found config file at: {config_path}\n")
    else:
        # Install and get the default configuration file
        config_path = install_default_configuration()

    # Add the base configuration to a list
    configurations = [SleepGuardConfiguration.load(config_path)]

    # If any configuration options are added on the command line, create a
    # config object from them and add them to the list.
    if command_line_config is not None:
        sys.stdout.write(
            f"Using command line options to override values in the config file: "
            f"{command_line_config}\n"
        )
        configurations.append(command_line_config)

    # Merge the configurations by overriding the base configuration with any
    # options given on the command line.
    merged_configuration = merge_configurations(configurations)

    # If any values are still missing from the configuration, use their default
    # values.
    final_configuration = assign_defaults(merged_configuration)
    sys.stdout.write(f"Using final configuration:\n{pformat(final_configuration)}\n")

    return final_configuration


def get_existing_configuration_files() -> list[pathlib.Path]:
    """
    Find and return any existing config files in the supported system or
    user directories.

    :return:
    """
    # Get the known paths where configuration files could be stored.
    configuration_paths = get_supported_configuration_paths()

    # Only keep the files that actually exist.
    return [p for p in configuration_paths if p.is_file()]


def get_supported_configuration_paths() -> list[pathlib.Path]:
    """
    Get a list of the supported configuration paths in order from the least
    priority to the highest.

    :return:
    """
    paths = platformdirs.site_config_dir(APP_NAME, multipath=True).split(os.pathsep)
    paths += [platformdirs.user_config_dir(APP_NAME)]

    return [pathlib.Path(p) / f"{APP_NAME}.yaml" for p in paths]


def is_system_util_above_threshold(
        monitors: Iterable[UtilizationMonitor]
) -> Optional[UtilizationMonitor]:
    """
    Checks if any of the measured utilization types are above their
    corresponding threshold.

    :param monitors:
    :return: The first monitor that is above their threshold or ``None`` if all
             are below their respective thresholds.
    """

    for monitor in monitors:
        if monitor.is_above_threshold():
            return monitor

    return None


def get_system_monitors(config: SleepGuardConfiguration) -> list[UtilizationMonitor]:
    """
    Get the list of system resource monitors to use.

    :return:
    """
    monitors = [UtilizationMonitorFactory.from_criteria(c) for c in config.monitor_criteria]

    # If a monitor could not be created, e.g., an unsupported GPU, a null
    # value will be returned, and we remove it here.
    monitors = [m for m in monitors if m is not None]

    return monitors


def get_sleep_inhibitor_method() -> str:
    """
    Gets the method used to keep the system awake.

    :return:
    """
    with keep.running() as r:
        method = r.used_method
        time.sleep(0.1)

    return method


def get_default_configuration_path() -> pathlib.Path:
    """
    Get the absolute path of the default configuration file.

    :return:
    """
    with as_file(files(resources).joinpath("default_configuration.yaml")) as path:
        return path


def install_default_configuration() -> pathlib.Path:
    """
    Install a default configuration in the user's home directory, if no
    configuration is detected in any of the supported locations.

    :return: The path to the newly created default configuration file.
    """
    user_dir = pathlib.Path(platformdirs.user_config_dir(APP_NAME))
    user_config_file = user_dir / f"{APP_NAME}.yaml"
    default_config_file = get_default_configuration_path()

    user_dir.mkdir(parents=True, exist_ok=True)

    sys.stdout.write(
        f"No configuration file detected. Installing the default "
        f"configuration to: {user_config_file}\n"
    )

    shutil.copyfile(default_config_file, user_config_file)

    return user_config_file


def setup_logging(configuration: SleepGuardConfiguration) -> logging.Logger:
    """
    Setup the logging.

    :param configuration:
    :return:
    """
    logging.basicConfig(
        level=configuration.log_level,
        format=configuration.log_format,
    )

    if configuration.syslog_address is not None:
        syslog_handler = logging.handlers.SysLogHandler(address=configuration.syslog_address)
        syslog_handler.ident = f"[{APP_NAME}] "
        syslog_handler.setLevel(configuration.log_level)
        logging.getLogger().addHandler(syslog_handler)

    log = logging.getLogger(APP_NAME)
    log.info(f"Starting Sleep Guard with inhibitor: {get_sleep_inhibitor_method()}")
    log.debug(f"Using configuration: {configuration}")

    return log


def main(options: Optional[ProgramOptions] = None):
    """

    :return:
    """
    # Use a global variables for these so I can stop them in the signal handler
    global system_monitors

    config = load_configuration(options)
    log = setup_logging(config)

    # Initialize all the system resource monitors
    system_monitors.extend(get_system_monitors(config))

    # Start the monitoring threads
    [monitor.start() for monitor in system_monitors]

    log.debug(f"Starting burn in period")
    time.sleep(config.burn_in)

    log.debug(f"Starting main loop")

    # The main loop
    while any([m.is_running for m in system_monitors]):
        inhibit_monitor = is_system_util_above_threshold(system_monitors)
        if inhibit_monitor is not None:
            with keep.running():
                log.debug(
                    f"Keeping the system awake because the {inhibit_monitor.__class__.__name__} "
                    f"average value {inhibit_monitor.get_average_utilization():0.2f} is "
                    f"above its threshold of {inhibit_monitor.threshold:0.2f}"
                )
                log.debug(f"Log values: {inhibit_monitor.get_current_logs()}")

                # keep.running should reset the idle timer, so there shouldn't
                # be a need to sleep for a long time.
                time.sleep(1)

        log.debug(f"Will recheck system utilization in {config.poll_period} seconds")
        time.sleep(config.poll_period)


def signal_handler(sig, frame):
    """
    Log that we are shutting down if Ctrl+C is pressed or SIGTERM is received.

    :param sig:
    :param frame:
    :return:
    """
    log = logging.getLogger(APP_NAME)
    log.info(
        f"Terminating Sleep Guard. Waiting for the burn in to complete and "
        f"all monitors to stop."
    )
    [m.stop() for m in system_monitors]


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Prevent the system from sleeping when the system is active.",
        add_option_string_dash_variants=DashVariant.UNDERSCORE_AND_DASH
    )
    parser.add_arguments(ProgramOptions, dest="options")

    program_options = parser.parse_args().options

    main(program_options)
