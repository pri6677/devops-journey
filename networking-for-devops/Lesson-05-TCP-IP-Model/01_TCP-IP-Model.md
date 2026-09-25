
# Networking Lesson 05 — TCP/IP Model

## 1. Why Do We Need a Networking Model?

Networking involves many different technologies and protocols.

A networking model gives us a structured way to understand:

> Which part of network communication is responsible for what?

A simplified network communication flow looks like:

Application
↓
TCP
↓
IP
↓
Wi-Fi / Ethernet
↓
Physical network

Each part has a different responsibility.

---

# 2. The TCP/IP Model

The TCP/IP model is commonly represented using 4 layers:

```text
┌─────────────────────────────┐
│  4. Application             │
├─────────────────────────────┤
│  3. Transport               │
├─────────────────────────────┤
│  2. Internet                │
├─────────────────────────────┤
│  1. Network Access / Link   │
└─────────────────────────────┘
````

The four layers are:

1. Application
2. Transport
3. Internet
4. Network Access / Link

---

# 3. Layer 4 — Application

The Application layer is where network applications and application protocols operate.

Examples:

* HTTP
* HTTPS
* DNS
* SSH
* SMTP
* FTP

For example:

```bash
curl https://example.com
```

`curl` is interacting with an application protocol: HTTPS.

The Application layer answers:

> What does the communication actually mean?

For HTTP, the communication can contain information such as:

```text
GET / HTTP/2
Host: example.com
```

---

# 4. Layer 3 — Transport

The Transport layer handles communication between applications/processes.

The two major protocols are:

* TCP
* UDP

## TCP

TCP provides features such as:

* Reliable delivery
* Ordering
* Acknowledgements
* Retransmission
* Connection management

## UDP

UDP provides:

* Low overhead
* No connection establishment
* No built-in delivery guarantee

---

# 5. Ports

Ports are associated with the Transport layer.

For example:

```text
192.168.0.152:54321
```

The IP address identifies the machine/interface.

The port identifies the application endpoint.

A simplified view:

```text
IP address
    +
Port
    ↓
Application endpoint
```

---

# 6. Layer 2 — Internet

The Internet layer is primarily concerned with:

* IP addressing
* Routing
* Delivering packets between networks

The main protocols include:

* IPv4
* IPv6

Example IPv4 address:

```text
192.168.0.152
```

IP answers the question:

> Where should this packet go?

The Linux command:

```bash
ip route
```

is directly related to this layer.

Example:

```text
default via 192.168.0.1 dev wlp2s0
```

This tells Linux where to send traffic when there is no more specific route.

---

# 7. Layer 1 — Network Access / Link

This layer handles communication over the local network technology.

Examples include:

* Ethernet
* Wi-Fi
* MAC addresses
* Frames

The command:

```bash
ip link
```

shows network interface information.

For example:

```text
wlp2s0
```

is a Wi-Fi network interface.

A MAC address may look like:

```text
4c:80:93:dd:d4:6b
```

The MAC address is associated with the network interface at the local network/link level.

---

# 8. TCP/IP Model Overview

```text
┌─────────────────────────────────────┐
│ Application                         │
│ HTTP, HTTPS, DNS, SSH, SMTP, FTP    │
├─────────────────────────────────────┤
│ Transport                           │
│ TCP, UDP, Ports                     │
├─────────────────────────────────────┤
│ Internet                            │
│ IPv4, IPv6, Routing                 │
├─────────────────────────────────────┤
│ Network Access / Link               │
│ Ethernet, Wi-Fi, MAC, Frames        │
└─────────────────────────────────────┘
```

---

# 9. Real Example — curl

Suppose we run:

```bash
curl https://example.com
```

Conceptually, the communication travels through the layers:

```text
Application
    │
    │ HTTPS
    ▼
Transport
    │
    │ TCP
    ▼
Internet
    │
    │ IP
    ▼
Network Access
    │
    │ Wi-Fi / Ethernet
    ▼
Network
```

On the receiving machine, the process is reversed:

```text
Physical / Link
      ↓
IP
      ↓
TCP
      ↓
HTTPS
      ↓
Application
```

This process is called:

* Encapsulation
* Decapsulation

---

# 10. Encapsulation

When data moves down through the networking stack, each layer adds information required by that layer.

Conceptually:

```text
Application data
       ↓
┌─────────────────────┐
│ TCP │ Application   │
└─────────────────────┘
       ↓
┌────────────────────────────┐
│ IP │ TCP │ Application     │
└────────────────────────────┘
       ↓
┌──────────────────────────────────┐
│ Ethernet │ IP │ TCP │ Application│
└──────────────────────────────────┘
```

Each layer adds its own information, commonly through headers.

A useful analogy is putting a letter inside multiple envelopes.

---

# 11. Decapsulation

When the receiving computer gets the data, the process happens in reverse.

```text
Ethernet frame
      ↓
Remove link-layer information
      ↓
IP packet
      ↓
Remove IP information
      ↓
TCP segment
      ↓
Remove TCP information
      ↓
Application data
```

This process is called decapsulation.

---

# 12. Data Units

A simplified view of the terminology is:

```text
Application
    ↓
Data

Transport
    ↓
TCP Segment / UDP Datagram

Internet
    ↓
IP Packet

Network Access / Link
    ↓
Frame
```

So the general flow is:

```text
Application Data
       ↓
TCP Segment
       ↓
IP Packet
       ↓
Ethernet / Wi-Fi Frame
```

---

# 13. OSI Model vs TCP/IP Model

The OSI model has 7 layers:

```text
7. Application
6. Presentation
5. Session
4. Transport
3. Network
2. Data Link
1. Physical
```

The TCP/IP model commonly has 4 layers:

```text
4. Application
3. Transport
2. Internet
1. Network Access
```

A common mapping is:

```text
OSI                         TCP/IP

Application ───────┐
Presentation ──────┼──→ Application
Session ───────────┘

Transport ─────────────→ Transport

Network ───────────────→ Internet

Data Link ────────┐
Physical ─────────┴──→ Network Access
```

The models are different abstractions.

The Internet protocol suite is commonly discussed using the TCP/IP model, while the OSI model is widely used as a conceptual framework for understanding networking.

---

# 14. Linux Commands and the TCP/IP Model

You have already used many Linux commands that correspond to different networking concepts.

| Command    | Main concept                    |
| ---------- | ------------------------------- |
| `ip link`  | Network interface / link        |
| `ip addr`  | IP addressing                   |
| `ip route` | Routing                         |
| `ip neigh` | Neighbor / ARP information      |
| `ping`     | ICMP / IP connectivity          |
| `ss`       | TCP / UDP sockets               |
| `curl`     | Application-layer communication |

---

# 15. DevOps Connection

The TCP/IP model is useful when troubleshooting network problems.

Suppose:

```bash
curl https://myserver.com
```

fails.

Instead of randomly changing configurations, troubleshoot layer by layer.

## Application

Check whether the HTTP/HTTPS service is working.

Example:

```bash
curl
```

## Transport

Check whether the TCP port is reachable.

Examples:

```bash
ss
nc
```

## Internet

Check IP addressing and routing.

Examples:

```bash
ip addr
ip route
ping
```

## Network Access / Link

Check whether the network interface is working.

Examples:

```bash
ip link
ip neigh
```

This gives you a structured troubleshooting process.

---

# 16. Practical Lab

Run the following commands in order.

## Step 1 — Check network interfaces

```bash
ip link
```

Look for your Wi-Fi interface:

```text
wlp2s0
```

---

## Step 2 — Check your IP address

```bash
ip addr show wlp2s0
```

You should see something similar to:

```text
inet 192.168.x.x/24
```

---

## Step 3 — Check your routing table

```bash
ip route
```

Look for:

```text
default via ...
```

The default route normally points to your default gateway.

---

## Step 4 — Check your neighbors

```bash
ip neigh
```

You may see something similar to:

```text
192.168.x.1 dev wlp2s0 lladdr xx:xx:xx:xx:xx:xx REACHABLE
```

This shows a neighbor associated with your local network.

---

## Step 5 — Check TCP and UDP sockets

```bash
ss -tuln
```

Options:

```text
-t = TCP
-u = UDP
-l = listening
-n = numeric
```

---

## Step 6 — Generate Application-Layer Traffic

Run:

```bash
curl -I https://example.com
```

You should receive HTTP response headers.

Think about the complete journey:

```text
curl
 ↓
HTTPS
 ↓
TCP
 ↓
IP
 ↓
Wi-Fi
 ↓
Internet
 ↓
example.com
```

---

# 17. TCP/IP Troubleshooting Flow

A useful simplified troubleshooting chain is:

```text
Application
     ↓
Transport
     ↓
IP / Routing
     ↓
Network Interface
     ↓
Physical / Wi-Fi
```

For Linux troubleshooting:

```text
ip link
    ↓
ip addr
    ↓
ip route
    ↓
ip neigh
    ↓
ping
    ↓
ss
    ↓
curl
```

The exact order can vary depending on the problem, but this gives a useful starting structure.

---

# 18. Important Concepts to Remember

## TCP/IP has 4 main layers

```text
1. Network Access / Link
2. Internet
3. Transport
4. Application
```

Remember them from bottom to top:

```text
Network Access
      ↓
Internet
      ↓
Transport
      ↓
Application
```

Or from top to bottom:

```text
Application
      ↓
Transport
      ↓
Internet
      ↓
Network Access
```

---

## Layer Responsibilities

### Application

```text
What is the communication about?
```

Examples:

```text
HTTP
HTTPS
DNS
SSH
SMTP
FTP
```

### Transport

```text
Which application/process?
```

Examples:

```text
TCP
UDP
Ports
```

### Internet

```text
Where should the packet go?
```

Examples:

```text
IPv4
IPv6
Routing
```

### Network Access / Link

```text
How does it travel across the local network?
```

Examples:

```text
Wi-Fi
Ethernet
MAC
Frames
```

---

# 19. Real-World Example

When you run:

```bash
curl https://example.com
```

a simplified conceptual flow is:

```text
┌───────────────────────────────┐
│ Application                   │
│ HTTPS                         │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Transport                     │
│ TCP                           │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Internet                      │
│ IP                            │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Network Access / Link         │
│ Wi-Fi / Ethernet              │
└───────────────┬───────────────┘
                ↓
             Network
                ↓
          example.com
```

---

# 20. DevOps Importance

Understanding TCP/IP is important for DevOps because many production problems involve networking.

Examples:

* Application cannot connect to database
* Server cannot reach the Internet
* Docker container cannot reach another container
* Kubernetes service cannot be reached
* AWS EC2 instance cannot connect to another instance
* HTTP service is running but inaccessible
* Port is blocked
* Routing is incorrect
* DNS works but TCP connection fails

The TCP/IP model helps identify which part of the communication path should be investigated.

---

# 21. Quick Revision

```text
TCP/IP Model

Application
    ↓
HTTP / HTTPS / DNS / SSH

Transport
    ↓
TCP / UDP / Ports

Internet
    ↓
IP / Routing

Network Access / Link
    ↓
Wi-Fi / Ethernet / MAC / Frames
```

Encapsulation:

```text
Data
 ↓
TCP Segment
 ↓
IP Packet
 ↓
Frame
```

Decapsulation:

```text
Frame
 ↓
IP Packet
 ↓
TCP Segment
 ↓
Data
```

Useful Linux commands:

```bash
ip link
ip addr
ip route
ip neigh
ping
ss
curl
```

---

# 22. Key Takeaway

The TCP/IP model divides network communication into layers so that each layer has a specific responsibility.

The most important mental model is:

```text
Application
    ↓
Transport
    ↓
Internet
    ↓
Network Access
```

And when troubleshooting:

```text
Is the interface working?
        ↓
Does it have an IP?
        ↓
Is routing correct?
        ↓
Can it reach the destination?
        ↓
Is the TCP port reachable?
        ↓
Is the application responding?
```

This layered approach will become especially important later when working with:

* AWS VPCs
* EC2
* Docker
* Kubernetes
* Load Balancers
* Firewalls
* Security Groups
* CI/CD infrastructure
* Production troubleshooting

```
```
