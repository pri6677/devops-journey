# Networking Lesson 01 — What Is a Network?

## 1. What Is a Network?

A network is a system that allows devices to communicate and exchange data with each other.

Examples of network-connected devices:

* Laptop
* Desktop
* Phone
* Server
* Printer
* Router
* Cloud server
* IoT devices

Basic idea:

```text
Computer A
    │
    │ data
    ↓
 Network
    │
    ↓
Computer B
```

The purpose of networking is to allow devices and applications to communicate.

---

# 2. Why Do Networks Exist?

A computer running an application is not very useful to remote users unless other devices can communicate with it.

For example:

```text
Laptop
   │
   │ request
   ↓
Network
   │
   ↓
Web Server
   │
   │ response
   ↓
Network
   │
   ↓
Laptop
```

Networking provides the communication path between systems.

---

# 3. Real-World Analogy

A useful analogy is a road system.

| Real World       | Networking         |
| ---------------- | ------------------ |
| Building         | Device             |
| Road             | Network connection |
| Address          | IP address         |
| Vehicle          | Data               |
| Destination      | Destination device |
| Traffic rules    | Network protocols  |
| Traffic junction | Router             |

Just as roads allow vehicles to travel between locations, networks allow data to travel between devices.

---

# 4. What Is Data?

Data is information exchanged between devices.

Examples:

* Web pages
* Images
* Videos
* Commands
* API requests
* Database queries
* SSH traffic

Data is transported through networks.

---

# 5. What Is a Packet?

Data transmitted across a network is divided into smaller units called packets.

Simplified example:

```text
Original data

HELLO_MY_FRIEND_I_AM_LEARNING_NETWORKING

             ↓

       Smaller pieces

HELLO
MY
FRIEND
I_AM
LEARNING
NETWORKING
```

A real network packet contains more information than just the application data. Later networking topics will introduce headers, source/destination addresses, protocols, ports, and payloads.

For now:

> A packet is a unit of data carried across a network.

---

# 6. Why Use Packets?

Breaking data into smaller units allows networks to:

* Share network resources between many devices
* Handle large amounts of data
* Route traffic efficiently
* Handle transmission problems
* Control how data is transmitted

---

# 7. Client and Server

A client requests a service.

A server provides a service.

Basic model:

```text
Client
   │
   │ request
   ↓
Server
   │
   │ response
   ↓
Client
```

Examples of clients:

* Web browser
* `curl`
* SSH client
* Mobile application

Examples of servers:

* Web server
* DNS server
* SSH server
* Database server
* API server

A server does not necessarily mean a special type of physical computer. A computer/application can act as a server when it provides a service to clients.

---

# 8. LAN

LAN means:

**Local Area Network**

A LAN connects devices within a relatively local area.

Examples:

* Home network
* Office network
* School network
* Computer lab

Example:

```text
             Router
           /    |    \
          /     |     \
      Laptop  Phone  Desktop
```

---

# 9. WAN

WAN means:

**Wide Area Network**

A WAN connects networks across a larger geographical area.

Conceptually:

```text
Delhi Network
      │
      │
Mumbai Network
      │
      │
London Network
```

LAN focuses on a local area, while WAN covers a larger geographical scope.

---

# 10. Internet

The Internet can be understood as a **network of interconnected networks**.

Conceptually:

```text
Home Network
      │
      ↓
ISP Network
      │
      ↓
Other Networks
      │
      ↓
Destination Network
      │
      ↓
Server
```

Many independently operated networks are interconnected to form the Internet.

---

# 11. Router

A router connects different networks and helps forward traffic between them.

Simplified:

```text
Network A
    │
    ↓
 Router
    │
    ↓
Network B
```

In a home network:

```text
Your Laptop
     │
     ↓
Home Router
     │
     ↓
Internet
```

The router commonly acts as the default gateway for devices on the local network.

---

# 12. Switch

A switch commonly connects devices within a local network.

Example:

```text
Laptop ──┐
         │
Desktop ─┤
         │
Server ──┤── Switch
         │
Printer ─┘
```

Simplified distinction:

```text
Switch
→ commonly connects devices within a network

Router
→ connects different networks
```

---

# 13. NIC

NIC means:

**Network Interface Card/Controller**

A NIC provides a network interface through which a computer can communicate.

A computer may have multiple interfaces:

```text
Linux Computer
      │
      ├── Ethernet interface
      │
      └── Wi-Fi interface
```

Linux exposes these interfaces through commands such as:

```bash
ip link
```

and:

```bash
ip addr
```

---

# 14. Linux Networking Observation

## `ip link`

Command:

```bash
ip link
```

This displays network interfaces.

My system showed:

```text
1: lo
2: enp1s0
3: wlp2s0
4: docker0
```

---

# 15. Loopback Interface

My system has:

```text
lo
```

with:

```text
inet 127.0.0.1/8
inet6 ::1/128
```

`lo` is the loopback interface.

It allows the computer to communicate with itself.

Conceptually:

```text
Your Computer
      │
      │ 127.0.0.1
      ↓
Your Computer
```

`127.0.0.1` is the IPv4 loopback address commonly used for local communication.

`::1` is the IPv6 loopback address.

---

# 16. Ethernet Interface

My system has:

```text
enp1s0
```

with:

```text
NO-CARRIER
state DOWN
```

This indicates that Linux currently does not detect an active physical Ethernet link on this interface.

My machine is currently using Wi-Fi instead.

---

# 17. Wi-Fi Interface

My active Wi-Fi interface is:

```text
wlp2s0
```

It has:

```text
state UP
```

and the IPv4 address:

```text
192.168.1.46/24
```

Therefore:

```text
Interface
    ↓
wlp2s0

IPv4 address
    ↓
192.168.1.46
```

The `/24` is CIDR notation. Subnet masks and CIDR will be studied later.

---

# 18. MAC Address

The Wi-Fi interface has:

```text
link/ether 4c:80:93:dd:d4:6b
```

This is the MAC address associated with the interface.

The system therefore has both:

```text
IP address
192.168.1.46

MAC address
4c:80:93:dd:d4:6b
```

IP addresses and MAC addresses serve different purposes and will be studied in detail later.

---

# 19. IPv6 Link-Local Address

The Wi-Fi interface also has:

```text
inet6 fe80::9caf:f456:3431:9ecf/64
```

This is an IPv6 link-local address.

IPv6 addressing will be covered later.

---

# 20. Docker Network Interface

My Linux machine also has:

```text
docker0
```

with:

```text
inet 172.17.0.1/16
```

This is a virtual network interface created by Docker.

Conceptually:

```text
Linux Host
     │
     ├── wlp2s0
     │      └── 192.168.1.46
     │
     └── docker0
            └── 172.17.0.1
```

Docker networking will become important later when learning containers.

---

# 21. `ip addr`

Command:

```bash
ip addr
```

This displays network interfaces and their assigned addresses.

Important addresses observed on my machine:

```text
lo
127.0.0.1

wlp2s0
192.168.1.46/24

docker0
172.17.0.1/16
```

---

# 22. Routing Table

Command:

```bash
ip route
```

My system showed:

```text
default via 192.168.1.1 dev wlp2s0 proto dhcp src 192.168.1.46 metric 600

172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown

192.168.1.0/24 dev wlp2s0 proto kernel scope link src 192.168.1.46 metric 600
```

The most important line initially is:

```text
default via 192.168.1.1 dev wlp2s0
```

This means Linux uses:

```text
192.168.1.1
```

as the default gateway for traffic that does not have a more specific route.

The traffic uses:

```text
wlp2s0
```

to reach the gateway.

Simplified:

```text
Your Laptop
192.168.1.46
      │
      ↓
192.168.1.1
Default Gateway / Router
      │
      ↓
Internet
```

---

# 23. Local Network Route

The routing table also contains:

```text
192.168.1.0/24 dev wlp2s0
```

This indicates that the local network:

```text
192.168.1.0/24
```

is directly reachable through:

```text
wlp2s0
```

The exact meaning of `/24` and how the network/host portions are calculated will be covered in the subnetting and CIDR lessons.

---

# 24. Neighbor Table

Command:

```bash
ip neigh
```

My system showed:

```text
192.168.1.36 dev wlp2s0 lladdr ec:5c:68:c0:b0:7f REACHABLE

192.168.1.1 dev wlp2s0 lladdr a8:3a:48:46:73:f2 REACHABLE
```

This gives mappings between local IP addresses and MAC addresses.

Simplified:

```text
IP address        MAC address

192.168.1.1   →   a8:3a:48:46:73:f2

192.168.1.36  →   ec:5c:68:c0:b0:7f
```

This is an early example of the relationship between IP addressing and MAC addressing.

The mechanism behind IPv4 local address-to-MAC resolution is ARP, which will be studied later.

---

# 25. Testing Internet Connectivity

Command:

```bash
ping 8.8.8.8
```

My result:

```text
8 packets transmitted, 8 received, 0% packet loss
```

Average round-trip time:

```text
6.211 ms
```

This shows that my system successfully exchanged ICMP echo traffic with:

```text
8.8.8.8
```

The path is conceptually:

```text
Linux Computer
      ↓
Wi-Fi
      ↓
Router
      ↓
ISP
      ↓
Internet
      ↓
8.8.8.8
```

---

# 26. TTL

The ping response included:

```text
ttl=118
```

TTL means:

**Time To Live**

It is a field associated with IP packets.

TTL will be studied in greater detail with IP and ICMP.

---

# 27. Testing a Domain Name

Command:

```bash
ping google.com
```

My system displayed:

```text
PING google.com (192.178.158.100)
```

I entered:

```text
google.com
```

but the system resolved it to:

```text
192.178.158.100
```

This demonstrates the role of DNS.

Conceptually:

```text
google.com
     ↓
DNS lookup
     ↓
192.178.158.100
     ↓
Network communication
```

This is why DNS becomes an important troubleshooting topic.

---

# 28. IP Connectivity vs DNS

Compare:

```bash
ping 8.8.8.8
```

with:

```bash
ping google.com
```

The first command already has an IP address.

```text
8.8.8.8
```

The second requires name resolution:

```text
google.com
     ↓
DNS
     ↓
IP address
```

Therefore, a useful troubleshooting distinction is:

```text
IP address works
but
domain name doesn't work

        ↓

Investigate DNS
```

This distinction will become important in Linux and Cloud troubleshooting.

---

# 29. My Current Network Map

Based on the Linux lab:

```text
                         INTERNET
                            │
                            │
                       192.168.1.1
                          Router
                            │
                          Wi-Fi
                            │
                         wlp2s0
                            │
                     192.168.1.46
                            │
                       YOUR LINUX PC
                       /           \
                      /             \
                    lo             docker0
               127.0.0.1          172.17.0.1
```

Another local device observed through the neighbor table:

```text
192.168.1.36
```

---

# 30. DevOps Connection

Networking is essential for Cloud and DevOps.

A typical application architecture might look like:

```text
User
 │
 ↓
Internet
 │
 ↓
Load Balancer
 │
 ↓
Web Server
 │
 ↓
Application
 │
 ↓
Database
```

When something fails, a DevOps engineer needs to investigate systematically:

```text
Interface
    ↓
IP address
    ↓
Route
    ↓
Gateway
    ↓
DNS
    ↓
Port
    ↓
Firewall
    ↓
Service
    ↓
Application
```

The networking track will progressively teach each part.

---

# 31. Important Concepts From Lesson 01

Remember the relationships:

```text
Network
→ allows devices to communicate

Packet
→ unit of data carried across a network

Client
→ requests a service

Server
→ provides a service

LAN
→ local-area network

WAN
→ wide-area network

Router
→ connects different networks

Switch
→ commonly connects devices within a local network

NIC
→ network interface used for communication

IP address
→ logical network address

MAC address
→ link-layer hardware/interface address

DNS
→ translates domain names into IP addresses
```

---

# 32. Linux Commands Practiced

```bash
ip link
```

View network interfaces.

```bash
ip addr
```

View interfaces and addresses.

```bash
ip route
```

View routing information.

```bash
ip neigh
```

View neighbor mappings.

```bash
ping 8.8.8.8
```

Test connectivity to an IP address.

```bash
ping google.com
```

Test name resolution and connectivity to a domain.

---

# 33. Key Mental Model

The most important idea from Lesson 01 is:

```text
Computer
   ↓
Network Interface
   ↓
Network
   ↓
Packets
   ↓
Router / Other Networks
   ↓
Destination
```

Later lessons will explain exactly how this journey works.

---

# 34. Lesson 01 Status

```text
Networking Lesson 01 — What Is a Network

Concepts:      ✅
Linux lab:     ✅
Real output:   ✅
Network map:   ✅
DevOps link:   ✅
```

Next lesson:

**Networking Lesson 02 — LAN, WAN, Internet & Network Devices**

Topics:

```text
Host
Network
Switch
Router
Modem
Access Point
NIC
LAN
WAN
Internet
```
