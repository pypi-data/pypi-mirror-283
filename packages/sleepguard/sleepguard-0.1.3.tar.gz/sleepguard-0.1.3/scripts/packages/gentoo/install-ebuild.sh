#!/usr/bin/env bash

# Copy the required contents of the current directory to install the ebuild
# into a local Gentoo repository given on the command line.

PACKAGE_VERSION=0.1.3

usage() {
  echo "Usage: $0 <local-ebuild-repository>"
  echo "This script copies the ebuild files in the current directory to the specified local ebuild repository."
  exit 1
}

# Check that exactly one argument is given.
if [ "$#" -ne 1 ]; then
    usage
fi

if [ ! -d "$1" ]; then
  echo "The ebuild repository does not exist: $1"
  usage
fi

script_directory="$(dirname "$(realpath "$0")")"
parent_directory="$(dirname "${script_directory}")"
ebuild_repository=$1
ebuild_directory="${ebuild_repository}/sys-power/sleepguard"

cd "${parent_directory}" || exit 1

# Create the ebuild directory if it does not exist.
mkdir -p "${ebuild_directory}"

# Copy the required files to the ebuild directory
rsync -r --exclude="README.md" --exclude="install-ebuild.sh" "${parent_directory}/gentoo/" "${ebuild_directory}/"

# Rename the ebuild file to append the version
mv "${ebuild_directory}/sleepguard.ebuild" "${ebuild_directory}/sleepguard-${PACKAGE_VERSION}.ebuild"

# Move to the ebuild directory
cd "${ebuild_directory}" || exit 1

# Create the package's Manifest file
pkgdev manifest
