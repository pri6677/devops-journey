# Networking Lesson 02 — LAN, WAN & Network Devices

## 1. Learning Objectives

In this lesson, we learned:

- What a host is
- What a network interface is
- What a NIC does
- What an Access Point is
- What a router does
- What a switch does
- What a modem does
- Difference between a switch and router
- LAN
- WAN
- Internet
- How these components appear in a real home network
- How to observe our own Linux network
- How to begin troubleshooting network connectivity systematically

---

# 2. What Is a Host?

A **host** is a device connected to a network that can send or receive network traffic.

Examples:

- Laptop
- Desktop
- Server
- Phone
- Virtual machine
- Cloud instance
- Container

Our Linux computer is a host.

```text
Linux Computer
      ↓
    Host
```

The term **host** is commonly used in networking and DevOps.

For example:

> "Can you reach the host?"

means:

> "Can you communicate with that network-connected system?"

---

# 3. Network Interface

A network interface is the part of a system that provides network connectivity.

Think of it as a **door through which the computer communicates with a network**.

```text
             Your Computer
          ┌─────────────────┐
          │                 │
          │  Applications    │
          │                 │
          │  Linux           │
          │                 │
          └────────┬────────┘
                   │
                  NIC
                   │
                Network
```

A computer can have multiple network interfaces.

Our machine has:

```text
lo       → Loopback
enp1s0   → Ethernet
wlp2s0   → Wi-Fi
docker0  → Docker virtual interface
```

---

# 4. Our Wi-Fi Interface

We used:

```bash
ip link
```

Our active Wi-Fi interface is:

```text
wlp2s0
```

It showed:

```text
<BROADCAST,MULTICAST,UP,LOWER_UP>
state UP
```

This means our Wi-Fi interface currently has an active network link.

Our Ethernet interface:

```text
enp1s0
```

showed:

```text
<NO-CARRIER,...,UP>
state DOWN
```

This indicates that there is currently no active Ethernet carrier/link.

---

# 5. Access Point

An **Access Point (AP)** provides wireless network connectivity to devices.

Simplified:

```text
Laptop
   ))) Wi-Fi
   ↓
Access Point
```

An access point can connect multiple wireless devices:

```text
             Access Point
             /     |     \
            /      |      \
        Laptop   Phone   Tablet
```

In many homes, the Wi-Fi access point is built into the same physical device as the router.

Therefore, one physical home networking device may provide several functions:

```text
Router
+
Switch
+
Wi-Fi Access Point
+
DHCP
+
NAT
```

The important thing is to understand the **networking functions**, not just the physical boxes.

---

# 6. Router

A **router connects different networks and forwards packets between them**.

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

Our home router provides a path from our local network toward the Internet.

Our setup:

```text
Your Laptop
192.168.1.46
      │
      ↓
192.168.1.1
Home Router
      │
      ↓
ISP
      │
      ↓
Internet
```

---

# 7. Default Gateway

Our route table showed:

```text
default via 192.168.1.1 dev wlp2s0
```

Therefore:

```text
Default Gateway = 192.168.1.1
```

A default gateway is essentially the **exit point from our local network** when traffic needs to reach a destination outside the local network.

Mental model:

```text
             YOUR LAN
                 │
                 │
          Your Laptop
        192.168.1.46
                 │
                 ↓
        Default Gateway
          192.168.1.1
                 │
                 ↓
                ISP
                 │
                 ↓
             Internet
```

---

# 8. Switch

A **switch** primarily connects devices within a local network.

Example:

```text
PC ───┐
      │
PC ───┤
      │
Server┤
      │
      ↓
    Switch
```

A useful beginner mental model:

```text
Switch
  ↓
"Connect devices within my network."

Router
  ↓
"Connect my network to another network."
```

This is a simplified model. Later, routing, IP addressing, MAC addresses, and forwarding will make the distinction more precise.

---

# 9. Switch vs Router

## Switch

```text
PC ──┐
     │
PC ──┤
     ↓
   SWITCH
     ↑
     │
Server
```

Primarily connects devices inside a local network.

## Router

```text
Network A
    │
    ↓
 ROUTER
    │
    ↓
Network B
```

Connects different networks and forwards traffic between them.

Remember:

```text
Switch → connects devices within a network

Router → connects different networks
```

---

# 10. Modem

A **modem** provides the connection between local networking equipment and the ISP's access technology.

The exact technology depends on how the ISP provides service.

Historically:

```text
Modem
= Modulator-Demodulator
```

A simplified model:

```text
Home
 │
Modem
 │
ISP
 │
Internet
```

Modern home devices often combine modem, router, switch, and Wi-Fi access point functions into one physical device.

---

# 11. LAN

**LAN** stands for **Local Area Network**.

A LAN is a network covering a relatively small/local area, such as:

- Home
- Office
- School
- Lab

Our home network is a LAN.

We have:

```text
192.168.1.46
```

for our laptop and:

```text
192.168.1.1
```

for our gateway/router.

Our local network is:

```text
192.168.1.0/24
```

We will learn exactly what `/24` means during IP addressing and subnetting.

Simplified:

```text
          HOME LAN
      192.168.1.0/24
              │
       ┌──────┼──────┐
       │      │      │
    Laptop   Phone  Other
    .1.46
       │
       ↓
    Router
    .1.1
       │
       ↓
    Internet
```

---

# 12. WAN

**WAN** stands for **Wide Area Network**.

A WAN connects networks over larger geographical areas.

Example:

```text
Delhi Office
     │
     │
    WAN
     │
     │
Mumbai Office
```

Companies can use WAN technologies to connect offices, data centers, and other locations.

Cloud infrastructure also relies on networking across large geographical areas.

---

# 13. Internet

The Internet can be understood as a **network of interconnected networks**.

It is not one single giant network device.

Simplified:

```text
Home LAN
    │
    ↓
   ISP
    │
    ↓
 Internet
   /   \
  /     \
AWS    Google
 │       │
Servers Servers
```

---

# 14. Our Real Network

Based on our Linux commands, our current network can be represented as:

```text
                       INTERNET
                           │
                          ISP
                           │
                     Home Router
                      192.168.1.1
                           │
                         Wi-Fi
                           │
                        wlp2s0
                           │
                     192.168.1.46
                           │
                      Your Linux PC
```

Our PC also has other interfaces:

```text
Your PC
 ├── lo
 │    └── 127.0.0.1
 │
 ├── wlp2s0
 │    └── 192.168.1.46
 │
 ├── enp1s0
 │    └── Ethernet
 │
 └── docker0
      └── 172.17.0.1
```

---

# 15. Docker Network Interface

Our system also has:

```text
docker0
```

with:

```text
172.17.0.1/16
```

This is a virtual network interface created by Docker.

Conceptually:

```text
                    Linux Host
                       │
              ┌────────┴────────┐
              │                 │
          wlp2s0             docker0
       192.168.1.46        172.17.0.1
              │                 │
           Home LAN        Docker Network
```

This will become important later when learning Docker networking.

---

# 16. Practical Linux Observation

## Check network interfaces

```bash
ip link
```

This shows network interfaces and their link state.

---

## Check IP addresses

```bash
ip addr
```

Our active interface showed:

```text
wlp2s0
192.168.1.46/24
```

---

## Check routing

```bash
ip route
```

Our output contained:

```text
default via 192.168.1.1 dev wlp2s0
```

Therefore:

```text
Default gateway = 192.168.1.1
```

---

# 17. Test Local Connectivity

We tested the local gateway:

```bash
ping -c 4 192.168.1.1
```

Result:

```text
4 packets transmitted, 4 received, 0% packet loss
```

Average round-trip time:

```text
2.215 ms
```

This demonstrated connectivity between:

```text
Laptop
   │
   ↓
Wi-Fi
   │
   ↓
192.168.1.1
Router
```

---

# 18. Test Internet Connectivity

We tested:

```bash
ping -c 4 8.8.8.8
```

Result:

```text
4 packets transmitted, 4 received, 0% packet loss
```

Average round-trip time:

```text
4.927 ms
```

This demonstrated a working path approximately like:

```text
Laptop
   ↓
Wi-Fi
   ↓
Home Router
   ↓
ISP
   ↓
Internet
   ↓
8.8.8.8
```

---

# 19. Troubleshooting Insight

The two ping tests test different parts of the network.

## Test 1

```bash
ping -c 4 192.168.1.1
```

Tests local connectivity toward the gateway.

```text
Laptop
   ↓
Local Network
   ↓
Router
```

## Test 2

```bash
ping -c 4 8.8.8.8
```

Tests connectivity farther beyond the local network.

```text
Laptop
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

This introduces an important troubleshooting principle:

```text
Don't randomly run commands.

Isolate the failure.
        ↓
Find where communication stops.
```

---

# 20. Example Troubleshooting Scenarios

## Scenario A

```text
ping 192.168.1.1
        ↓
      works

ping 8.8.8.8
        ↓
      fails
```

The local connection to the router is working.

The problem may be farther beyond the local network, such as the router's Internet connection, ISP path, or another routing problem.

---

## Scenario B

```text
ping 192.168.1.1
        ↓
      fails
```

Investigate the local network first:

- Wi-Fi/Ethernet connection
- Network interface
- IP configuration
- Local routing
- Gateway
- Wireless/access-point connectivity

---

# 21. DevOps Connection

Networking knowledge is essential when running:

```text
Frontend
Backend
Database
```

A typical architecture might look like:

```text
                 Internet
                    │
                    ↓
              Load Balancer
                    │
                    ↓
               Frontend/Web
                    │
                    ↓
                 Backend
                    │
                    ↓
                Database
```

Networking helps answer:

- Who can communicate with whom?
- Which network is the server in?
- Which route does traffic take?
- Which port is being used?
- Where can traffic be blocked?
- Is the problem local or remote?

These concepts later appear in:

- AWS VPCs
- Subnets
- Route tables
- Security Groups
- Docker networks
- Kubernetes Services
- Kubernetes Ingress
- Load Balancers
- CI/CD infrastructure

---

# 22. Key Terms

| Term | Meaning |
|---|---|
| Host | Network-connected device |
| NIC | Network interface hardware |
| Network interface | System interface used for network communication |
| Access Point | Provides wireless network connectivity |
| Switch | Primarily connects devices within a network |
| Router | Connects different networks |
| Modem | Provides connectivity to an ISP's access technology |
| LAN | Local Area Network |
| WAN | Wide Area Network |
| Internet | Interconnected networks |
| Gateway | Device/path used to reach other networks |
| Default gateway | Gateway used when no more specific route exists |

---

# 23. Important Mental Model

Remember:

```text
Host
 ↓
NIC
 ↓
Switch / Access Point
 ↓
Router
 ↓
Other Networks
 ↓
Internet
```

And for our actual machine:

```text
Your Linux PC
      │
   wlp2s0
      │
   Wi-Fi
      │
192.168.1.1
   Router
      │
     ISP
      │
  Internet
```

---

# 24. What We Learned

We can now explain our own network instead of simply running commands.

Our system has:

```text
Wi-Fi interface:
wlp2s0

IPv4:
192.168.1.46

Local network:
192.168.1.0/24

Default gateway:
192.168.1.1

Docker interface:
docker0

Docker IP:
172.17.0.1
```

Connectivity tests showed:

```text
Laptop → Router       SUCCESS
Laptop → Internet     SUCCESS
```

This is the foundation for later network troubleshooting.

---

# 25. Interview Questions

1. What is a host?
2. What is a network interface?
3. What does a router do?
4. What does a switch do?
5. What is an Access Point?
6. What is the difference between a switch and a router?
7. What is a LAN?
8. What is a WAN?
9. What is the Internet?
10. What is a default gateway?
11. Why can one physical home device perform multiple networking functions?
12. What does `ip route` show?
13. What does `ip addr` show?
14. Why would you ping the default gateway during troubleshooting?
15. If the gateway responds but `8.8.8.8` doesn't, what part of the path would you investigate?

---

# 26. Lesson Summary

The most important concepts from this lesson are:

```text
Host
  ↓
Network Interface
  ↓
Local Network
  ↓
Gateway / Router
  ↓
Other Networks
  ↓
Internet
```

Networking is not just about memorizing IP addresses.

As a Cloud/DevOps engineer, the goal is to understand:

```text
Who is communicating?
        ↓
Through which interface?
        ↓
On which network?
        ↓
Through which gateway?
        ↓
Along which path?
        ↓
To which destination?
```

That way, when something breaks, we can **reason about the failure instead of randomly trying commands**.
