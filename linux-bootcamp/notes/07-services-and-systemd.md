# Linux Services & systemd

## 1. What is a Service?

A service is a program that runs in the background and provides functionality to the system.

Examples:

- Docker → runs the Docker daemon
- SSH → allows remote access
- CUPS → handles printing
- Cron → runs scheduled tasks

Think of it like:

Linux System
├── Docker service
├── SSH service
├── CUPS service
└── Cron service

---

## 2. What is systemd?

systemd is the system and service manager used by Linux.

Think of systemd as the manager:

systemd
├── Docker
├── SSH
├── CUPS
└── Cron

It can:

- start services
- stop services
- restart services
- check service status
- enable services at boot
- disable services at boot
- view service logs

The main command is:

systemctl

---

## 3. Check a Service

Command:

systemctl status SERVICE

Example:

systemctl status docker

Important information:

Loaded: loaded
Active: active (running)
Main PID: 49778

Active: active (running) means the service is currently running.

Active: inactive (dead) means the service is currently stopped.

---

## 4. Service vs Process

A process is a running instance of a program.

We can inspect a process with:

ps -p PID

Example:

ps -p 49778

A service is managed by systemd.

The relationship can look like:

docker.service
    ↓
dockerd
    ↓
PID 49778
    ↓
running process

So:

systemctl → manages services

ps → shows processes

---

## 5. Start a Service

Command:

sudo systemctl start SERVICE

Example:

sudo systemctl start docker

Then verify:

systemctl status docker

---

## 6. Stop a Service

Command:

sudo systemctl stop SERVICE

Example:

sudo systemctl stop docker

Then:

systemctl status docker

The service should show:

Active: inactive (dead)

---

## 7. Restart a Service

Command:

sudo systemctl restart SERVICE

Example:

sudo systemctl restart docker

Restart is commonly used after changing a service configuration.

---

## 8. Enable a Service

Enable means:

"Start this service automatically when Linux boots."

Check:

systemctl is-enabled docker

Example output:

enabled

Enable it with:

sudo systemctl enable docker

---

## 9. Disable a Service

Disable means:

"Do not automatically start this service when Linux boots."

Command:

sudo systemctl disable docker

Important:

disable does not necessarily stop a currently running service.

It changes the boot behavior.

---

## 10. Active vs Enabled

These are different concepts.

Check whether the service is running now:

systemctl is-active docker

Example:

active

Check whether it starts automatically at boot:

systemctl is-enabled docker

Example:

enabled

Remember:

ACTIVE
→ Is it running right now?

ENABLED
→ Will it start automatically at boot?

A service can therefore be:

active + enabled

active + disabled

inactive + enabled

---

## 11. Finding Services

List running services:

systemctl --type=service --state=running

List service units:

systemctl list-units --type=service

---

## 12. CUPS Example

We investigated the CUPS printing service.

Command:

systemctl status cups

We found:

Active: active (running)

Main PID: 976

Then we checked the process:

ps -p 976

Output showed:

976 ... cupsd

The relationship was:

cups.service
    ↓
cupsd
    ↓
PID 976

This demonstrates that a systemd service manages a process.

---

## 13. Services and Network Ports

A service can have a process that listens on a network port.

We used:

sudo ss -ltnp

For CUPS:

sudo ss -ltnp | grep ':631'

We found:

127.0.0.1:631
[::1]:631

and the process:

cupsd

So:

CUPS service
    ↓
cupsd process
    ↓
TCP port 631

This connects Linux service management with networking.

---

## 14. Docker Example

We checked Docker with:

systemctl status docker

Docker was running:

Active: active (running)

We also found its process:

ps -p 1247

Output:

1247 ... dockerd

Later Docker was stopped.

After stopping:

Active: inactive (dead)

We checked the old PID:

ps -p 1247

No process was returned.

Then we started Docker again:

sudo systemctl start docker

Docker received a new PID:

49778

This demonstrates an important concept:

A process can stop and later restart with a different PID.

The service remains the same:

docker.service

but the process instance can change:

Old process → PID 1247

New process → PID 49778

---

## 15. Checking Service Logs

systemd stores service logs that can be viewed with journalctl.

For Docker:

journalctl -u docker

To show only errors:

journalctl -u docker -p err

If the result is:

-- No entries --

it means there are no journal entries matching that error priority for the query.

We also inspected Docker startup logs and saw messages such as:

Loading containers: done.

Daemon has completed initialization

API listen on /run/docker.sock

Started docker.service

The important lesson is that logs help us understand what a service is doing internally.

---

## 16. SSH

SSH means:

Secure Shell

SSH allows us to remotely access another computer's terminal.

Think of it like:

Phone
    │
    │ SSH
    ↓
Laptop
    │
    ↓
Linux shell

The SSH client uses:

ssh

The SSH server uses:

sshd

The service is:

ssh.service

---

## 17. SSH Client

We checked:

ssh -V

Example:

OpenSSH_9.6p1

We also checked the installed SSH client package:

dpkg -l | grep openssh

The client is used when our machine connects to another machine.

Example:

ssh pri@10.27.157.123

---

## 18. SSH Server

The SSH server accepts incoming SSH connections.

The server process is:

sshd

The systemd service is:

ssh.service

We checked:

systemctl status ssh

Initially the SSH service was not running.

After starting SSH, we verified that it was listening.

---

## 19. SSH Port

SSH normally uses:

TCP port 22

We checked:

sudo ss -ltnp | grep ':22'

We saw:

0.0.0.0:22
[::]:22

and:

sshd

This means the SSH server is listening for incoming connections.

The relationship is:

Network
    ↓
TCP port 22
    ↓
sshd
    ↓
SSH session

---

## 20. localhost

localhost means:

"This same computer."

IPv4 localhost:

127.0.0.1

We tested:

ssh localhost

This connected from the laptop back into the same laptop.

We verified:

whoami

Output:

pri

And:

hostname

Output:

pri-HP-ProBook-430-G4

So the SSH connection was working.

---

## 21. Laptop IP Address

We checked the Wi-Fi interface:

ip addr show wlp2s0

The laptop had:

10.27.157.123/24

We also checked:

hostname -I

and found:

10.27.157.123

This was the laptop's local network IP.

Therefore another device on the same network could attempt:

ssh pri@10.27.157.123

---

## 22. Phone → Laptop SSH

We installed Termux on the phone.

First we tested connectivity:

ping -c 4 10.27.157.123

Result:

4 packets transmitted
4 received
0% packet loss

This proved that the phone could reach the laptop over the network.

Then we connected:

ssh pri@10.27.157.123

The laptop's SSH server accepted the connection.

We verified:

whoami

Output:

pri

And:

hostname

Output:

pri-HP-ProBook-430-G4

This means the phone was successfully controlling the laptop's Linux shell remotely.

---

## 23. SSH Keys

Initially SSH used a password.

We then created an SSH key pair on the phone:

ssh-keygen -t ed25519

This created:

~/.ssh/id_ed25519

and:

~/.ssh/id_ed25519.pub

There are two keys:

Private key
→ id_ed25519
→ Keep secret

Public key
→ id_ed25519.pub
→ Can be shared

Think of it like:

Private key = your secret key

Public key = the lock that can be installed on a server

---

## 24. Copying the Public Key

We used:

ssh-copy-id pri@10.27.157.123

It installed the phone's public key on the laptop.

After that:

ssh pri@10.27.157.123

worked without asking for the laptop account password.

This is called:

SSH public-key authentication

---

## 25. SSH Key Files

The phone's ~/.ssh directory contained:

authorized_keys
id_ed25519
id_ed25519.pub
known_hosts
known_hosts.old

Important files:

id_ed25519
→ private key
→ never share

id_ed25519.pub
→ public key
→ safe to share

known_hosts
→ stores information about SSH servers previously contacted by this SSH client

authorized_keys
→ contains public keys allowed to authenticate to an account

---

## 26. Complete SSH Picture

Phone:

Termux
    ↓
SSH client
    ↓
private key
    ↓
network
    ↓
TCP port 22
    ↓
sshd
    ↓
public key verification
    ↓
Linux shell

Laptop:

Zorin Linux
    ↓
ssh.service
    ↓
sshd
    ↓
port 22
    ↓
user account: pri

---

## 27. The Most Important Mental Model

Do not try to memorize hundreds of commands.

Understand this chain:

Service
    ↓
systemd manages it
    ↓
Process
    ↓
Process may listen on a port
    ↓
Network connection
    ↓
Another machine can connect

For SSH:

ssh.service
    ↓
sshd
    ↓
PID
    ↓
TCP port 22
    ↓
Phone
    ↓
SSH session
    ↓
Linux shell

For CUPS:

cups.service
    ↓
cupsd
    ↓
PID 976
    ↓
TCP port 631

---

## 28. Troubleshooting Workflow

When something is not working, think step by step.

1. Is the service running?

systemctl status SERVICE

2. Is the process running?

ps aux

3. Is the expected port listening?

ss -ltnp

4. What does the service log say?

journalctl -u SERVICE

5. Is the machine reachable?

ping IP_ADDRESS

6. Can we connect?

ssh USER@IP

This workflow will become extremely useful in DevOps.

---

## 29. Important Commands

### systemd / Services

systemctl status SERVICE

sudo systemctl start SERVICE

sudo systemctl stop SERVICE

sudo systemctl restart SERVICE

sudo systemctl enable SERVICE

sudo systemctl disable SERVICE

systemctl is-active SERVICE

systemctl is-enabled SERVICE

systemctl list-units --type=service

systemctl --type=service --state=running

### Processes

ps -p PID

ps aux

### Logs

journalctl -u SERVICE

journalctl -u SERVICE -p err

### Networking

ip addr

ip addr show INTERFACE

hostname -I

ss -ltnp

sudo ss -ltnp

### Connectivity

ping -c 4 IP_ADDRESS

### SSH

ssh -V

ssh USER@IP

ssh localhost

ssh-keygen -t ed25519

ssh-copy-id USER@IP

---

## 30. DevOps Connection

These concepts are fundamental for DevOps.

Later, when working with:

- AWS
- Docker
- Kubernetes
- CI/CD
- monitoring
- Linux servers
- production systems

we will constantly ask:

What service is running?

What process is running?

What PID does it have?

What port is it listening on?

Is the network reachable?

Can I connect remotely?

Are there errors in the logs?

The goal is not command memorization.

The goal is to develop the ability to look at a Linux system and understand what is happening.

---

# Final Mental Model

Linux system

├── systemd
│   ├── docker.service
│   ├── ssh.service
│   └── cups.service
│
├── Processes
│   ├── dockerd
│   ├── sshd
│   └── cupsd
│
├── Network
│   ├── IP addresses
│   └── Ports
│
└── Remote Access
    └── SSH

This is the foundation we have built so far for Linux administration and troubleshooting.
