Create a local ebuild repository, if you do not already have one.
See the [Gentoo Wiki](https://wiki.gentoo.org/wiki/Creating_an_ebuild_repository).


Run the following commands to install the ebuild (or execute the `install-ebuild.sh` script).

```bash
# Copy this directory (gentoo) into a local ebuild repository:
root> cp -r ../gentoo ${repo}/sys-power/sleepguard

# Move to the new ebuild directory
root$ cd ${repo}/sys-power/sleepguard

# Change the name of the file to append the current version
root$ mv sleepguard.ebuild sleepguard-${PV}.ebuild

# Create the package's Manifest file
root$ pkgdev manifest
```
