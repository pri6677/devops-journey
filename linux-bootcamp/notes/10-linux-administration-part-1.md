# Linux Administration — Part 1

> **Purpose:** Complete Linux Administration knowledge from a system administrator's perspective.
>
> **Practical mode:** The commands and representative outputs below document the practicals as if they were performed. The hands-on commands can be repeated later.
>
> **Operating environment used for examples:** Zorin OS 18 / Ubuntu-based Linux, Bash, systemd.

---

# 1. What Is Linux Administration?

Linux administration means:

> **Managing, maintaining, securing, monitoring, troubleshooting, and automating a Linux computer or server.**

A Linux administrator needs to understand much more than individual commands.

For example, if a website is not working, an administrator might need to determine:

```text
Is the server running?
       ↓
Is the service running?
       ↓
Is the process running?
       ↓
Is the port listening?
       ↓
Is the disk full?
       ↓
Is memory exhausted?
       ↓
Are there errors in the logs?
       ↓
Is the firewall blocking traffic?
       ↓
Is the network working?
```

This is why Linux Administration connects many earlier Linux topics together.

---

# 2. Linux Administrator Mental Model

Think of a Linux server as a large office building.

```text
Linux System
│
├── Users
│   └── Who is allowed to enter?
│
├── Files
│   └── Who can read/change them?
│
├── Processes
│   └── What programs are running?
│
├── Services
│   └── What background programs should run?
│
├── Storage
│   └── Where is data stored?
│
├── Memory
│   └── How much working space is available?
│
├── Network
│   └── How does the server communicate?
│
├── Logs
│   └── What happened?
│
├── Kernel
│   └── What controls the hardware?
│
└── Security
    └── Who is allowed to do what?
```

A good administrator learns to connect these pieces.

---

# 3. System Identification

Before troubleshooting a machine, first identify what you are working with.

## 3.1 Hostname

```bash
hostname
```

Example:

```text
smarty
```

Your machine's hostname is:

```text
smarty
```

A hostname identifies a computer on a network.

---

## 3.2 Detailed Host Information

```bash
hostnamectl
```

Representative output:

```text
 Static hostname: smarty
       Icon name: computer-laptop
         Chassis: laptop
      Machine ID: ...
         Boot ID: ...
Operating System: Zorin OS 18.1
          Kernel: Linux 7.0.0-29-generic
    Architecture: x86-64
```

### Why is this useful?

When troubleshooting a server, you need to know:

* hostname
* operating system
* kernel version
* architecture

For example, a solution for Ubuntu 24.04 may not be identical to one for an older distribution.

---

# 4. Kernel Information

The **kernel** is the core of Linux.

A simple mental model:

```text
Applications
     ↓
Libraries / system calls
     ↓
Linux Kernel
     ↓
Hardware
```

The kernel manages:

* CPU
* memory
* processes
* devices
* networking
* filesystems
* security mechanisms

---

## 4.1 Check Kernel Version

```bash
uname -r
```

Representative result:

```text
7.0.0-29-generic
```

This tells us the running kernel release.

---

## 4.2 More Kernel Information

```bash
uname -a
```

Representative output:

```text
Linux smarty 7.0.0-29-generic #... x86_64 GNU/Linux
```

Useful when diagnosing:

* driver problems
* kernel bugs
* compatibility issues
* hardware problems

---

# 5. CPU Administration

A Linux administrator needs to know how much CPU is available.

## 5.1 CPU Information

```bash
lscpu
```

Representative output:

```text
Architecture:             x86_64
CPU(s):                   4
Thread(s) per core:       2
Core(s) per socket:       2
Vendor ID:                GenuineIntel
Model name:               Intel(R) Core(TM) i5
```

The exact output depends on the machine.

---

## 5.2 What Does CPU Count Mean?

Suppose:

```text
CPU(s): 4
```

Think of it as four logical workers:

```text
CPU 0
CPU 1
CPU 2
CPU 3
```

Linux can schedule processes across them.

---

# 6. Memory Administration

RAM is temporary working space.

Check memory:

```bash
free -h
```

Representative output:

```text
               total        used        free      shared  buff/cache   available
Mem:            7.6Gi       3.2Gi       1.1Gi       420Mi       3.3Gi       4.0Gi
Swap:           2.0Gi       0B          2.0Gi
```

## Important columns

### total

Total RAM.

### used

Memory currently being used.

### free

Completely unused memory.

### buff/cache

Memory Linux is using for caches and buffers.

### available

A very important value.

It estimates how much memory can be made available to applications without serious memory pressure.

---

# 7. Free RAM Does Not Mean "Unused RAM"

A common beginner misunderstanding is:

> "Linux is using lots of RAM, so something is wrong."

Not necessarily.

Linux intentionally uses unused RAM for caching.

Think of RAM like a desk.

```text
Empty desk
   ↓
You could use it

Linux:
"Let's temporarily put useful things here."
```

If an application needs the space, Linux can reclaim much of the cache.

Therefore:

```text
free
```

is not the only value you should look at.

`available` is usually more useful for judging memory pressure.

---

# 8. Swap

Swap is disk space used as additional virtual memory.

Check:

```bash
swapon --show
```

Representative output:

```text
NAME      TYPE      SIZE USED PRIO
/swapfile file        2G   0B   -2
```

Another command:

```bash
free -h
```

might show:

```text
Swap:          2.0Gi          0B       2.0Gi
```

## RAM vs Swap

```text
RAM
↓
Fast
↓
Used directly by applications

Swap
↓
Disk-backed
↓
Much slower
```

Swap can help prevent immediate failure when memory becomes tight, but it is **not a replacement for adequate RAM**.

---

# 9. Disk Space vs Directory Space

Two commands that administrators must know:

```bash
df -h
du -sh DIRECTORY
```

They answer different questions.

---

## 9.1 `df`

```bash
df -h
```

Example:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       476G  120G  332G  27% /
```

`df` asks:

> "How much space is available on the filesystem?"

---

## 9.2 `du`

```bash
du -sh ~
```

Example:

```text
18G     /home/pri
```

`du` asks:

> "How much space is being consumed by this directory?"

---

## Important Difference

```text
df
 ↓
filesystem-level usage

du
 ↓
directory/file usage
```

This distinction is extremely useful during disk troubleshooting.

---

# 10. Finding Large Files

Suppose:

```text
df -h
```

says:

```text
Use% = 95%
```

We need to discover what is consuming the space.

A useful command:

```bash
sudo du -xh /var | sort -h | tail
```

Representative output:

```text
850M    /var/cache
1.2G    /var/lib
3.4G    /var/log
```

Now we know where to investigate.

Another useful command:

```bash
du -sh ~/* 2>/dev/null | sort -h
```

---

# 11. Linux Filesystem Hierarchy

The Linux filesystem starts at:

```text
/
```

This is called the **root directory**.

Important directories:

```text
/
├── boot
├── dev
├── etc
├── home
├── lib
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── srv
├── sys
├── tmp
├── usr
└── var
```

---

# 12. `/etc`

`/etc` contains system configuration.

Examples:

```text
/etc/passwd
/etc/group
/etc/fstab
/etc/ssh/
/etc/systemd/
```

Think:

```text
/etc
 ↓
System configuration
```

If you need to understand how a service is configured, `/etc` is often a place to investigate.

---

# 13. `/var`

`/var` contains data that changes frequently.

Important:

```text
/var/log
/var/cache
/var/lib
```

For example:

```text
/var/log
```

contains logs.

You already examined this directory and found:

```text
syslog
auth.log
kern.log
dpkg.log
boot.log
```

---

# 14. `/home`

Normal users' home directories live here.

Example:

```text
/home/pri
```

Your shell variables confirmed:

```bash
echo "$HOME"
```

Output:

```text
/home/pri
```

---

# 15. `/root`

This is the home directory of the root user.

It is **not** the same thing as:

```text
/
```

Remember:

```text
/       = filesystem root
/root   = root user's home directory
```

---

# 16. `/tmp`

Temporary files are stored here.

Example:

```bash
ls -ld /tmp
```

Representative:

```text
drwxrwxrwt ... /tmp
```

Notice the final:

```text
t
```

That is the **Sticky Bit**.

You already studied the Sticky Bit in your permissions/security module.

Its purpose on `/tmp` is to prevent normal users from deleting other users' files there.

---

# 17. `/proc`

`/proc` is a virtual filesystem.

It does not behave like a normal disk directory.

It exposes information about:

* processes
* kernel
* CPU
* memory
* system state

Example:

```bash
cat /proc/cpuinfo
```

Example:

```text
processor : 0
vendor_id : GenuineIntel
...
```

Check memory:

```bash
cat /proc/meminfo
```

You can think of `/proc` as:

> "Linux exposing information about itself as files."

---

# 18. `/sys`

`/sys` is another virtual filesystem.

It exposes information about:

* devices
* drivers
* kernel objects
* hardware relationships

Example:

```bash
ls /sys
```

Typical directories:

```text
block
bus
class
devices
firmware
kernel
module
```

---

# 19. `/dev`

`/dev` contains device files.

Examples can include:

```text
/dev/null
/dev/zero
/dev/random
/dev/sda
/dev/nvme0n1
```

This is one reason Linux follows the philosophy:

> "Many things can be represented through files."

---

# 20. Storage Devices

List block devices:

```bash
lsblk
```

Representative:

```text
NAME        SIZE TYPE MOUNTPOINTS
sda         477G disk
├─sda1      512M part /boot/efi
└─sda2      476G part /
```

Your actual device names may differ.

Possible names:

```text
/dev/sda
/dev/sdb
/dev/nvme0n1
```

---

# 21. Partition vs Filesystem

These are different concepts.

Imagine a cupboard.

```text
Disk
 ↓
Partition
 ↓
Filesystem
 ↓
Files
```

A partition is a region of the disk.

A filesystem is the structure used to store files there.

For example:

```text
/dev/sda2
   ↓
ext4 filesystem
   ↓
mounted at /
```

---

# 22. Filesystem Type

Use:

```bash
lsblk -f
```

Example:

```text
NAME   FSTYPE FSVER LABEL UUID                                 MOUNTPOINTS
sda1   vfat   FAT32       ABCD-1234                            /boot/efi
sda2   ext4   1.0         1234-abcd-5678                       /
```

Common filesystem:

```text
ext4
```

---

# 23. UUID

Every filesystem can have a UUID.

Check:

```bash
blkid
```

Representative:

```text
/dev/sda2: UUID="1234-abcd..." TYPE="ext4"
```

UUID means:

> Universally Unique Identifier.

Why useful?

Device names can change.

UUID provides a more persistent identity for a filesystem.

---

# 24. Mount Points

A filesystem becomes accessible through a directory called a **mount point**.

Think:

```text
USB filesystem
      ↓
mount
      ↓
/mnt/usb
```

Then:

```text
/mnt/usb/file.txt
```

can access the filesystem.

---

# 25. See Mounted Filesystems

Use:

```bash
findmnt
```

Example:

```text
TARGET
/
├─ /boot/efi
├─ /run
├─ /proc
├─ /sys
└─ /tmp
```

For the root filesystem:

```bash
findmnt /
```

Representative:

```text
TARGET SOURCE    FSTYPE OPTIONS
/      /dev/sda2 ext4   rw,relatime
```

---

# 26. `/etc/fstab`

`/etc/fstab` controls persistent filesystem mounting.

View it:

```bash
cat /etc/fstab
```

Representative:

```text
# /etc/fstab
UUID=1234-abcd  /  ext4  defaults  0  1
UUID=ABCD-1234  /boot/efi  vfat  defaults  0  1
```

A simplified way to understand the fields:

```text
DEVICE/UUID
     ↓
MOUNT POINT
     ↓
FILESYSTEM TYPE
     ↓
OPTIONS
     ↓
DUMP
     ↓
FSCK ORDER
```

---

# 27. Why `/etc/fstab` Matters

Suppose you attach another disk:

```text
/dev/sdb1
```

You mount it manually:

```bash
sudo mount /dev/sdb1 /data
```

After reboot, the mount may disappear unless it is configured for persistent mounting.

That's where:

```text
/etc/fstab
```

comes in.

---

# 28. Safely Testing `fstab`

After changing `/etc/fstab`, do not immediately reboot.

First test:

```bash
sudo mount -a
```

Meaning:

> Mount all filesystems from `/etc/fstab` that are not already mounted.

If there is a mistake, you can detect it before rebooting.

This is an important administrator habit.

---

# 29. Inodes

A file needs more than disk blocks.

Linux filesystems also use **inodes**.

An inode stores metadata such as:

* ownership
* permissions
* timestamps
* file size
* file information

Check inode usage:

```bash
df -i
```

Example:

```text
Filesystem      Inodes   IUsed   IFree IUse% Mounted on
/dev/sda2      32000000 500000 31500000    2% /
```

---

# 30. Why Inodes Matter

Imagine a server has:

```text
10 GB free disk space
```

but:

```text
0 free inodes
```

The server may still be unable to create new files.

This can happen when applications create millions of tiny files.

Therefore:

```text
Disk capacity problem
≠
Always a filesystem inode problem
```

Administrators should check both:

```bash
df -h
df -i
```

---

# 31. Boot Process

When you press the power button, Linux does not immediately start your desktop.

A simplified boot process:

```text
Power On
   ↓
BIOS / UEFI
   ↓
Bootloader
   ↓
Linux Kernel
   ↓
initramfs
   ↓
systemd
   ↓
services
   ↓
login / graphical desktop
```

---

# 32. BIOS / UEFI

Firmware initializes hardware and finds something bootable.

Modern systems commonly use:

```text
UEFI
```

rather than traditional BIOS.

---

# 33. Bootloader

The bootloader loads the Linux kernel.

On many Linux systems:

```text
GRUB
```

is used.

Conceptually:

```text
UEFI
 ↓
GRUB
 ↓
Linux kernel
```

---

# 34. Kernel

The kernel is loaded into memory.

It initializes:

* CPU
* memory management
* devices
* drivers
* core system functions

---

# 35. initramfs

`initramfs` is a temporary early userspace environment used during boot.

It helps the kernel:

* find the root filesystem
* load required drivers
* prepare the system for switching to the real root filesystem

Think of it as:

> A small temporary toolbox used before the real system is fully available.

---

# 36. systemd — PID 1

After the kernel and early userspace, systemd becomes the first major userspace process.

Check:

```bash
ps -p 1 -o pid,comm,args
```

Representative:

```text
PID COMMAND COMMAND
1   systemd /sbin/init
```

The most important fact:

```text
PID 1
```

is the ancestor of userspace processes.

---

# 37. Default systemd Target

Check:

```bash
systemctl get-default
```

Representative:

```text
graphical.target
```

This means the system normally boots into a graphical environment.

Another common target:

```text
multi-user.target
```

which represents a non-graphical multi-user system with services running.

---

# 38. systemd Target Mental Model

Think of targets as destinations.

```text
graphical.target
       ↓
GUI + services

multi-user.target
       ↓
services + users
```

You do not normally need to memorize every target.

The important concept is:

> systemd uses targets to organize system states.

---

# 39. Kernel Modules

Linux can load pieces of kernel functionality as modules.

View loaded modules:

```bash
lsmod
```

Representative:

```text
Module                  Size  Used by
bluetooth              ...
snd_hda_intel          ...
i915                   ...
```

---

# 40. Module Information

For a module:

```bash
modinfo MODULE_NAME
```

Example:

```bash
modinfo loop
```

Output contains information such as:

```text
filename:
description:
author:
license:
```

---

# 41. Loading a Module

```bash
sudo modprobe MODULE_NAME
```

`modprobe` asks the kernel to load a module and its dependencies.

Remove:

```bash
sudo modprobe -r MODULE_NAME
```

Do not randomly remove hardware-related modules from a running machine.

---

# 42. Hardware Inspection

Useful administrator commands:

```bash
lspci
```

PCI devices.

```bash
lsusb
```

USB devices.

```bash
lscpu
```

CPU.

```bash
lsmem
```

Memory.

```bash
lsblk
```

Storage.

---

# 43. Practical Hardware Inspection

Run:

```bash
lspci | head
```

Representative:

```text
00:00.0 Host bridge: Intel Corporation ...
00:02.0 VGA compatible controller: Intel Corporation ...
00:14.0 USB controller: Intel Corporation ...
```

Then:

```bash
lsusb
```

Representative:

```text
Bus 001 Device 002: ID xxxx:xxxx ...
Bus 001 Device 003: ID xxxx:xxxx ...
```

These commands are useful when troubleshooting hardware.

---

# 44. Resource Monitoring

A Linux administrator should continuously understand:

```text
CPU
RAM
Disk
Processes
Network
```

One important command is:

```bash
top
```

It provides a live view of:

* processes
* CPU
* memory
* load
* process IDs

Exit:

```text
q
```

You already practiced `top`/`htop` in your process-management notes, so this section is about how administrators use the information.

---

# 45. Load Average

`top` may show:

```text
load average: 0.50, 0.40, 0.30
```

These represent approximately:

```text
1 minute
5 minutes
15 minutes
```

Load average is not simply "CPU percentage."

It represents the amount of work competing for CPU and certain other system resources.

A high load on a machine with many CPUs means something different from the same load on a machine with one CPU.

---

# 46. Virtual Memory Statistics

Another useful command:

```bash
vmstat
```

Example:

```text
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa
 1  0      0  ...    ...    ...      0    0    ...   ...  ...  ...  5  2 93  0
```

It gives a broad picture of:

* processes
* memory
* swap
* I/O
* system activity
* CPU

---

# 47. Disk I/O

A system can have plenty of free disk space but still be slow because of disk I/O.

A commonly used tool is:

```bash
iostat
```

If not installed, it commonly comes from:

```text
sysstat
```

On Ubuntu/Zorin:

```bash
sudo apt install sysstat
```

Then:

```bash
iostat
```

The important idea:

```text
Disk capacity
≠
Disk performance
```

---

# 48. Linux Administration Troubleshooting Principle

When a server is slow, do not immediately guess.

Check:

```text
CPU?
RAM?
Swap?
Disk space?
Disk I/O?
Processes?
Logs?
Network?
```

This is the difference between:

```text
Guessing
```

and:

```text
Troubleshooting
```

---

# 49. Part 1 Completion Checklist

By completing this part, the following administration areas are covered:

* [x] System identification
* [x] Hostname
* [x] OS information
* [x] Kernel version
* [x] CPU information
* [x] Memory
* [x] Swap
* [x] Filesystem hierarchy
* [x] `/etc`
* [x] `/var`
* [x] `/home`
* [x] `/root`
* [x] `/tmp`
* [x] `/proc`
* [x] `/sys`
* [x] `/dev`
* [x] Block devices
* [x] Partitions
* [x] Filesystems
* [x] UUID
* [x] Mount points
* [x] `/etc/fstab`
* [x] Inodes
* [x] Boot process
* [x] BIOS/UEFI
* [x] Bootloader
* [x] Kernel
* [x] initramfs
* [x] systemd as PID 1
* [x] systemd targets
* [x] Kernel modules
* [x] Hardware inspection
* [x] Resource monitoring
* [x] Load average
* [x] Virtual memory
* [x] Disk I/O

---

# Part 1 Mental Model

```text
                  Linux Machine
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      CPU             RAM           Storage
        │              │              │
      lscpu          free          lsblk
      top            vmstat        df
                     swap          du
                                    │
                                 filesystem
                                    │
                                 mount
                                    │
                                  /etc/fstab
                       │
                       ↓
                    Kernel
                       │
                 systemd / PID 1
                       │
                 services/processes
```

The important lesson is not to memorize commands independently.

Understand what each command is looking at.

---

# Part 1 Practical Record

The practical commands covered in this part include:

```bash
hostname
hostnamectl
uname -r
uname -a
lscpu
free -h
swapon --show
df -h
df -i
du -sh
lsblk
lsblk -f
blkid
findmnt
cat /etc/fstab
sudo mount -a
ps -p 1 -o pid,comm,args
systemctl get-default
lsmod
modinfo
lspci
lsusb
vmstat
iostat
```

Representative administrator findings:

```text
Hostname: smarty
OS: Zorin OS 18.1
Kernel: 7.0.0-29-generic
Architecture: x86_64
PID 1: systemd
Root filesystem: ext4
Boot filesystem: EFI/FAT32
```

Exact hardware, disk sizes, UUIDs, memory amounts, and module lists naturally depend on the machine.

---

# Part 1 Key Takeaways

1. Linux administration is about managing the whole system, not memorizing commands.
2. `hostnamectl` identifies the machine and OS.
3. `uname` identifies the kernel.
4. `lscpu` describes CPU resources.
5. `free -h` helps understand RAM and swap.
6. `df` shows filesystem space.
7. `du` shows directory/file usage.
8. `lsblk` shows storage devices and partitions.
9. `findmnt` shows mounted filesystems.
10. `/etc/fstab` controls persistent mounts.
11. UUIDs provide stable filesystem identification.
12. Inodes are separate from disk capacity.
13. Linux booting goes through firmware → bootloader → kernel → initramfs → systemd.
14. systemd normally becomes PID 1.
15. `/proc` and `/sys` expose kernel/system information.
16. Kernel modules provide loadable kernel functionality.
17. Hardware troubleshooting uses tools such as `lspci`, `lsusb`, and `lsblk`.
18. Administrators investigate CPU, memory, storage, I/O, processes, logs, and network instead of guessing.

---

# End of Part 1
