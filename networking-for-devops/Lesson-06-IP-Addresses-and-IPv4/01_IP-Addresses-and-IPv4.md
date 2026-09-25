
````markdown
# Networking Lesson 06: IP Addresses & IPv4

## 1. What Is an IP Address?

An IP address identifies a device/interface on a network so packets can be delivered to the correct destination.

Example:

```text
10.189.112.123
````

Your Linux machine currently has this IPv4 address on Wi-Fi:

```text
10.189.112.123/24
```

An IP address is a Layer 3 (Internet layer) concept in the TCP/IP model.

---

# 2. IPv4 Basics

IPv4 addresses are 32 bits long.

They are divided into four 8-bit sections called octets.

```text
10.189.112.123
│   │   │   │
│   │   │   └── Octet 4
│   │   └────── Octet 3
│   └────────── Octet 2
└────────────── Octet 1
```

Each octet can contain values from:

```text
0 - 255
```

Therefore:

```text
IPv4 = 4 octets × 8 bits = 32 bits
```

---

# 3. IPv4 in Binary

Each octet represents 8 bits.

Example:

```text
10 = 00001010
```

So:

```text
10.189.112.123
```

is represented as four 8-bit sections.

Understanding binary becomes important when learning subnetting and CIDR.

---

# 4. Network Portion and Host Portion

An IPv4 address can be divided into:

```text
Network portion + Host portion
```

For example:

```text
10.189.112.123/24
```

With `/24`:

```text
Network = first 24 bits
Host    = remaining 8 bits
```

Conceptually:

```text
10.189.112 | 123
-----------   ---
 Network     Host
```

The network portion identifies the network.

The host portion identifies a device inside that network.

---

# 5. CIDR Notation

CIDR means:

**Classless Inter-Domain Routing**

Example:

```text
10.189.112.123/24
```

The `/24` means:

```text
24 bits are used for the network portion.
```

IPv4 has 32 bits total:

```text
32 - 24 = 8 host bits
```

The corresponding subnet mask is:

```text
255.255.255.0
```

---

# 6. /24 Network

For:

```text
10.189.112.123/24
```

The network is:

```text
10.189.112.0/24
```

Subnet mask:

```text
255.255.255.0
```

Broadcast address:

```text
10.189.112.255
```

Traditional usable host range:

```text
10.189.112.1
      ↓
10.189.112.254
```

So:

```text
Network address = 10.189.112.0
Broadcast address = 10.189.112.255
Usable hosts = 10.189.112.1 - 10.189.112.254
```

For a normal `/24` IPv4 subnet, there are:

```text
256 total addresses
254 traditional usable host addresses
```

---

# 7. Private IPv4 Address Ranges

Private IPv4 addresses are commonly used inside LANs and private cloud networks.

The major private ranges are:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

Examples:

```text
10.189.112.123
172.17.0.1
192.168.1.10
```

These addresses are not directly routable across the public Internet.

---

# 8. Public IP Address

A public IP address is used for communication across the public Internet.

Example concept:

```text
Your private IP
      |
      v
Router/NAT
      |
      v
Public Internet
```

A home or organization router commonly performs NAT so private devices can access the Internet using a public address.

---

# 9. Loopback Address

The IPv4 loopback range is:

```text
127.0.0.0/8
```

The most commonly used loopback address is:

```text
127.0.0.1
```

It refers back to the local machine.

Test:

```bash
ping -c 4 127.0.0.1
```

Your result:

```text
4 packets transmitted, 4 received, 0% packet loss
```

This confirms that local loopback communication is working.

Conceptually:

```text
Application
    |
    v
127.0.0.1
    |
    v
Same machine
```

It does not mean traffic is going out to the LAN or Internet.

---

# 10. 0.0.0.0

`0.0.0.0` has special meanings depending on context.

For example, a server listening on:

```text
0.0.0.0:8000
```

usually means:

```text
Listen on all available IPv4 interfaces.
```

This is different from:

```text
127.0.0.1:8000
```

which means:

```text
Listen only on the local machine's loopback interface.
```

This distinction is important when deploying applications and services.

---

# 11. APIPA / IPv4 Link-Local Addresses

IPv4 link-local addresses are in:

```text
169.254.0.0/16
```

They can appear when a device cannot obtain an address from DHCP.

Example:

```text
169.254.x.x
```

A device with such an address may be able to communicate locally in limited circumstances, but it generally does not provide normal Internet connectivity.

---

# 12. IPv6 Basics

IPv6 is the newer Internet Protocol version.

IPv6 addresses are 128 bits long.

Example:

```text
2001:db8::1
```

IPv6 uses hexadecimal notation rather than IPv4's dotted decimal notation.

IPv6 loopback:

```text
::1
```

IPv6 link-local addresses commonly start with:

```text
fe80::
```

Your machine showed:

```text
fe80::b204:f3b1:7bb:eba6/64
```

This is an IPv6 link-local address.

Important:

```text
Having an IPv6 address
        ≠
Having IPv6 Internet connectivity
```

A usable IPv6 route is also required.

---

# 13. Linux Lab: Check IPv4 Addresses

Command:

```bash
ip -4 addr
```

Your relevant output was:

```text
wlp2s0:
inet 10.189.112.123/24
```

Your current Wi-Fi IPv4 configuration:

```text
Interface: wlp2s0
IPv4:      10.189.112.123
CIDR:      /24
Network:   10.189.112.0/24
Broadcast: 10.189.112.255
```

You also had:

```text
docker0:
172.17.0.1/16
```

This is the Docker bridge network on your Linux machine.

---

# 14. Check One Interface

Command:

```bash
ip addr show wlp2s0
```

Important information from your output:

```text
link/ether 4c:80:93:dd:d4:6b
inet 10.189.112.123/24
inet6 fe80::b204:f3b1:7bb:eba6/64
```

This shows:

* MAC address
* IPv4 address
* IPv6 link-local address

---

# 15. Your Current Routing Table

Command:

```bash
ip route
```

Your output:

```text
default via 10.189.112.89 dev wlp2s0 proto dhcp src 10.189.112.123 metric 600
10.189.112.0/24 dev wlp2s0 proto kernel scope link src 10.189.112.123 metric 600
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
```

The important entries are:

```text
default via 10.189.112.89 dev wlp2s0
```

and:

```text
10.189.112.0/24 dev wlp2s0
```

Your default gateway is:

```text
10.189.112.89
```

---

# 16. Local Network vs Remote Network

Your machine:

```text
10.189.112.123/24
```

Local network:

```text
10.189.112.0/24
```

Gateway:

```text
10.189.112.89
```

Because the gateway belongs to the same `/24` network:

```text
10.189.112.0/24
```

your machine can reach it directly through the local network.

For an Internet destination such as:

```text
142.250.29.139
```

Linux sees that it is not part of:

```text
10.189.112.0/24
```

so it uses the default gateway:

```text
10.189.112.89
```

Conceptually:

```text
Destination: 10.189.112.89
        |
        v
Same local subnet
        |
        v
Send directly
```

But:

```text
Destination: 142.250.29.139
        |
        v
Not local subnet
        |
        v
Use default route
        |
        v
10.189.112.89
```

This is the foundation of routing.

---

# 17. Gateway Connectivity Test

Command:

```bash
ping -c 4 10.189.112.89
```

Your result:

```text
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 2.388/10.422/19.077/8.022 ms
```

This confirms that your Linux machine can reach its default gateway.

Conceptually:

```text
Your PC
10.189.112.123
      |
      v
Gateway
10.189.112.89
      |
      v
Internet
```

---

# 18. Why 192.168.0.1 Did Not Work

Earlier you tested:

```bash
ping -c 4 192.168.0.1
```

and received 100% packet loss.

Your current network is:

```text
10.189.112.0/24
```

not:

```text
192.168.0.0/24
```

Your current gateway is:

```text
10.189.112.89
```

Therefore, `192.168.0.1` is not your current gateway.

This demonstrates why you should inspect the routing table instead of assuming the gateway address.

Use:

```bash
ip route
```

to find the current default gateway.

---

# 19. IPv4 Internet Connectivity Test

Command:

```bash
ping -4 -c 4 google.com
```

Your system resolved:

```text
google.com
    ↓
142.250.29.139
```

Result:

```text
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 48.177/59.169/83.887/14.561 ms
```

This confirms working IPv4 Internet connectivity.

The journey is approximately:

```text
Your PC
10.189.112.123
      |
      v
Local Wi-Fi network
      |
      v
Gateway
10.189.112.89
      |
      v
Internet
      |
      v
Google
142.250.29.139
```

---

# 20. IPv6 Connectivity Test

Command:

```bash
ping -6 -c 4 google.com
```

Your result:

```text
ping: connect: Network is unreachable
```

This means Linux currently does not have a usable IPv6 route for reaching the destination.

Your machine does have an IPv6 link-local address:

```text
fe80::b204:f3b1:7bb:eba6/64
```

But that alone does not provide IPv6 Internet connectivity.

The important distinction is:

```text
IPv6 address
     +
usable IPv6 route
     +
IPv6 gateway/connectivity
     =
IPv6 Internet connectivity
```

---

# 21. Why IPv4 Works but IPv6 Does Not

Your IPv4 routing table contains a default route:

```text
default via 10.189.112.89 dev wlp2s0
```

So for an unknown IPv4 destination:

```text
Unknown IPv4 destination
        |
        v
Default route
        |
        v
10.189.112.89
```

For IPv6, your current system does not have an equivalent usable route to the Internet.

Therefore:

```text
IPv6 destination
      |
      v
IPv6 routing table
      |
      v
No suitable route
      |
      v
Network is unreachable
```

This is a practical example of why routing tables matter.

---

# 22. `ping -c` Syntax

The `-c` option specifies the number of packets to send.

Correct:

```bash
ping -c 4 google.com
```

Meaning:

```text
-c 4 = send 4 packets
```

Incorrect:

```bash
ping -c google.com
```

because `ping` expects a numeric packet count after `-c`.

---

# 23. `ping -4` and `ping -6`

Force IPv4:

```bash
ping -4 -c 4 google.com
```

Force IPv6:

```bash
ping -6 -c 4 google.com
```

This is useful for troubleshooting when a system supports both protocols.

For example:

```text
IPv4 works
IPv6 fails
```

This immediately tells you that the problem may be specific to IPv6 configuration or routing rather than general Internet connectivity.

---

# 24. Packet Loss

Example:

```text
4 packets transmitted, 4 received, 0% packet loss
```

This means every ICMP packet received a reply.

If you see:

```text
4 packets transmitted, 2 received, 50% packet loss
```

then half of the packets did not receive replies.

Packet loss can indicate:

* Network problems
* Congestion
* Wireless instability
* Firewall behavior
* Routing problems
* Destination-side filtering

Ping results should be interpreted in context because some devices intentionally block or rate-limit ICMP.

---

# 25. Latency

Latency is the time required for a packet to travel to the destination and receive a response.

Example:

```text
time=49.0 ms
```

Lower latency generally means a faster round trip.

Your gateway test:

```text
min = 2.388 ms
avg = 10.422 ms
max = 19.077 ms
```

Google IPv4 test:

```text
min = 48.177 ms
avg = 59.169 ms
max = 83.887 ms
```

The Internet destination has higher latency because the packet travels much farther and crosses additional network infrastructure.

---

# 26. Same Subnet vs Different Subnet

Suppose your machine is:

```text
10.189.112.123/24
```

Then:

```text
10.189.112.50
```

is in the same `/24` subnet:

```text
10.189.112.0/24
```

So it can be reached directly on the local network.

But:

```text
10.189.113.50
```

belongs to:

```text
10.189.113.0/24
```

which is a different subnet.

Traffic to a different subnet normally needs a router/default gateway.

Conceptually:

```text
Same subnet:

PC ───────────── Device
       direct


Different subnet:

PC ─── Gateway/Router ─── Device
```

This concept becomes extremely important in:

* AWS VPCs
* Docker
* Kubernetes
* Virtual machines
* Linux servers
* Cloud networking

---

# 27. How Linux Decides Where to Send a Packet

Suppose your machine needs to send a packet.

Linux checks the destination against its routing table.

Example:

```text
Destination:
10.189.112.89
```

Routing table contains:

```text
10.189.112.0/24 dev wlp2s0
```

Therefore:

```text
Destination belongs to local subnet
        ↓
Use wlp2s0 directly
```

Now suppose destination is:

```text
142.250.29.139
```

That is not inside:

```text
10.189.112.0/24
```

So Linux uses:

```text
default via 10.189.112.89
```

Therefore:

```text
Destination is remote
        ↓
Use default gateway
```

This is one of the most important concepts from this lesson.

---

# 28. Practical Command Cheat Sheet

## Show IPv4 addresses

```bash
ip -4 addr
```

## Show all addresses

```bash
ip addr
```

## Show a specific interface

```bash
ip addr show wlp2s0
```

## Show routing table

```bash
ip route
```

## Test loopback

```bash
ping -c 4 127.0.0.1
```

## Test gateway

```bash
ping -c 4 10.189.112.89
```

## Test IPv4 Internet

```bash
ping -4 -c 4 google.com
```

## Test IPv6 Internet

```bash
ping -6 -c 4 google.com
```

## Check interface state

```bash
ip link
```

---

# 29. DevOps Connection

IP addressing is fundamental to almost every DevOps technology.

## Linux

You need to understand:

```text
IP
Subnet
Gateway
Route
Interface
```

for server troubleshooting.

## AWS

You will encounter:

```text
VPC
Subnet
CIDR
Route Table
Internet Gateway
NAT Gateway
Private IP
Public IP
```

Example:

```text
VPC: 10.0.0.0/16

Subnet:
10.0.1.0/24
```

Understanding `/24` and `/16` is therefore essential.

## Docker

Your machine already has:

```text
172.17.0.0/16
```

for the default Docker bridge network.

## Kubernetes

Kubernetes networking uses multiple IP ranges for:

```text
Pods
Services
Nodes
```

Understanding IP addressing and routing will make those concepts much easier.

## Troubleshooting

A common DevOps troubleshooting sequence is:

```text
Interface
   ↓
IP address
   ↓
Subnet
   ↓
Route
   ↓
Gateway
   ↓
DNS
   ↓
Destination
   ↓
Port
   ↓
Firewall
   ↓
Service
   ↓
Application
```

---

# 30. Important Takeaways

Remember these points:

1. IPv4 addresses are 32 bits.
2. IPv4 has four octets.
3. Each octet ranges from 0 to 255.
4. `/24` means 24 network bits and 8 host bits.
5. `10.189.112.123/24` belongs to `10.189.112.0/24`.
6. The traditional `/24` broadcast address is `10.189.112.255`.
7. Your current gateway is `10.189.112.89`.
8. `127.0.0.1` is the IPv4 loopback address.
9. `0.0.0.0` can mean all IPv4 interfaces when used as a server bind/listen address.
10. Private IPv4 ranges include `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16`.
11. `169.254.0.0/16` is IPv4 link-local/APIPA space.
12. IPv6 addresses are 128 bits.
13. `fe80::/10` is IPv6 link-local space.
14. Having an IPv6 address does not automatically mean IPv6 Internet connectivity.
15. `ip route` shows how Linux routes traffic.
16. A default route is used when no more specific route matches.
17. Same-subnet traffic can be sent directly; traffic to another subnet normally goes through a router.
18. `ping -4` forces IPv4.
19. `ping -6` forces IPv6.
20. `Network is unreachable` commonly indicates that Linux has no suitable route for the destination.

---

# Lesson 06 Practical Summary

Your actual Linux networking state during this lab:

```text
Wi-Fi interface:
wlp2s0

IPv4:
10.189.112.123/24

IPv4 network:
10.189.112.0/24

Broadcast:
10.189.112.255

Default gateway:
10.189.112.89

IPv6 link-local:
fe80::b204:f3b1:7bb:eba6/64

Docker network:
172.17.0.0/16
```

Connectivity:

```text
127.0.0.1          → SUCCESS
10.189.112.89      → SUCCESS
IPv4 Google        → SUCCESS
IPv6 Google        → NO USABLE ROUTE
```

The biggest concept to carry forward:

```text
IP Address
    +
Subnet/CIDR
    +
Routing Table
    +
Gateway
    ↓
Determines how Linux reaches a destination
```

---

# Next Lesson

## Lesson 07 — Subnetting & CIDR

You will learn:

```text
Why /24?
What does /25 mean?
How many hosts are in /26?
What is the network address?
What is the broadcast address?
Are 192.168.1.10 and 192.168.2.10 on the same network?
Why does AWS use /16, /24, /28, etc.?
```

These concepts directly prepare you for:

```text
AWS VPC
AWS Subnets
Routing Tables
Docker Networking
Kubernetes Networking
Cloud Infrastructure
```

```
```
