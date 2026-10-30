# Networking for DevOps — Lecture 14
## UDP (User Datagram Protocol): Connectionless Communication, Ports, and Real-World Uses

**Roadmap position:** Networking → Lecture 14  
**Previous lecture:** Lecture 13 — ICMP, Ping, TTL, and Traceroute  
**Today's focus:** Understanding UDP, how it uses ports, why it is lightweight, and why applications such as DNS, online games, and real-time video use it.

---

# 1. What Is UDP?

**UDP stands for User Datagram Protocol.**

UDP is a **Layer 4 (Transport Layer)** protocol in the TCP/IP networking model. It operates on top of IP and allows applications running on different hosts to exchange data.

To understand why UDP is needed, consider your laptop running several applications simultaneously:

- A browser accessing a website.
- A video call running in the background.
- A DNS request resolving a domain name.
- An online game receiving updates from a server.

All these applications use the network, but your operating system must know which application should receive each incoming piece of data.

UDP helps accomplish this using **port numbers**.

### Where UDP fits into networking

```text
          Application
       DNS, games, media
                |
                v
          UDP (Layer 4)
        Source and destination
             port numbers
                |
                v
           IP (Layer 3)
       Source and destination
             IP addresses
                |
                v
      Ethernet / Wi-Fi (Layer 2)
          MAC addressing
                |
                v
       Physical transmission
```

This diagram shows the conceptual layering. Real applications can use different combinations of transport and link-layer protocols, but the essential idea is that UDP carries application data inside IP packets.

### What is a datagram?

The data unit associated with UDP is called a **UDP datagram**.

For example, imagine a DNS application wants to ask a DNS server for the IP address of `example.com`.

The application creates a DNS message. UDP adds its transport header, including source and destination ports. IP then encapsulates the UDP datagram inside an IP packet.

Conceptually:

```text
DNS message
    |
    v
+----------------------+------------------+
| UDP Header (8 bytes) | DNS Message      |
+----------------------+------------------+
                |
                v
+-----------------------------------------+
| IP Header | UDP Header | DNS Message    |
+-----------------------------------------+
                |
                v
       Link-layer frame
```

**Remember these distinctions:**

| Term | Meaning |
|---|---|
| UDP | Transport-layer protocol |
| Datagram | UDP's data unit |
| Port | Identifies a transport-layer endpoint associated with an application |
| IP packet | Carries the UDP datagram across IP networks |
| Ethernet frame | Carries the IP packet over an Ethernet link |

---

# 2. Understanding Ports in UDP

An IP address identifies a network interface or host's network-layer destination, depending on the context. A port number helps the operating system deliver incoming transport data to the appropriate application endpoint.

Think of it this way:

- **IP address:** Which machine or network interface should receive the traffic?
- **Port number:** Which application endpoint on that machine should receive it?

For example, a DNS server commonly receives DNS queries on UDP port `53`.

If a client sends a UDP datagram to a DNS server at `192.168.1.100`, destination port `53` tells the receiving operating system which UDP socket should receive the datagram.

The exact application handling the data depends on which process has the relevant socket open.

## 2.1 Source and destination ports

A UDP header contains four main fields:

| Field | Size | Purpose |
|---|---:|---|
| Source port | 16 bits | Identifies the sender's transport endpoint; it can be zero when no source port is used |
| Destination port | 16 bits | Identifies the destination transport endpoint |
| Length | 16 bits | Length of the UDP header plus UDP data |
| Checksum | 16 bits | Provides error detection for the UDP datagram and relevant IP pseudo-header information |

The UDP header is **8 bytes long**.

Port numbers are 16 bits, so their numerical range is `0–65535`.

Commonly, applications use well-known or registered ports for server services, while clients often use temporary, or *ephemeral*, source ports.

### Example: A DNS query

Suppose your laptop sends a DNS query to a DNS server.

```text
Client laptop
IP: 192.168.1.10
Source port: 53000
           |
           | UDP datagram
           v
DNS server
IP: 192.168.1.53
Destination port: 53
```

The UDP information looks conceptually like this:

```text
Source IP:        192.168.1.10
Destination IP:   192.168.1.53

Source port:      53000
Destination port: 53

UDP data:         DNS query
```

Here, `53000` is an illustrative client port, not a port that every DNS query must use.

The operating system uses the destination IP address and transport information to deliver the datagram to the appropriate socket.

---

# 3. Core Characteristics of UDP

UDP has several important characteristics.

## 3.1 Connectionless

UDP does not establish a transport connection before sending data.

TCP, by contrast, normally begins with a three-way handshake:

```text
Client                         Server
  |                               |
  |------ SYN ------------------->|
  |<----- SYN-ACK ----------------|
  |------ ACK ------------------->|
  |                               |
  |       Connection ready        |
```

UDP does not perform this handshake.

A sender can construct and send a UDP datagram without first establishing a connection with the receiver.

For example:

```text
Client                         Server
  |                               |
  |------ UDP datagram ---------->|
  |                               |
  |------ UDP datagram ---------->|
  |                               |
```

There is no UDP connection handshake in this exchange.

**Important:** Connectionless does not mean that UDP cannot be used in an ongoing conversation. Applications can exchange thousands of UDP datagrams and maintain their own session state.

For example, a multiplayer game can maintain a game session while using UDP to exchange frequent position updates.

## 3.2 Stateless at the transport-protocol level

UDP does not maintain TCP-style connection state, sequence numbers, or a retransmission mechanism.

However, avoid interpreting *stateless* as meaning that nothing remembers anything.

The operating system still maintains socket information, and applications can maintain their own state.

For example, a game server may remember:

- Which players are connected.
- Their current positions.
- Their health and equipment.
- Which game session they belong to.

UDP simply does not provide TCP-style reliable, ordered delivery by itself.

## 3.3 Unreliable delivery

UDP provides **no built-in guarantee that a datagram will reach its destination**.

A datagram might be:

- Lost because of network congestion.
- Dropped by a firewall.
- Discarded because the receiver is overloaded.
- Received more than once due to application or network behavior.
- Delivered out of order relative to other datagrams.

UDP itself does not retransmit lost datagrams or rearrange them into the order in which they were sent.

Consider a game sending three position updates:

```text
Sender                         Receiver
  |                               |
  |------ Update 1 -------------->|
  |------ Update 2 -----X         |  Lost
  |------ Update 3 -------------->|
  |                               |
```

The receiver might obtain Update 1 and Update 3 without receiving Update 2.

For a fast-moving game, that may be acceptable. The latest position update might be more useful than an older update that arrives too late.

For other applications, losing data may be unacceptable. Those applications must implement their own reliability mechanisms or use a different transport protocol.

## 3.4 Lightweight

UDP has a fixed **8-byte header**, excluding the payload and any IP or link-layer headers.

TCP has a larger, variable-length header and provides more functionality, including connection management, sequence numbers, acknowledgments, retransmission mechanisms, and flow control.

UDP avoids much of that built-in machinery.

But there is an important correction to a common oversimplification:

**UDP does not have zero protocol overhead.**

It still adds an 8-byte header. IP and the link layer add their own headers, and applications still need processing time.

The accurate conclusion is that UDP has **low transport-protocol overhead**, not zero overhead.

## 3.5 Fast, but not automatically faster in every situation

UDP avoids the transport handshake and the delay associated with TCP's built-in retransmission and ordered-delivery mechanisms.

This can make it especially useful for latency-sensitive applications.

However, UDP is not automatically faster in every scenario.

Actual performance depends on factors such as:

- Network latency.
- Packet loss.
- Congestion.
- Packet size and frequency.
- Application design.
- Whether the application needs reliability.
- Whether the application implements additional mechanisms on top of UDP.

A well-designed application using UDP can be excellent for real-time traffic. A poorly designed UDP application can perform worse than one using TCP.

### UDP characteristics: revision table

| Characteristic | UDP |
|---|---|
| Transport layer | Layer 4 |
| Connection handshake | No |
| Header size | 8 bytes |
| Built-in retransmission | No |
| Built-in ordered delivery | No |
| Built-in connection state | No TCP-style connection state |
| Port numbers | Yes |
| Delivery guarantee | No |
| Typical benefit | Low overhead and low-latency communication |

---

# 4. Real-World Applications of UDP

Your lecture identifies several important applications of UDP. Let's understand why each one may benefit from it.

## 4.1 WebRTC: Real-time communication in browsers

WebRTC enables real-time audio, video, and data communication between compatible applications, including web browsers.

Imagine a browser-based video call.

The application needs to send audio and video continuously while minimizing delay.

Suppose a video frame contains information that arrives late. Displaying it several seconds after it was recorded may be less useful than displaying the next, more recent frame.

UDP can help support this low-latency communication model.

WebRTC commonly uses secure RTP media over UDP when network conditions permit, with ICE helping establish connectivity. WebRTC can also use TCP-based paths or relays in some situations, so it is not restricted to UDP alone.

**DevOps connection:** If a real-time communication service experiences choppy audio or video, you may need to investigate packet loss, latency, firewall rules, NAT traversal, and network connectivity.

## 4.2 Multiplayer gaming

Online multiplayer games often exchange frequent updates about player positions, movements, and actions.

For example:

```text
Game client                    Game server
     |                              |
     |------ Position: X=10 ------->|
     |------ Position: X=12 ------->|
     |------ Position: X=15 ------->|
     |<----- Updated game state ----|
```

Imagine the second update is lost.

If the next update arrives shortly afterward, the server may still be able to estimate the player's current position using the newer information.

Retransmitting every old position update could increase delay and deliver outdated information.

However, not all game data can safely be lost.

For example:

- Frequent position updates may tolerate some loss.
- A critical inventory change may require reliable delivery.
- A purchase or account update must not silently disappear.

Game developers may use UDP for time-sensitive traffic and implement custom reliability, sequencing, or acknowledgment mechanisms for data that needs them.

**Key idea:** UDP is useful when minimizing delay matters more than guaranteeing the delivery of every individual update.

## 4.3 Video and audio calls

Applications such as Zoom may use UDP for real-time media when the network and application configuration permit it.

Live audio and video must balance quality against delay.

Consider a video call:

- Network delay increases.
- A few media packets are lost.
- The next audio packets arrive successfully.

The application may conceal the missing audio or video information and continue playing newer media.

For a live conversation, this can be preferable to waiting for retransmissions of old media.

However, UDP does not itself guarantee smooth playback. The application must handle jitter, packet loss, buffering, and media synchronization.

**DevOps connection:** Network quality for real-time applications is often evaluated using latency, jitter, packet loss, and bandwidth.

## 4.4 VPNs and the TCP-over-TCP problem

Your lecture mentions OpenVPN, which supports both UDP and TCP transport modes.

A VPN creates a tunnel through which other network traffic travels.

Suppose a TCP application sends traffic through a VPN tunnel that itself uses TCP:

```text
Application TCP connection
           |
           v
       VPN tunnel
     using outer TCP
           |
           v
        Internet
```

The inner TCP connection and outer TCP connection can both attempt to handle packet loss and retransmissions.

Under certain loss and congestion conditions, their recovery mechanisms can interact badly, causing extra buffering and poor performance. This is commonly called the **TCP-over-TCP meltdown problem**.

Using UDP as the VPN's outer transport avoids adding a second TCP reliability layer around the tunneled traffic.

The inner TCP connection can still use TCP's reliability mechanisms.

### Important clarification

UDP does not automatically make a VPN secure or reliable.

Security comes from the VPN's cryptographic and authentication mechanisms. The transport choice affects how the tunnel carries data and handles network conditions.

OpenVPN supports UDP and TCP; other VPN technologies may use different transport designs.

## 4.5 DNS: Domain Name System

Domain Name System translates domain names into information such as IP addresses.

For example:

```text
example.com
     |
     v
DNS resolver
     |
     v
IP address information
```

A traditional DNS query commonly uses UDP port `53`.

The client sends a DNS query, and the server returns a response. This can happen without establishing a TCP connection first.

That makes UDP convenient for small request-response exchanges.

### Example

```text
Client                         DNS server
  |                                 |
  |---- UDP query, port 53 -------->|
  |<--- UDP response ---------------|
  |                                 |
```

The client typically uses an ephemeral source port, while the DNS server receives the query on destination port `53`.

The response reverses the transport ports:

```text
Query:
Source port:      53000
Destination port: 53

Response:
Source port:      53
Destination port: 53000
```

These port numbers are illustrative.

### A correction about DNS performance

The lecture's summary compares TCP's 11 trips with UDP's 2 trips. Treat that as a simplified illustration of the extra exchanges that connection setup can require, **not as a universal DNS timing rule**.

A basic DNS exchange over UDP can often complete in one query and one response. A new TCP connection may require additional setup exchanges before the DNS request and response.

However:

- DNS also supports TCP, and TCP is important for certain responses and other DNS operations.
- Modern DNS may use encrypted transports with additional setup behavior.
- DNS over TLS uses TCP, while DNS over HTTPS commonly uses HTTPS over TCP or HTTP/3 over QUIC.
- UDP queries can be retried over TCP when required, including in response to truncated DNS messages.

Therefore, the accurate takeaway is that **UDP is efficient for many small DNS request-response exchanges, but DNS is not limited to UDP**.

## 4.6 QUIC: Reliability built on UDP

QUIC is an important example of how applications can build additional transport functionality on top of UDP.

UDP itself does not guarantee delivery, ordering, or retransmission.

QUIC implements its own mechanisms for features including:

- Reliable delivery of stream data.
- Loss detection and recovery.
- Congestion control.
- Encryption and connection establishment.
- Multiplexing multiple streams.

HTTP/3 uses QUIC.

Conceptually:

```text
HTTP/3
   |
   v
QUIC
(reliability, congestion control,
 encryption, streams)
   |
   v
UDP
   |
   v
IP
   |
   v
Network
```

This demonstrates a crucial networking principle:

**UDP provides a lightweight transport foundation, and higher-level protocols can add the behavior they need.**

QUIC is not simply unreliable data sent through UDP. It implements its own reliability mechanisms while using UDP as its underlying transport.

---

# 5. How UDP Datagrams Travel Through the Network

Now let's connect UDP to the networking concepts you have already learned: IP addresses, routing, MAC addresses, and the OSI model.

Suppose your laptop sends a DNS query to a DNS server.

Assume these illustrative values:

| Property | Client | DNS server |
|---|---|---|
| IP address | `192.168.1.10` | `192.168.1.53` |
| UDP port | `53000` | `53` |

Assume both hosts are on the same local subnet.

## Step 1: The application creates data

The DNS resolver needs to resolve a domain name.

It creates a DNS query message.

At this point, the DNS message contains the DNS-specific information, but the network stack still needs to transport it to the DNS server.

## Step 2: UDP adds its header

UDP encapsulates the DNS message.

```text
+----------------------+------------------+
| UDP Header           | DNS Query        |
| Src: 53000           |                  |
| Dst: 53              |                  |
+----------------------+------------------+
```

The source port identifies the client's local transport endpoint. The destination port identifies the DNS service's transport endpoint.

The UDP header also contains the length and checksum fields.

## Step 3: IP adds its header

IP encapsulates the UDP datagram in an IP packet.

```text
+-----------------+----------------------+------------------+
| IP Header       | UDP Header           | DNS Query        |
| Src: 192.168.1.10| Src: 53000           |                  |
| Dst: 192.168.1.53| Dst: 53              |                  |
+-----------------+----------------------+------------------+
```

IP addresses help the network stack determine where the packet should go.

The routing table determines whether the destination is directly reachable or requires a next hop.

## Step 4: The link layer delivers the packet

Because the example assumes the DNS server is on the same local subnet, the client needs the server's link-layer address.

For IPv4 over Ethernet, the client can use ARP to resolve the destination's IPv4 address to a MAC address if the mapping is not already available.

The packet is then carried inside a link-layer frame.

```text
+------------------+-----------------+------------------+
| Ethernet Header  | IP Header       | UDP + DNS Data   |
+------------------+-----------------+------------------+
```

If the DNS server were on a remote network instead, the client would normally send the frame to its default gateway's MAC address. The IP destination would still be the DNS server.

That is the same local-versus-remote routing behavior you studied in earlier lectures.

## Step 5: The receiver processes the packet

At the destination, the receiving system processes the data through its network stack.

Conceptually:

```text
Ethernet frame
      |
      v
IP packet
      |
      v
UDP datagram
      |
      v
Destination UDP socket (port 53)
      |
      v
DNS server processes query
```

The operating system uses the destination address and UDP port information to deliver the datagram to the appropriate socket.

The DNS server processes the query and prepares a response.

## Step 6: The response reverses the transport ports

The DNS response typically uses:

```text
Source UDP port:      53
Destination UDP port: 53000
```

Its source and destination IP addresses correspond to the DNS server and client, respectively, subject to any NAT or other address translation along the path.

The client receives the response through the appropriate socket.

**Important:** UDP does not guarantee that the response will arrive. The DNS client or resolver must have appropriate timeout and retry behavior if a response does not arrive.

---

# 6. UDP vs. TCP

You should understand this comparison clearly because it is a common networking and DevOps interview topic.

| Feature | UDP | TCP |
|---|---|---|
| Full name | User Datagram Protocol | Transmission Control Protocol |
| Layer | Transport (Layer 4) | Transport (Layer 4) |
| Connection setup | No transport handshake | Normally uses a three-way handshake |
| Header size | 8 bytes | Minimum 20 bytes |
| Delivery guarantee | None built into UDP | Reliable delivery of the TCP byte stream |
| Retransmissions | Not provided by UDP itself | Built in |
| Ordering | Not guaranteed | Provides ordered byte-stream delivery |
| Flow control | Not provided by UDP itself | Built in |
| Congestion control | Not provided by UDP itself | Built in |
| Data unit | Datagram | Segment |
| Communication pattern | Message-oriented datagrams | Byte stream |
| Typical examples | DNS queries, real-time media, gaming | SSH, many web connections, file transfers |

A few details matter:

1. UDP applications can implement their own acknowledgments, retries, congestion control, or ordering.
2. TCP does not preserve application message boundaries; it provides a byte stream.
3. UDP preserves datagram boundaries for the receiving application, but a datagram may be lost.
4. UDP's smaller header does not guarantee that an application using UDP will always perform better than one using TCP.

### Which protocol should an application choose?

**TCP is often appropriate when reliable, ordered delivery is important.**

Examples include transferring files or establishing an SSH session.

**UDP is often appropriate when low latency and application-specific handling of loss are important.**

Examples include real-time media and frequent game-state updates.

Modern protocols such as QUIC demonstrate that applications can also implement reliable communication over UDP when they need it.

---

# 7. Hands-On Linux Lab: Observe UDP on Zorin OS

Let's inspect UDP using your Linux terminal.

## Lab 1: View UDP sockets

Run:

```bash
ss -u -a -n
```

What the options mean:

- `ss` — displays socket information.
- `-u` — selects UDP sockets.
- `-a` — displays listening and non-listening sockets.
- `-n` — displays numerical addresses and port numbers instead of resolving names.

You may see output similar to:

```text
State   Recv-Q Send-Q Local Address:Port  Peer Address:Port
UNCONN  0      0      0.0.0.0:5353        0.0.0.0:*
UNCONN  0      0      127.0.0.1:323       0.0.0.0:*
```

This is illustrative. Your actual output may be different.

UDP sockets are often shown as `UNCONN` because UDP does not establish TCP-style connections. Some UDP sockets can nevertheless be associated with a specific peer by the application or operating system.

**Try this too:**

```bash
ss -u -a -n -p
```

The `-p` option attempts to show process information. You may need `sudo` to see details about processes owned by other users.

```bash
sudo ss -u -a -n -p
```

This is useful when investigating which services have UDP sockets open.

## Lab 2: View listening UDP sockets

Run:

```bash
ss -u -l -n
```

Here, `-l` filters for listening sockets.

Remember that UDP does not have a TCP-style listening state or handshake. The command identifies sockets bound to local addresses and ports that are available to receive datagrams.

If you do not see port `53`, that does not automatically mean DNS is broken. Your machine might use a local resolver with a different configuration, or the relevant DNS service may not expose a socket in the way you expect.

## Lab 3: Observe DNS traffic

First, check which DNS configuration is active:

```bash
resolvectl status
```

This can show DNS servers associated with your network interfaces.

Next, check whether `dig` is installed:

```bash
command -v dig
```

If it is available, make a DNS query:

```bash
dig example.com
```

To request a typical UDP DNS query explicitly:

```bash
dig +notcp example.com
```

The query will commonly use UDP unless conditions require another behavior. The exact output depends on your DNS configuration and response.

If `dig` is not installed, you can install it on your Ubuntu-based Zorin system with:

```bash
sudo apt update
sudo apt install dnsutils
```

Package names may vary by distribution version, but `dnsutils` is commonly used on Ubuntu-derived systems.

### What did you learn?

You have now seen that:

- Applications use local sockets.
- UDP sockets are visible through `ss`.
- DNS can use UDP.
- The destination port helps the operating system deliver incoming datagrams to the appropriate application endpoint.

## Lab 4: Inspect a UDP packet with tcpdump

If you want to observe DNS traffic directly, use `tcpdump`.

First, check whether it is installed:

```bash
command -v tcpdump
```

Then start a capture:

```bash
sudo tcpdump -i any -nn 'udp port 53'
```

Open a second terminal and run:

```bash
dig +notcp example.com
```

Return to the first terminal to inspect the captured packets.

Useful options:

- `-i any` — capture on available interfaces.
- `-nn` — avoid resolving IP addresses and port numbers into names.
- `'udp port 53'` — capture UDP packets with source or destination port 53.

Stop the capture with `Ctrl+C`.

**Note:** This filter only matches traditional DNS traffic over UDP port 53. It will not necessarily capture DNS traffic carried over TCP, DNS over HTTPS, DNS over TLS, or other encrypted DNS transports.

Depending on your resolver configuration, the query may be sent to a local resolver first, which then contacts another DNS server. You might not see the exact traffic path you expected.

---

# 8. UDP and DevOps: Why You Need to Know This

Networking knowledge is valuable for cloud engineering because cloud services depend on communication between applications, hosts, and networks.

## Scenario 1: A DNS lookup fails on an EC2 instance

Imagine an application running on an AWS EC2 instance cannot resolve a domain name.

You need to investigate whether:

- The application is making DNS requests.
- The configured DNS resolver is reachable.
- UDP traffic is permitted where required.
- Routing and network configuration are correct.
- The DNS service is responding.
- The resolver is retrying or switching to TCP when appropriate.

In an AWS environment, network ACLs, security groups, routing, and DNS configuration may all matter.

**Important:** Security groups are stateful, while network ACLs are stateless. Their rules and the return path can affect whether DNS traffic succeeds.

## Scenario 2: A service is listening on the wrong protocol or port

Suppose a service is expected to receive UDP traffic on port `5000`, but a firewall rule only allows TCP port `5000`.

The service may appear to be configured for the correct port number, yet the traffic still fails.

Why?

Because **TCP port 5000 and UDP port 5000 are different transport endpoints**. Allowing one protocol does not automatically allow the other.

Useful Linux commands include:

```bash
ss -t -l -n
```

This checks TCP listening sockets.

```bash
ss -u -l -n
```

This checks UDP sockets bound for receiving datagrams.

## Scenario 3: A real-time application experiences poor quality

Suppose users complain that an online meeting is choppy.

You should investigate:

- Packet loss.
- Latency.
- Jitter.
- Bandwidth saturation.
- Firewall restrictions.
- NAT traversal.
- Whether the application is falling back to another transport path.

UDP can reduce some transport-related delays, but it cannot eliminate congestion or network packet loss.

## Scenario 4: A Kubernetes application cannot communicate with another service

A Kubernetes environment may have services and applications communicating over UDP or TCP, depending on their design.

When troubleshooting, verify:

1. Which transport protocol the application uses.
2. Which port the application actually binds to.
3. Whether the Kubernetes Service declares the correct protocol and port.
4. Whether network policies or firewalls permit the traffic.
5. Whether the receiving application is handling the datagrams correctly.

For example, a service configured for UDP will not become reachable merely because a TCP port with the same numerical value is allowed.

---

# 9. Common Mistakes to Avoid

| Mistake | Correct understanding |
|---|---|
| UDP has zero overhead. | UDP has an 8-byte header, in addition to IP and link-layer overhead. |
| UDP guarantees faster communication than TCP. | UDP has low transport overhead, but actual performance depends on the application and network. |
| UDP never needs reliability. | Applications using UDP can implement reliability when needed. |
| UDP cannot support ongoing sessions. | Applications can maintain session state independently of UDP's transport behavior. |
| UDP does not use ports. | UDP uses source and destination ports. |
| All DNS traffic uses UDP. | DNS can use UDP or TCP, and modern DNS also uses other transport arrangements. |
| UDP packets always arrive in order. | UDP provides no ordering guarantee. |
| UDP cannot lose packets. | UDP itself provides no delivery guarantee or retransmission. |
| TCP and UDP port 53 are interchangeable. | They are distinct transport endpoints. A service and firewall must support the required protocol. |
| QUIC is just ordinary unreliable UDP. | QUIC implements its own reliability, congestion control, encryption, and stream mechanisms over UDP. |

---

# 10. Interview Questions and Answers

### Q1. What is UDP?

UDP, or User Datagram Protocol, is a connectionless transport-layer protocol that sends datagrams using source and destination port numbers. It has a small header and does not provide built-in reliable delivery or ordered delivery.

### Q2. Which OSI layer does UDP belong to?

UDP belongs to Layer 4, the Transport Layer.

### Q3. What is the size of the UDP header?

The UDP header is **8 bytes**, consisting of four 16-bit fields: source port, destination port, length, and checksum.

### Q4. Why is UDP called connectionless?

UDP does not establish a transport connection through a handshake before sending datagrams. It also does not maintain TCP-style connection state.

### Q5. Does UDP guarantee packet delivery?

No. UDP itself does not guarantee delivery, ordering, or retransmission.

### Q6. What is the purpose of a UDP port?

A UDP port helps the operating system deliver an incoming datagram to the appropriate local application socket.

### Q7. Why is UDP useful for online gaming?

Gaming often requires frequent, time-sensitive updates. Losing an old position update may be preferable to waiting for retransmission when a newer update is already available.

### Q8. Why does DNS commonly use UDP?

Many DNS queries are small request-response exchanges. UDP allows them to be sent without establishing a TCP connection first. DNS can also use TCP when required.

### Q9. Can UDP be reliable?

UDP does not provide reliability itself, but an application or higher-level protocol can implement acknowledgments, retransmissions, sequencing, and other reliability mechanisms.

QUIC is an important example.

### Q10. What is the TCP-over-TCP problem?

It is a performance problem that can occur when TCP traffic is tunneled through another TCP connection. The two layers' retransmission and congestion-recovery mechanisms can interact poorly under packet loss.

Using UDP for the outer VPN tunnel can avoid that additional TCP reliability layer.

### Q11. What is the difference between a UDP port and an IP address?

An IP address helps identify the network-layer destination. A UDP port identifies the transport endpoint associated with an application on that destination.

### Q12. What is QUIC?

QUIC is a transport protocol built on UDP that implements its own mechanisms for reliable streams, congestion control, encryption, and other transport functionality. HTTP/3 uses QUIC.

---

# 11. Lecture 14 — Quick Revision Cheat Sheet

Memorize these core facts:

```text
UDP
 |
 +-- Full form: User Datagram Protocol
 |
 +-- OSI layer: Layer 4 (Transport)
 |
 +-- Data unit: Datagram
 |
 +-- Header size: 8 bytes
 |
 +-- Ports: Source port + Destination port
 |
 +-- Connection handshake: No
 |
 +-- Built-in retransmission: No
 |
 +-- Built-in ordering: No
 |
 +-- Delivery guarantee: No
 |
 +-- Common uses:
       - DNS
       - Real-time audio/video
       - Multiplayer gaming
       - Some VPN configurations
       - QUIC / HTTP/3
```

### The most important concept

**UDP is lightweight because it leaves many transport responsibilities to the application or higher-level protocol.**

This makes it useful when low latency and control over communication behavior matter. It does not mean that UDP traffic cannot be reliable; it means that UDP itself does not provide TCP-style reliability.

---

# 12. Practice Exercises

Try these questions to strengthen your understanding.

### Exercise 1: Basic concepts

Answer the following:

1. What does UDP stand for?
2. Which transport-layer information does UDP add to an application message?
3. How many bytes long is the UDP header?
4. Does UDP perform a three-way handshake?
5. Does UDP automatically retransmit a lost datagram?

### Exercise 2: Understand the ports

A client sends a DNS query with the following details:

```text
Client IP:        192.168.1.10
Client UDP port:  53000

DNS server IP:    192.168.1.53
DNS server port:  53
```

Answer:

1. What is the destination UDP port of the query?
2. Which port identifies the client's local transport endpoint?
3. What are the source and destination ports in a typical response?
4. Why does the client need a port number if it already knows the DNS server's IP address?

### Exercise 3: Choose the transport

For each situation, explain why UDP or TCP might be appropriate.

1. A real-time multiplayer game's frequent position updates.
2. An SSH session to a Linux server.
3. A DNS lookup.
4. A protocol that needs reliable, ordered stream delivery but is designed to run over UDP.

### Exercise 4: Linux practice

Run:

```bash
ss -u -a -n
```

Then run:

```bash
ss -t -a -n
```

Explain the difference between the two outputs.

Next, if `dig` is installed, run:

```bash
dig +notcp example.com
```

Identify the query's transport protocol and the DNS server's port.

### Exercise 5: Troubleshooting

An application sends UDP datagrams to port `5000`, but the server does not receive them.

List at least five things you would check.

Think about:

- The server's socket.
- The destination IP address.
- The transport protocol.
- Routing.
- Firewall rules.
- Packet capture.
- Application behavior.

---

## Answers for Self-Verification

**Exercise 1**

1. User Datagram Protocol.
2. Source port, destination port, length, and checksum fields.
3. 8 bytes.
4. No.
5. No, not by itself.

**Exercise 2**

1. Destination port `53`.
2. Source port `53000`.
3. Source port `53`, destination port `53000`, assuming the same endpoints and no relevant translation.
4. The IP address identifies the network-layer destination; the port helps the operating system deliver data to the appropriate application socket.

**Exercise 3**

1. UDP is often suitable because frequent updates are latency-sensitive and some loss may be acceptable.
2. TCP is appropriate because SSH needs reliable, ordered delivery.
3. UDP is commonly used for DNS queries, though DNS also supports TCP.
4. QUIC is an example of a protocol that implements reliable streams and other transport features over UDP.

**Exercise 4**

- `ss -u -a -n` shows UDP sockets.
- `ss -t -a -n` shows TCP sockets.
- A typical DNS query uses UDP destination port `53`, though DNS may use TCP or another transport depending on the configuration and situation.

**Exercise 5**

Possible checks:

1. Verify the server is listening or has a UDP socket bound to the expected address and port.
2. Confirm the client is using UDP, not TCP.
3. Verify the destination IP address and port.
4. Check the routing table and network reachability.
5. Check host firewalls and network firewalls.
6. Check cloud security groups and network ACLs if applicable.
7. Capture traffic with `tcpdump` on the client and server.
8. Confirm the application can process the incoming datagrams.
9. Check for packet loss, overload, or network-policy restrictions.
10. Remember that UDP provides no built-in delivery guarantee or acknowledgment.

---

## What Comes Next?

**Lecture 14 is complete.**

You now understand UDP, its 8-byte header, connectionless behavior, ports, real-world use cases, and how UDP datagrams travel through IP networks.

