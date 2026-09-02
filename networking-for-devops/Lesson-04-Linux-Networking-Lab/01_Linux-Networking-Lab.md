Yes — here is the **entire Lesson 04 in ONE single copy block**. Just click **Copy** once.

````markdown
# Networking Lesson 04 — Linux Networking Lab

## 1. Lesson Overview

In this lesson, we used Linux networking commands to inspect how a real Linux machine connects to a network.

We practiced:

- Network interfaces
- Loopback
- Ethernet
- Wi-Fi
- Docker bridge
- MAC addresses
- IPv4 addresses
- IPv6 addresses
- Subnet masks
- Default gateway
- Routing table
- Neighbor/ARP information
- Network connectivity
- Listening ports
- TCP and UDP sockets
- Localhost vs all interfaces
- HTTP/HTTPS connectivity
- Basic OSI layer troubleshooting

The goal was not just to memorize commands.

The goal was to understand:

> "What is my Linux machine doing on the network?"

---

# 2. Network Interfaces

A network interface is a connection point through which a computer communicates with a network.

A Linux machine can have multiple interfaces.

For example:

```text
Computer
│
├── lo
│   └── Loopback
│
├── enp1s0
│   └── Ethernet
│
├── wlp2s0
│   └── Wi-Fi
│
└── docker0
    └── Docker virtual network
````

We can inspect interfaces using:

```bash
ip link
```

---

# 3. `ip link`

Command:

```bash
ip link
```

Purpose:

Shows the network interfaces available on the Linux system.

It mainly shows:

* Interface names
* Interface state
* MAC addresses
* Interface flags
* MTU

Example interfaces observed:

```text
lo
enp1s0
wlp2s0
docker0
```

---

# 4. Loopback Interface — `lo`

The interface:

```text
lo
```

means:

> Loopback interface.

It allows a computer to communicate with itself.

Its most common IPv4 address is:

```text
127.0.0.1
```

IPv6 loopback:

```text
::1
```

Example:

```bash
ip addr show lo
```

You may see:

```text
inet 127.0.0.1/8
inet6 ::1/128
```

---

# 5. Why Loopback Is Important

Loopback is heavily used in Linux and DevOps.

For example:

```text
Application A
     │
     ▼
127.0.0.1
     │
     ▼
Application B
```

The communication stays inside the same machine.

It does not need to travel through the physical network.

Examples:

```text
127.0.0.1:3000
127.0.0.1:5000
127.0.0.1:8080
127.0.0.1:5432
```

These are commonly used by locally running applications and databases.

---

# 6. Ethernet Interface — `enp1s0`

Our system also had:

```text
enp1s0
```

This is an Ethernet network interface.

It is normally used for a wired network connection.

We observed:

```text
NO-CARRIER
state DOWN
```

This means the interface exists, but there is no active physical Ethernet connection.

For example:

```text
Computer
   │
   │ Ethernet cable
   X
Router/Switch
```

If the cable is disconnected, Linux may report:

```text
NO-CARRIER
```

---

# 7. Wi-Fi Interface — `wlp2s0`

Our active Wi-Fi interface was:

```text
wlp2s0
```

It showed:

```text
UP
LOWER_UP
```

This indicates that the interface is active and has a working lower-level network connection.

Our Wi-Fi IPv4 address was:

```text
192.168.0.152/24
```

---

# 8. Docker Interface — `docker0`

We also saw:

```text
docker0
```

This is a virtual network bridge created by Docker.

Our system had:

```text
172.17.0.1/16
```

associated with the Docker bridge.

Conceptually:

```text
Linux Host
│
├── Wi-Fi
│   └── 192.168.0.152
│
└── docker0
    └── 172.17.0.1
         │
         ├── Container
         ├── Container
         └── Container
```

Docker creates virtual networking so containers can communicate.

This becomes very important later when learning:

* Docker
* Kubernetes
* Containers
* Cloud networking

---

# 9. MAC Address

Every network interface normally has a MAC address.

MAC means:

> Media Access Control

A MAC address identifies a network interface at the data-link layer.

Example format:

```text
aa:bb:cc:dd:ee:ff
```

We can see MAC addresses using:

```bash
ip link
```

or:

```bash
ip link show wlp2s0
```

---

# 10. IPv4 Address

We used:

```bash
ip addr
```

This command shows IP addresses assigned to interfaces.

Our Wi-Fi interface had:

```text
192.168.0.152/24
```

Breaking it down:

```text
192.168.0.152
       │
       └── IPv4 address
```

The:

```text
/24
```

is the CIDR prefix length.

---

# 11. What `/24` Means

An IPv4 address contains:

```text
32 bits
```

A `/24` means:

```text
24 bits = network portion
8 bits  = host portion
```

Conceptually:

```text
192.168.0.152/24

Network       Host
────────────  ─────
192.168.0     152
```

The subnet mask for `/24` is:

```text
255.255.255.0
```

The network address is:

```text
192.168.0.0
```

The broadcast address is:

```text
192.168.0.255
```

Usable host range:

```text
192.168.0.1 - 192.168.0.254
```

---

# 12. IPv6

Linux also showed IPv6 addresses.

For example, we saw a link-local address beginning with:

```text
fe80::
```

IPv6 addresses are much larger than IPv4 addresses.

IPv4:

```text
32 bits
```

IPv6:

```text
128 bits
```

IPv6 loopback:

```text
::1
```

IPv6 link-local addresses commonly begin with:

```text
fe80::
```

---

# 13. `ip route`

Command:

```bash
ip route
```

Purpose:

Shows the Linux routing table.

Our system had a default route similar to:

```text
default via 192.168.0.1 dev wlp2s0
```

This is extremely important.

---

# 14. Understanding the Default Route

The line:

```text
default via 192.168.0.1 dev wlp2s0
```

means:

```text
For destinations that don't match
a more specific route:

send traffic to
192.168.0.1

through:
wlp2s0
```

`192.168.0.1` is our default gateway.

Usually, this is the local router.

---

# 15. Default Gateway

A default gateway is the device Linux uses to reach networks outside its local network.

Example:

```text
Your Computer
192.168.0.152
      │
      ▼
Default Gateway
192.168.0.1
      │
      ▼
Internet
```

Without an appropriate route/default gateway, a machine may be unable to reach the Internet.

---

# 16. Local Route

Our routing table also contained a route similar to:

```text
192.168.0.0/24 dev wlp2s0
```

This tells Linux that:

```text
192.168.0.0/24
```

is directly reachable through:

```text
wlp2s0
```

Therefore, traffic to another device such as:

```text
192.168.0.20
```

can be sent directly on the local network rather than through the Internet.

---

# 17. Docker Route

We also saw a route similar to:

```text
172.17.0.0/16 dev docker0
```

This represents Docker's virtual network.

Conceptually:

```text
Host
│
└── docker0
      │
      ├── 172.17.0.x
      ├── 172.17.0.x
      └── 172.17.0.x
```

This demonstrates that Linux can maintain multiple networks and routes simultaneously.

---

# 18. `ip neigh`

Command:

```bash
ip neigh
```

Purpose:

Shows the neighbor table.

For IPv4 Ethernet networks, this is closely related to ARP.

Example:

```text
192.168.0.1 dev wlp2s0 lladdr XX:XX:XX:XX:XX:XX REACHABLE
```

This means Linux knows the MAC address associated with the IP address.

---

# 19. ARP Concept

Suppose our computer wants to communicate with:

```text
192.168.0.1
```

It needs to know the destination MAC address on the local network.

ARP helps resolve:

```text
IP address
     │
     ▼
MAC address
```

Conceptually:

```text
192.168.0.1
     │
     ▼
ARP
     │
     ▼
MAC address
```

Then Ethernet frames can be sent to the correct device.

---

# 20. `REACHABLE`

When we saw:

```text
REACHABLE
```

it meant Linux considered the neighbor entry recently confirmed/reachable.

Example:

```text
192.168.0.1 dev wlp2s0 lladdr XX:XX:XX:XX:XX:XX REACHABLE
```

This is a good sign when troubleshooting local network communication.

---

# 21. `INCOMPLETE`

We also saw some entries with:

```text
INCOMPLETE
```

This means Linux has not successfully resolved the neighbor's link-layer address yet.

For example:

```text
192.168.0.x dev wlp2s0 INCOMPLETE
```

This does not automatically mean the entire network is broken.

The particular destination may simply be unavailable or not responding.

---

# 22. Testing the Gateway

We tested:

```bash
ping -c 4 192.168.0.1
```

The gateway responded successfully.

We got:

```text
4 packets transmitted
4 packets received
0% packet loss
```

This tells us that our machine could reach the local gateway using ICMP.

---

# 23. Testing Internet Connectivity

We then tested:

```bash
ping -c 4 8.8.8.8
```

The result showed successful replies.

This demonstrated that:

```text
Computer
   │
   ▼
Wi-Fi
   │
   ▼
Gateway
   │
   ▼
Internet
   │
   ▼
8.8.8.8
```

was reachable using ICMP.

---

# 24. Important Difference: Ping

`ping` primarily tests ICMP connectivity.

For example:

```bash
ping -c 4 8.8.8.8
```

It does NOT prove that every application service is working.

A successful ping means:

> IP-level communication using ICMP worked.

It does not necessarily mean:

```text
HTTP works
HTTPS works
SSH works
DNS works
Database works
```

---

# 25. `ss`

Command:

```bash
ss -tuln
```

This is used to inspect sockets.

Options:

```text
-s     meaning
────────────────────────────
-t     TCP
-u     UDP
-l     listening
-n     don't resolve names; show numbers
```

Therefore:

```bash
ss -tuln
```

means:

> Show listening TCP and UDP sockets using numeric addresses/ports.

---

# 26. TCP and UDP Listening Ports

We observed multiple listening sockets.

For example:

```text
0.0.0.0:22
[::]:22
```

Port:

```text
22
```

is commonly used by SSH.

This means an SSH server was listening.

---

# 27. Port 22

SSH commonly uses:

```text
TCP port 22
```

Conceptually:

```text
Client
   │
   │ TCP connection
   │
   ▼
Server
TCP 22
   │
   ▼
SSH
```

This is extremely important for DevOps because SSH is commonly used to access Linux servers.

---

# 28. `127.0.0.1:PORT`

Suppose an application listens on:

```text
127.0.0.1:8080
```

This normally means:

> The service is listening only on the local machine.

Other machines generally cannot connect directly to that listener.

Example:

```text
Same Machine
     │
     ▼
127.0.0.1:8080
     │
     ▼
Application
```

---

# 29. `0.0.0.0:PORT`

Suppose a service listens on:

```text
0.0.0.0:8080
```

For an IPv4 listening socket, this generally means:

> Listen on all IPv4 interfaces.

For example:

```text
Wi-Fi
192.168.0.152
      │
      ├─────────┐
      │         │
Ethernet       │
      │         │
      └────┬────┘
           ▼
      0.0.0.0:8080
           │
           ▼
       Application
```

This distinction is extremely important when deploying applications.

---

# 30. `localhost`

`localhost` usually refers to the local machine.

A common IPv4 mapping is:

```text
localhost → 127.0.0.1
```

Example:

```bash
curl http://localhost:8080
```

The request is directed to a service running locally.

---

# 31. Testing HTTPS With `curl`

We used:

```bash
curl -I https://example.com
```

The `-I` option asks for response headers rather than downloading the complete response body.

We received an HTTP response similar to:

```text
HTTP/2 200
```

This demonstrated successful application-level HTTPS communication.

---

# 32. Ping vs Curl

These two commands test different things.

### Ping

```bash
ping -c 4 8.8.8.8
```

Tests:

```text
ICMP
↓
IP connectivity
```

### Curl

```bash
curl -I https://example.com
```

Tests:

```text
HTTPS
↓
TCP
↓
IP
↓
Network
```

So:

```text
ping works
```

does not guarantee:

```text
curl works
```

And:

```text
curl works
```

means much more of the communication stack is functioning.

---

# 33. Practical OSI Layer Mapping

The OSI model is a conceptual framework.

Our practical Linux commands can be related to different layers.

```text
OSI Layer 7 — Application
    │
    └── curl, HTTP, HTTPS, DNS, SSH

OSI Layer 4 — Transport
    │
    └── TCP, UDP, ports, ss

OSI Layer 3 — Network
    │
    └── IP, routing, ping

OSI Layer 2 — Data Link
    │
    └── MAC, ARP, Ethernet, ip neigh

OSI Layer 1 — Physical
    │
    └── Cable, Wi-Fi radio, carrier
```

Linux does not literally have separate commands for each OSI layer.

The model is used to help us understand and troubleshoot networking.

---

# 34. Example: Troubleshooting a Server

Suppose you cannot access a server.

Do not immediately assume:

> "The application is broken."

Instead, troubleshoot layer by layer.

A useful chain is:

```text
1. Interface
      ↓
2. IP address
      ↓
3. Route
      ↓
4. Gateway
      ↓
5. DNS
      ↓
6. Destination
      ↓
7. Port
      ↓
8. Firewall
      ↓
9. Service
      ↓
10. Application
```

This is a very important DevOps troubleshooting mindset.

---

# 35. Example Troubleshooting Commands

### Check interfaces

```bash
ip link
```

### Check IP addresses

```bash
ip addr
```

### Check routing

```bash
ip route
```

### Check neighbors

```bash
ip neigh
```

### Test gateway

```bash
ping -c 4 192.168.0.1
```

### Test Internet IP

```bash
ping -c 4 8.8.8.8
```

### Check listening ports

```bash
ss -tuln
```

### Test HTTP/HTTPS

```bash
curl -I https://example.com
```

---

# 36. Our Network

Based on the commands we ran, our system can be represented approximately as:

```text
                    INTERNET
                       │
                       │
                       ▼
                192.168.0.1
                 Default Gateway
                       │
                       │ Wi-Fi
                       ▼
              wlp2s0 / 192.168.0.152
                       │
                ┌──────┴──────┐
                │   Linux     │
                │   System    │
                └──────┬──────┘
                       │
             ┌─────────┼──────────┐
             │         │          │
             ▼         ▼          ▼
            lo       enp1s0     docker0
        127.0.0.1    Ethernet   172.17.0.1
                                   │
                                   ▼
                              Containers
```

---

# 37. Commands Practiced

Throughout this lesson we practiced:

```bash
ip link
```

```bash
ip addr
```

```bash
ip route
```

```bash
ip neigh
```

```bash
ping -c 4 192.168.0.1
```

```bash
ping -c 4 8.8.8.8
```

```bash
ss -tuln
```

```bash
curl -I https://example.com
```

---

# 38. What We Learned

We learned how to inspect a real Linux machine's networking configuration.

Important concepts:

* Network interfaces
* Loopback
* Ethernet
* Wi-Fi
* Docker virtual networking
* MAC addresses
* IPv4
* IPv6
* CIDR `/24`
* Network address
* Broadcast address
* Default gateway
* Routing table
* Neighbor table
* ARP concept
* ICMP
* TCP
* UDP
* Ports
* Listening sockets
* Localhost
* `0.0.0.0`
* HTTPS
* Basic OSI mapping
* Network troubleshooting

---

# 39. Why This Matters for DevOps

Networking is everywhere in DevOps.

### Linux

You need networking to troubleshoot servers.

### AWS

You will work with:

```text
VPC
Subnets
Route Tables
Internet Gateway
NAT Gateway
Security Groups
Network ACLs
Load Balancers
```

### Docker

Containers communicate using virtual networks.

### Kubernetes

Pods and services communicate through networking.

### Terraform

Terraform creates cloud networking infrastructure.

### CI/CD

Build servers communicate with:

```text
Git repositories
Artifact repositories
Cloud services
Application servers
Containers
Kubernetes clusters
```

### Monitoring

Monitoring systems communicate over networks to collect metrics and logs.

---

# 40. Important DevOps Mindset

When something cannot connect, don't randomly change configurations.

Collect evidence.

For example:

```text
Can I see the interface?
        ↓
Does it have an IP?
        ↓
Is the route correct?
        ↓
Can I reach the gateway?
        ↓
Can I reach the destination?
        ↓
Does DNS resolve?
        ↓
Is the port listening?
        ↓
Is the firewall blocking it?
        ↓
Is the service running?
        ↓
Is the application responding?
```

This approach will become extremely useful when troubleshooting real production systems.

---

# 41. Final Mental Model

Remember this:

```text
Interface
    ↓
IP Address
    ↓
Subnet
    ↓
Route
    ↓
Gateway
    ↓
Destination
    ↓
Port
    ↓
Service
    ↓
Application
```

Networking troubleshooting is basically finding:

> "Where exactly does communication stop?"

---

# 42. Lesson Status

## Networking Lesson 04 — Linux Networking Lab

Status:

```text
COMPLETED
```

We successfully inspected our real Linux network and connected the commands to the concepts we have been learning.

---

# 43. Next Lesson

## Networking Lesson 05 — TCP/IP Model

Next we will learn:

* TCP/IP model
* Its layers
* Application layer
* Transport layer
* Internet layer
* Network Access/Link layer
* TCP vs IP
* How TCP/IP relates to OSI
* Encapsulation
* Decapsulation
* Headers
* Real packet journey
* What happens when you run:

```bash
curl https://example.com
```

We will connect the theory directly to Linux, AWS, Docker, Kubernetes, and DevOps.

```
```
