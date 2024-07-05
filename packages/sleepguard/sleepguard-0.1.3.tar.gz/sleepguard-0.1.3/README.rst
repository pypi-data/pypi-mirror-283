Sleep Guard
===========

Other tools such as `Caffeine <https://launchpad.net/caffeine>`__ for Linux and `Caffeinate <https://ss64.com/mac/caffeinate.html>`__ for the Mac will keep your system awake, but require explicit action by the user.
If you are like me, I often start a long running process, but forget to actually take the explicit action and come back to a sleeping system with no work done.

``sleepguard`` is a program that monitors several system resources and prevents the computer from sleeping automatically if it detects significant activity (as defined by the user).


Installation
============

.. code-block::

    pip install sleepguard

To enable GPU monitoring you must install one (or both) of the optional variants: ``amd`` for AMD or ``nvidia`` for NVIDIA cards.

.. code-block::

    pip install sleepguard[amd,nvidia]

Basic Usage
===========

The main application is implemented in the ``sleepguard.guard`` module and can be run like any other python application.
This will start an infinite loop that periodically polls the desired system resources and will prevent the system from sleeping [1]_ if any of the values are above their configured thresholds.

.. code-block::

    python -m sleepguard.gaurd

Full Documentation
==================

See `read the docs <https://sleepguard.readthedocs.io/en/latest/>`__ for the full documentation and configuration options.


.. [1] For at least KDE and Gnome, the idle timer is reset when activity is detected.
       If not other activity is detected, this will cause sleep to be disabled for the number of minutes configured in DE's power management settings.
       It is also the likely behavior for other desktop environments, but is untested.
