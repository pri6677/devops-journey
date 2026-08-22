# Linux Administration — Part 2

> **Purpose:** Finish the remaining Linux Administration concepts and build a professional troubleshooting mindset.
>
> **Practical mode:** Commands below include representative results so the notes document the practical work even when the commands are performed later.

---

# 1. Administrator Configuration Files

Linux stores many configuration files under:

```text
/etc
```

Some important files:

```text
/etc/passwd
/etc/group
/etc/shadow
/etc/sudoers
/etc/fstab
/etc/hosts
/etc/hostname
/etc/ssh/
/etc/systemd/
```

You have already worked with users/groups, permissions, SSH, and `fstab`.

The important administrator habit is:

> Before changing a configuration file, understand what the file controls and make a backup when appropriate.

---

# 2. Shell Configuration

Your Bash configuration is commonly stored in:

```text
~/.bashrc
```

View it:

```bash
cat ~/.bashrc
```

Your existing Bash work included aliases and functions such as:

```bash
alias ll='ls -la'
```

and functions.

---

# 3. Reloading `.bashrc`

After modifying `.bashrc`, the current shell does not automatically reread the file.

Use:

```bash
source ~/.bashrc
```

or:

```bash
. ~/.bashrc
```

Example:

```bash
source ~/.bashrc
```

No output normally means the file was loaded successfully.

Then:

```bash
type ll
```

might show:

```text
ll is aliased to `ls -la'
```

---

# 4. Environment Variables

Check:

```bash
printenv
```

Or specific variables:

```bash
echo "$USER"
echo "$HOME"
echo "$SHELL"
echo "$PATH"
echo "$PWD"
echo "$HOSTNAME"
```

Example:

```text
pri
/home/pri
/bin/bash
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
/home/pri
smarty
```

Environment variables are important because applications inherit them from their parent processes.

---

# 5. PATH

`PATH` tells the shell where to look for executable commands.

Example:

```bash
echo "$PATH"
```

Possible:

```text
/usr/local/bin:/usr/bin:/bin
```

The colon:

```text
:
```

separates directories.

When you type:

```bash
python3
```

Bash searches directories in `PATH`.

This connects directly to your earlier practical:

```bash
command -v python3
```

which returned:

```text
/usr/bin/python3
```

---

# 6. Resource Limits

Linux can limit what processes/users can consume.

Check:

```bash
ulimit -a
```

Representative output:

```text
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
open files              (-n) 1024
max user processes      (-u) 7815
stack size              (kbytes, -s) 8192
```

Exact values depend on the system.

---

# 7. Why Resource Limits Matter

Imagine an application opens files repeatedly.

Eventually it may report:

```text
Too many open files
```

The application might not be broken.

The operating system may simply be enforcing its file-descriptor limit.

This is why administrators must understand:

```text
application
   ↓
process
   ↓
resource limit
   ↓
kernel
```

---

# 8. File Descriptors

Linux processes use file descriptors to interact with files and streams.

The three standard descriptors are:

```text
0 → stdin
1 → stdout
2 → stderr
```

You already used these concepts in Bash.

Example:

```bash
command > output.txt
```

means:

```text
stdout → output.txt
```

And:

```bash
command 2> error.txt
```

means:

```text
stderr → error.txt
```

---

# 9. Signals

A signal is a message sent to a process.

Common signals:

| Signal  | Number | Meaning             |
| ------- | -----: | ------------------- |
| SIGHUP  |      1 | Hangup              |
| SIGINT  |      2 | Interrupt           |
| SIGTERM |     15 | Request termination |
| SIGKILL |      9 | Force termination   |

---

# 10. `kill` Does Not Mean "Destroy"

This is an important correction.

When we write:

```bash
kill 1234
```

we are really saying:

> Send a signal to process 1234.

The default signal is usually:

```text
SIGTERM
```

which gives the application an opportunity to clean up.

---

# 11. SIGTERM vs SIGKILL

Preferred:

```bash
kill PID
```

Force:

```bash
kill -9 PID
```

Think:

```text
SIGTERM
"Please shut down cleanly."

        ↓

application cleans up

        ↓

exit
```

Versus:

```text
SIGKILL
"Stop immediately."
```

SIGKILL does not allow the application to perform normal cleanup.

Therefore:

> Do not automatically use `kill -9`.

Try normal termination first.

---

# 12. Scheduled Tasks — cron

Linux administrators often automate repetitive work.

Examples:

* backups
* cleanup
* reports
* monitoring
* maintenance

Traditional tool:

```text
cron
```

---

# 13. Viewing User Cron Jobs

```bash
crontab -l
```

If there are no entries:

```text
no crontab for pri
```

or it may display existing jobs.

---

# 14. Editing Cron Jobs

```bash
crontab -e
```

This opens the user's crontab.

A cron entry looks like:

```text
0 2 * * * /home/pri/backup.sh
```

---

# 15. Understanding Cron Syntax

Cron uses:

```text
minute hour day-of-month month day-of-week
```

Example:

```text
0 2 * * *
```

means:

```text
minute       = 0
hour         = 2
day           = every
month         = every
weekday       = every
```

Therefore:

> Run at 02:00 every day.

---

# 16. Another Cron Example

```text
*/5 * * * * /home/pri/check.sh
```

Means:

> Run every 5 minutes.

The `*` means "every possible value" in that field.

---

# 17. System Cron Directories

Linux also provides:

```text
/etc/cron.hourly/
/etc/cron.daily/
/etc/cron.weekly/
/etc/cron.monthly/
```

These allow administrators to organize scheduled maintenance tasks.

---

# 18. Cron vs systemd Timers

Modern Linux systems also use systemd timers.

Compare:

```text
cron
 ↓
traditional scheduling

systemd timer
 ↓
integrated with systemd
```

For modern server administration, understand both.

---

# 19. systemd Timers

List timers:

```bash
systemctl list-timers
```

Representative:

```text
NEXT                         LEFT
Sat 2026-08-22 02:00:00      20min
Sun 2026-08-23 00:00:00      1d
```

The exact timers depend on installed software.

---

# 20. Timer Mental Model

A systemd timer normally triggers a service.

```text
timer
  ↓
schedule reached
  ↓
service starts
  ↓
command/script executes
```

This is similar to:

```text
cron
  ↓
run command
```

but integrated into systemd.

---

# 21. Log Management

Linux systems produce huge amounts of logs.

You already worked with:

```text
/var/log
journalctl
```

Important principle:

> Logs tell you what happened.

For example:

```bash
journalctl -u ssh
```

can show SSH service activity.

---

# 22. Log Priority

systemd logs have priorities.

Useful:

```bash
journalctl -p err
```

This focuses on error-level messages.

Example:

```text
kernel: ACPI Error
bluetoothd: Failed operation
systemd: Failed to start service
```

Not every error means the computer is broken.

For example, your own machine showed firmware/ACPI/Bluetooth-related messages. An administrator must investigate whether an error is actually affecting functionality before attempting a fix.

---

# 23. Boot Logs

View current boot logs:

```bash
journalctl -b
```

View errors from current boot:

```bash
journalctl -b -p err
```

This is extremely useful after reboot problems.

---

# 24. Previous Boot

List boots:

```bash
journalctl --list-boots
```

Representative:

```text
-2  abc123...  Wed ...
-1  def456...  Thu ...
 0  ghi789...  Fri ...
```

The current boot is:

```text
0
```

Previous boot:

```text
-1
```

View previous boot:

```bash
journalctl -b -1
```

---

# 25. Service Logs

For SSH:

```bash
journalctl -u ssh
```

Recent entries:

```bash
journalctl -u ssh -n 20
```

Follow live logs:

```bash
journalctl -u ssh -f
```

`-f` means:

> Follow new messages as they arrive.

This is similar to:

```bash
tail -f
```

---

# 26. SSH Socket Activation

Your system gave an excellent real-world example.

You ran:

```bash
systemctl status ssh
```

and saw:

```text
Active: inactive (dead)
TriggeredBy: ssh.socket
```

Then:

```bash
systemctl status ssh.socket
```

showed:

```text
Active: active (listening)
Listen: 0.0.0.0:22
        [::]:22
Triggers: ssh.service
```

This means SSH is using **socket activation**.

---

# 27. What Is Socket Activation?

Instead of keeping the service process running all the time:

```text
ssh.service
    ↓
always running
```

systemd can keep the socket listening:

```text
ssh.socket
    ↓
listens on port 22
    ↓
connection arrives
    ↓
ssh.service starts
```

Mental model:

```text
Client
  │
  │ TCP connection
  ↓
Port 22
  │
  ↓
ssh.socket
  │
  ↓
ssh.service
  │
  ↓
sshd
```

This explains why:

```text
ssh.service = inactive
```

does **not necessarily mean SSH is unavailable**.

Your subsequent test proved it:

```bash
ssh localhost
```

successfully connected.

---

# 28. Verify Listening Ports

Use:

```bash
ss -tlnp
```

Your actual result showed:

```text
LISTEN 0 4096 0.0.0.0:22  0.0.0.0:*
LISTEN 0 4096 [::]:22     [::]:*
```

Therefore SSH was listening on:

```text
IPv4 port 22
IPv6 port 22
```

This is a perfect example of Linux administration troubleshooting.

---

# 29. Understand `0.0.0.0`

When a service listens on:

```text
0.0.0.0:22
```

it means it is listening on all IPv4 interfaces.

It does **not** mean that `0.0.0.0` is a remote machine.

Similarly:

```text
[::]:22
```

represents listening on IPv6 addresses.

---

# 30. Localhost

You tested:

```bash
ssh localhost
```

`localhost` refers to the current machine.

Usually:

```text
127.0.0.1
```

for IPv4.

Your test:

```text
ssh localhost
```

successfully logged in as:

```text
pri
```

This proves several things simultaneously:

```text
SSH client works
      ↓
SSH server is reachable locally
      ↓
port 22 is listening
      ↓
authentication works
      ↓
shell session starts
```

This is exactly how administrators should think about tests.

---

# 31. Basic Linux Networking Tools

Networking fundamentals will be studied later as a separate roadmap section.

For Linux Administration, however, you should know these tools:

```bash
ip addr
ip route
ss
ping
hostname -I
```

---

# 32. IP Addresses

```bash
ip addr
```

shows interfaces and addresses.

Example:

```text
inet 192.168.1.20/24
```

This tells us:

```text
IP address = 192.168.1.20
```

Networking theory will come later.

For now, the administrator's question is:

> Does this machine have the expected address?

---

# 33. Routing

```bash
ip route
```

Representative:

```text
default via 192.168.1.1 dev wlan0
192.168.1.0/24 dev wlan0 proto kernel scope link
```

The important idea:

```text
IP address
   +
routing table
   ↓
where packets go
```

---

# 34. Connectivity Test

```bash
ping -c 4 127.0.0.1
```

Representative:

```text
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.028 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.031 ms
...
4 packets transmitted, 4 received, 0% packet loss
```

This tests the local network stack.

It does not prove that the internet is working.

---

# 35. DNS Resolution

Check name resolution:

```bash
getent hosts example.com
```

Representative:

```text
93.184.216.34 example.com
```

This asks the system's configured name-resolution mechanism to resolve the hostname.

---

# 36. DNS Troubleshooting Mindset

If:

```bash
ping 8.8.8.8
```

works but:

```bash
ping example.com
```

doesn't,

one possible problem is DNS.

Conceptually:

```text
Can reach IP?
      ↓
YES

Can resolve hostname?
      ↓
NO

Investigate DNS
```

Networking theory will be covered later.

---

# 37. Firewall Administration

A firewall controls network traffic.

On Ubuntu/Zorin, a common command-line frontend is:

```bash
ufw
```

Check status:

```bash
sudo ufw status
```

Representative:

```text
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
```

---

# 38. Allowing SSH

Example:

```bash
sudo ufw allow 22/tcp
```

This creates a rule allowing TCP traffic to port 22.

---

# 39. Removing a Firewall Rule

```bash
sudo ufw delete allow 22/tcp
```

Always be careful when modifying firewall rules on remote machines.

A wrong rule can lock you out.

---

# 40. Backup Concepts

A Linux administrator must understand backups.

A backup is:

> A recoverable copy of important data.

Important distinction:

```text
Archive
≠
Backup
```

An archive packages files.

A backup is part of a recovery strategy.

---

# 41. tar

Create a compressed archive:

```bash
tar -czf backup.tar.gz important/
```

Meaning:

```text
-c  create
-z  gzip compression
-f  filename
```

Extract:

```bash
tar -xzf backup.tar.gz
```

Meaning:

```text
-x  extract
-z  gzip
-f  filename
```

---

# 42. Verify an Archive

List contents without extracting:

```bash
tar -tzf backup.tar.gz
```

Representative:

```text
important/
important/config.txt
important/data.txt
```

This is useful before restoring.

---

# 43. rsync

`rsync` synchronizes files/directories.

Example:

```bash
rsync -av source/ destination/
```

`-a`:

```text
archive mode
```

`-v`:

```text
verbose
```

Conceptually:

```text
Source
  │
  │ rsync
  ↓
Destination
```

It is especially useful because it can transfer only changed data instead of blindly copying everything every time.

---

# 44. Backup Verification

A backup is not truly useful if you have never tested restoration.

Professional principle:

```text
Backup
  ↓
Test restore
  ↓
Verify data
```

A file called:

```text
backup.tar.gz
```

does not automatically mean:

> "My data is safe."

---

# 45. Log Rotation

Logs can grow forever if unmanaged.

Linux commonly uses:

```text
logrotate
```

Configuration:

```text
/etc/logrotate.conf
/etc/logrotate.d/
```

You already saw rotated logs such as:

```text
syslog
syslog.1
syslog.2.gz
syslog.3.gz
```

This means:

```text
current log
   ↓
rotation
   ↓
old log
   ↓
compression
   ↓
eventual deletion
```

---

# 46. Why Log Rotation Matters

Imagine:

```text
application.log
```

grows by:

```text
1 GB/day
```

Without rotation:

```text
1 day → 1 GB
10 days → 10 GB
100 days → 100 GB
```

Eventually the filesystem may fill.

Log management is therefore also a **storage management problem**.

---

# 47. Users and Account State

You already practiced users and groups extensively.

Useful commands:

```bash
id USER
getent passwd USER
getent group GROUP
passwd -S USER
```

Your `tester` example showed:

```text
tester L 2026-08-08 0 99999 7 -1
```

The important point:

```text
L
```

means the account's password is locked.

---

# 48. Account vs Home Directory

You discovered something important:

```bash
getent passwd tester
```

returned:

```text
tester:x:1001:1002::/home/tester:/bin/sh
```

but:

```bash
ls -ld /home/tester
```

returned:

```text
No such file or directory
```

This teaches an important administrator lesson:

> An account entry can exist even when its home directory does not currently exist.

Linux account metadata and actual filesystem directories are related but not identical.

---

# 49. Shells and `nologin`

System accounts may have shells such as:

```text
/usr/sbin/nologin
```

or:

```text
/bin/false
```

Example:

```bash
getent passwd sshd
```

might show:

```text
sshd:x:122:65534::/run/sshd:/usr/sbin/nologin
```

This means the account is not intended for normal interactive login.

This is an important security concept:

```text
Service account
      ↓
Run service
      ↓
No interactive login
```

---

# 50. `sudo` and Least Privilege

You already learned `sudo`.

The professional principle behind it is:

> Give users only the privileges they need.

This is called:

```text
Least Privilege
```

Instead of:

```text
Everything → root
```

prefer:

```text
Normal user
   ↓
sudo
   ↓
specific administrative action
```

---

# 51. Root vs sudo

Root:

```text
UID 0
```

Check:

```bash
id root
```

Representative:

```text
uid=0(root) gid=0(root) groups=0(root)
```

A normal user may temporarily execute a command with root privileges:

```bash
sudo command
```

This is safer operationally than doing all work inside a permanent root shell.

---

# 52. Linux Administration Troubleshooting Workflow

This is one of the most important sections.

Suppose:

> "The application is not working."

Do **not** immediately restart everything.

Use a structured process.

---

## Step 1 — Is the machine alive?

```bash
uptime
```

Example:

```text
10:00:00 up 2 days, 4:31, 1 user, load average: 0.20, 0.15, 0.10
```

---

## Step 2 — Is the service running?

```bash
systemctl status SERVICE
```

Example:

```text
Active: active (running)
```

or:

```text
Active: inactive (dead)
```

---

## Step 3 — Is the process running?

```bash
pgrep SERVICE
```

or:

```bash
ps aux | grep SERVICE
```

---

## Step 4 — Is the expected port listening?

```bash
ss -ltnp
```

Example:

```text
LISTEN 0 4096 0.0.0.0:8080
```

---

## Step 5 — What do the logs say?

```bash
journalctl -u SERVICE -n 50
```

Look for:

```text
ERROR
FAILED
TIMEOUT
PERMISSION
CONNECTION
```

---

## Step 6 — Is the disk full?

```bash
df -h
```

---

## Step 7 — Is memory exhausted?

```bash
free -h
```

---

## Step 8 — Is CPU overloaded?

```bash
top
```

---

## Step 9 — Is networking working?

```bash
ip addr
ip route
ping -c 4 TARGET
```

---

# 53. Complete Troubleshooting Flow

```text
             APPLICATION PROBLEM
                     │
                     ↓
             Is machine alive?
                     │
                     ↓
             Is service running?
                     │
                     ↓
             Is process running?
                     │
                     ↓
             Is port listening?
                     │
                     ↓
                Check logs
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
        CPU         RAM        Disk
          │          │          │
          └──────────┼──────────┘
                     ↓
                  Network
                     │
                     ↓
                Find root cause
                     │
                     ↓
                  Fix it
                     │
                     ↓
                 Verify it
```

---

# 54. Never Stop at "It Works"

Suppose you restart a service:

```bash
sudo systemctl restart nginx
```

and it starts.

Don't immediately declare victory.

Verify:

```bash
systemctl is-active nginx
```

Then:

```bash
ss -ltnp
```

Then:

```bash
curl localhost
```

Then:

```bash
journalctl -u nginx -n 20
```

The administrator's job is:

```text
Change
 ↓
Verify
 ↓
Confirm
```

---

# 55. Practical Example — SSH Troubleshooting

Your own system provided a perfect example.

You checked:

```bash
systemctl status ssh
```

and saw:

```text
Active: inactive (dead)
TriggeredBy: ssh.socket
```

A beginner might conclude:

> SSH is broken.

But you investigated further.

You checked:

```bash
systemctl status ssh.socket
```

and found:

```text
Active: active (listening)
Listen: 0.0.0.0:22
        [::]:22
```

Then:

```bash
ss -tlnp
```

confirmed:

```text
0.0.0.0:22
[::]:22
```

Finally:

```bash
ssh localhost
```

successfully connected.

Conclusion:

```text
ssh.service inactive
       +
ssh.socket active
       ↓
socket activation
       ↓
SSH is available
```

This is exactly the kind of reasoning expected from a Linux administrator.

---

# 56. Common Administrator Mistakes

## Mistake 1 — Using `kill -9` immediately

Better:

```bash
kill PID
```

Only force when necessary:

```bash
kill -9 PID
```

---

## Mistake 2 — Rebooting without investigation

Bad troubleshooting:

```text
Problem
 ↓
reboot
 ↓
hope
```

Better:

```text
Problem
 ↓
logs
 ↓
service
 ↓
process
 ↓
resources
 ↓
network
 ↓
root cause
```

---

## Mistake 3 — Confusing `df` and `du`

Remember:

```text
df = filesystem
du = files/directories
```

---

## Mistake 4 — Editing `/etc/fstab` and immediately rebooting

Safer:

```bash
sudo mount -a
```

first.

---

## Mistake 5 — Treating every log error as catastrophic

A log line containing:

```text
ERROR
```

doesn't automatically mean:

```text
system is broken
```

Investigate:

```text
When did it happen?
How often?
What component?
Does functionality fail?
Is there an impact?
```

---

## Mistake 6 — Running everything as root

Use:

```bash
sudo command
```

when administrative privileges are actually required.

---

## Mistake 7 — Deleting files to solve disk problems without investigation

First:

```bash
df -h
du -sh
```

Then identify the cause.

Never blindly delete:

```text
/var/*
/etc/*
/usr/*
```

---

# 57. Important Administrator Commands

## System

```bash
hostnamectl
uname -a
uptime
```

## CPU/RAM

```bash
lscpu
free -h
vmstat
top
```

## Storage

```bash
lsblk
lsblk -f
df -h
df -i
du -sh
blkid
findmnt
```

## Boot/kernel

```bash
uname -r
ps -p 1 -o pid,comm,args
lsmod
modinfo
```

## Services

```bash
systemctl status SERVICE
systemctl start SERVICE
systemctl stop SERVICE
systemctl restart SERVICE
systemctl enable SERVICE
systemctl disable SERVICE
systemctl is-active SERVICE
systemctl is-enabled SERVICE
```

## Logs

```bash
journalctl
journalctl -b
journalctl -b -p err
journalctl -u SERVICE
journalctl -u SERVICE -n 20
journalctl -u SERVICE -f
```

## Users

```bash
whoami
id
groups
getent passwd USER
getent group GROUP
passwd -S USER
```

## Networking tools

```bash
ip addr
ip route
ss -tlnp
ping
getent hosts
```

## Scheduling

```bash
crontab -l
crontab -e
systemctl list-timers
```

## Backup

```bash
tar
rsync
```

## Hardware

```bash
lspci
lsusb
lsblk
```

---

# 58. Administration Decision Tree

When something breaks:

```text
                    PROBLEM
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
         SYSTEM?              APPLICATION?
             │                   │
      ┌──────┼──────┐            ↓
      ↓      ↓      ↓        SERVICE?
     CPU    RAM    DISK          │
      │      │      │            ↓
      └──────┼──────┘        PROCESS?
             │                   │
             ↓                   ↓
          LOGS ←────────────── PORT?
             │                   │
             └─────────┬─────────┘
                       ↓
                    NETWORK
                       │
                       ↓
                  ROOT CAUSE
                       │
                       ↓
                     FIX
                       │
                       ↓
                   VERIFY
```

This is the mental model to carry into DevOps.

---

# 59. Linux Administration and DevOps

Everything we learned here appears later in DevOps.

## AWS

You will manage Linux EC2 instances.

You will need:

```bash
systemctl
journalctl
ss
df
free
ps
```

---

## Docker

Containers use Linux processes, namespaces, cgroups, filesystems, and networking.

Understanding Linux makes Docker much easier.

---

## Kubernetes

Kubernetes nodes run Linux.

You will troubleshoot:

```text
processes
CPU
memory
networking
storage
logs
services
```

---

## CI/CD

Build agents and runners execute Linux commands.

You will need:

```bash
bash
permissions
processes
environment variables
exit codes
logs
```

---

## Monitoring

Monitoring systems measure:

```text
CPU
RAM
disk
network
processes
services
```

Everything starts with Linux fundamentals.

---

# 60. Complete Linux Administration Checklist

## System

* [x] Hostname
* [x] OS information
* [x] Kernel information
* [x] CPU
* [x] RAM
* [x] Swap
* [x] Load average
* [x] Resource monitoring

## Storage

* [x] Block devices
* [x] Partitions
* [x] Filesystems
* [x] ext4
* [x] Mount points
* [x] UUID
* [x] `/etc/fstab`
* [x] `df`
* [x] `du`
* [x] Inodes
* [x] Disk I/O

## Filesystem hierarchy

* [x] `/`
* [x] `/etc`
* [x] `/var`
* [x] `/home`
* [x] `/root`
* [x] `/tmp`
* [x] `/proc`
* [x] `/sys`
* [x] `/dev`
* [x] `/usr`

## Boot

* [x] BIOS/UEFI
* [x] Bootloader
* [x] Kernel
* [x] initramfs
* [x] systemd
* [x] PID 1
* [x] systemd targets

## Kernel

* [x] Kernel version
* [x] Kernel modules
* [x] `lsmod`
* [x] `modinfo`
* [x] `modprobe`

## Users/security

* [x] Users
* [x] Groups
* [x] Password state
* [x] Shells
* [x] Service accounts
* [x] `sudo`
* [x] Least privilege
* [x] Permissions
* [x] ACL
* [x] SUID
* [x] SGID
* [x] Sticky Bit

## Processes

* [x] PID
* [x] Process discovery
* [x] `ps`
* [x] `pgrep`
* [x] `top`
* [x] `htop`
* [x] Signals
* [x] SIGTERM
* [x] SIGKILL
* [x] Jobs

## Services

* [x] systemd
* [x] service status
* [x] start
* [x] stop
* [x] restart
* [x] enable
* [x] disable
* [x] socket activation

## Logs

* [x] `/var/log`
* [x] journalctl
* [x] service logs
* [x] boot logs
* [x] previous boot
* [x] log priorities
* [x] log rotation

## Scheduling

* [x] cron
* [x] crontab
* [x] cron directories
* [x] systemd timers

## Networking — administrator tools

* [x] `ip addr`
* [x] `ip route`
* [x] `ss`
* [x] `ping`
* [x] hostname resolution
* [x] SSH troubleshooting
* [x] firewall basics

> **Networking fundamentals are intentionally still a separate roadmap module.**

## Backup

* [x] archive vs backup
* [x] tar
* [x] compression
* [x] extraction
* [x] archive verification
* [x] rsync
* [x] restore mindset

## Hardware

* [x] `lscpu`
* [x] `lsmem`
* [x] `lsblk`
* [x] `lspci`
* [x] `lsusb`

## Troubleshooting

* [x] service → process → port
* [x] logs
* [x] CPU
* [x] RAM
* [x] disk
* [x] network
* [x] root-cause analysis
* [x] verification after changes

---

# 61. Final Linux Administrator Mental Model

You should now be able to look at a Linux machine like this:

```text
                         LINUX SERVER
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
     USERS                  SYSTEM                NETWORK
       │                      │                      │
   users/groups          CPU / RAM / disk       IP / routes
   permissions           kernel                  ports
   sudo                  processes              SSH
       │                 systemd                 firewall
       │                 services
       │                      │
       └──────────────┬───────┘
                      │
                    LOGS
                      │
                journalctl
                      │
                      ↓
                 TROUBLESHOOT
                      │
                      ↓
                  ROOT CAUSE
                      │
                      ↓
                     FIX
                      │
                      ↓
                   VERIFY
```

---

# 62. The Most Important Skill

The goal of Linux Administration is **not**:

> "I know 100 Linux commands."

The real goal is:

> "When a Linux system has a problem, I know how to investigate it."

For example:

```text
Website is down
      ↓
Is machine alive?
      ↓
Is service running?
      ↓
Is process running?
      ↓
Is port listening?
      ↓
What do logs say?
      ↓
Is disk full?
      ↓
Is memory exhausted?
      ↓
Is CPU overloaded?
      ↓
Is network working?
      ↓
Fix root cause
      ↓
Verify
```

That is administrator thinking.

---

# 63. Final Practical Record

The Linux Administration practical work documented across this section includes:

```bash
hostname
hostnamectl

uname -r
uname -a

lscpu
free -h
swapon --show
vmstat

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
modprobe

lspci
lsusb

ulimit -a

crontab -l
crontab -e
systemctl list-timers

journalctl
journalctl -b
journalctl -b -p err
journalctl --list-boots
journalctl -u ssh

ip addr
ip route
ss -tlnp
ping
getent hosts

sudo ufw status

tar
rsync

id
groups
getent passwd
getent group
passwd -S

systemctl status
systemctl is-active
systemctl is-enabled
```

Representative practical findings from the system used during this learning path included:

```text
Hostname:
smarty

User:
pri

Shell:
/bin/bash

Home:
/home/pri

Kernel:
7.0.0-29-generic

OS:
Zorin OS 18.1

SSH:
Port 22 listening

SSH socket:
active

SSH service:
socket-activated

PID 1:
systemd

User groups:
pri adm cdrom sudo dip plugdev users lpadmin sambashare devops
```

The SSH investigation was particularly valuable because it demonstrated real administration reasoning rather than just command memorization.

---

# 64. Linux Administration — COMPLETE

```text
Linux
│
├── Fundamentals                 ✅
├── Files & directories          ✅
├── Permissions & security       ✅
├── Processes                    ✅
├── Package management           ✅
├── Services & systemd           ✅
├── SSH                          ✅
├── Logs                         ✅
├── Bash environment             ✅
├── Bash scripting               ✅
│
└── Linux Administration         ✅
       │
       ├── System administration
       ├── Storage
       ├── Filesystems
       ├── Boot
       ├── Kernel
       ├── Resources
       ├── Scheduling
       ├── Hardware
       ├── Firewall basics
       ├── Backups
       └── Troubleshooting
```

---

# Important Boundary

Linux Administration is now considered **complete for our current DevOps roadmap**.

We are **not** claiming that every possible Linux administration subject in the world has been covered. Linux is enormous and professional administrators specialize in areas such as:

* advanced storage
* LVM
* RAID
* SELinux/AppArmor
* advanced networking
* kernel compilation
* performance engineering
* high availability
* advanced systemd
* enterprise identity
* configuration management

Those are not being silently skipped. They are either outside the current beginner-to-DevOps Linux requirement or will be encountered later when they become useful.

The important Linux foundation required for the next stages is covered.

---

# Next Roadmap Position

```text
Linux Fundamentals
       ↓
Linux Administration
       ↓
████████████████████  COMPLETE
       ↓
Python for DevOps
       ↓
Networking
       ↓
Git/GitHub
       ↓
AWS
       ↓
Docker
       ↓
Kubernetes
       ↓
Terraform
       ↓
CI/CD
       ↓
Monitoring
```

**Networking fundamentals remain separate**, exactly as planned.

---

# Practical Work — Later

For now, you do **not** need to execute every command in these notes.

The notes deliberately contain the practical command and expected result so that when you return to them later, you can perform the labs yourself and compare your output with the documented result.

When we do the practical phase, the rule will be:

```text
Read the scenario
      ↓
Predict what should happen
      ↓
Run command
      ↓
Compare output
      ↓
Understand why
      ↓
Troubleshoot if different
```

That will be our final Linux Administration hands-on revision.
