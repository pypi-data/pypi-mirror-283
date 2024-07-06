#!/usr/bin/env bash
set -e

# A startup script for KDE (and possibly other desktop environments).
# It will check for the existence of a virtual environment at
# ~/.virtualenvs/sleepguard. If one does not exist it will create a new one
# and install sleepguard. Once the virtual environment is set up it will
# start sleepguard.

VENV_DIR="${HOME}/.virtualenvs/sleepguard"

if [ ! -d "${VENV_DIR}" ]
then
  # If the virtual environment doesn't already exist, then create it
  # and install sleepguard
  logger -p use.notice -t sleepguard "Creating a new virtual environment at: ${VENV_DIR}"

  mkdir -p "${HOME}/.virtualenvs"

  python -m venv "${VENV_DIR}"

  # shellcheck source="${HOME}/.virtualenvs/sleepguard"
  source "${VENV_DIR}/bin/activate"

  pip install sleepguard[all]
else
  # Otherwise activate the existing virtual environment
  logger -p user.debug -t sleepguard "Using existing virtual environment at: ${VENV_DIR}"

  source "${VENV_DIR}/bin/activate"
fi

sleepguard
