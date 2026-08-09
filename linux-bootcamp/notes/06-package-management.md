# Linux Package Management

## What I Learned

Linux package management is used to install, remove, update, search, inspect, and troubleshoot software.

On Zorin OS, the main tools are:

- apt — higher-level package manager
- dpkg — lower-level Debian package manager

## APT

### Check Version

apt --version

### Refresh Package Information

sudo apt update

apt update refreshes package metadata. It does not upgrade installed packages.

### List Installed Packages

apt list --installed

Example:

apt list --installed 2>/dev/null | grep '^tree/'

### Show Package Information

apt show tree

Useful information includes:

- Package name
- Version
- Dependencies
- Download size
- Installed size
- Repository
- Description

### Search Packages

apt search TERM

### Install

sudo apt install PACKAGE

### Remove

sudo apt remove PACKAGE

### Purge

sudo apt purge PACKAGE

remove removes the package while package-managed configuration may remain.

purge removes the package and its package-managed configuration.

### Autoremove

sudo apt autoremove

Removes automatically installed dependencies that are no longer required.

Safely preview it with:

sudo apt autoremove --dry-run

--dry-run shows what would happen without making the change.

## DPKG

dpkg is the lower-level Debian package management tool.

### List Packages

dpkg -l

Check whether tree is installed:

dpkg -l | grep '^ii  tree'

ii means the package is desired and currently installed.

### Package Status

dpkg -s tree

Important result:

Status: install ok installed

### Package to Files

dpkg -L tree

Shows every file installed by the tree package.

### File to Package

dpkg -S /usr/bin/tree

Example:

tree: /usr/bin/tree

This tells us that /usr/bin/tree belongs to the tree package.

## which

which tree

Example:

/usr/bin/tree

which answers:

Where is the executable?

Whereas:

dpkg -S /usr/bin/tree

answers:

Which package owns the executable?

## Package Troubleshooting Workflow

Problem
   ↓
Check command
   ↓
Find executable
   ↓
Find owning package
   ↓
Check package status
   ↓
Inspect package files
   ↓
Inspect dependencies
   ↓
Make change
   ↓
Verify

Useful commands:

which COMMAND
dpkg -S /path/to/executable
dpkg -s PACKAGE
dpkg -L PACKAGE
apt show PACKAGE

## Hands-on Example: tree

Find executable:

which tree

Result:

/usr/bin/tree

Find owning package:

dpkg -S /usr/bin/tree

Result:

tree: /usr/bin/tree

Check package status:

dpkg -s tree

Result:

Status: install ok installed

List package files:

dpkg -L tree

Inspect package information:

apt show tree

## .deb Packages

A .deb file is a Debian package archive.

Install a local .deb using dpkg:

sudo dpkg -i some-package.deb

-i means install.

Inspect a .deb:

dpkg -I package.deb

List files inside a .deb:

dpkg -c package.deb

## APT vs DPKG

APT
├── repositories
├── package search
├── dependency resolution
├── downloads
└── installation

DPKG
├── Debian package database
├── .deb packages
├── package status
└── package/file inspection

APT is normally preferred for repository-based installation because it handles dependencies.

## Important Lessons

- apt update refreshes package information but does not upgrade packages.
- apt show PACKAGE displays package information and dependencies.
- dpkg -s PACKAGE checks package status.
- dpkg -L PACKAGE shows files installed by a package.
- dpkg -S FILE finds which package owns a file.
- which COMMAND finds the executable in the current PATH.
- --dry-run lets us preview potentially destructive operations.
- A .deb is a Debian package file.
- dpkg -i package.deb installs a local .deb.
- APT is higher-level; dpkg is lower-level.
- Good troubleshooting starts with inspection instead of blindly installing or removing software.

## Cheat Sheet

apt --version — Show APT version

sudo apt update — Refresh package metadata

apt list --installed — List installed packages

apt show PACKAGE — Show package information

apt search TERM — Search packages

sudo apt install PACKAGE — Install package

sudo apt remove PACKAGE — Remove package

sudo apt purge PACKAGE — Remove package and package-managed configuration

sudo apt autoremove --dry-run — Preview automatic removals

dpkg -l — List package states

dpkg -s PACKAGE — Show package status

dpkg -L PACKAGE — List package files

dpkg -S FILE — Find package owning a file

sudo dpkg -i FILE.deb — Install local .deb

which COMMAND — Find executable

## Status

Linux Package Management — Completed

Next:

Linux Networking Fundamentals
