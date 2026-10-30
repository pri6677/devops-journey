# Networking for DevOps — Lecture 11
# OSI Model, TCP/IP Model, and the Journey of a Packet

**Roadmap position:** Networking → Lecture 11  
**Previous lecture:** Lecture 10 — ARP (Address Resolution Protocol)  
**Today's goal:** Understand how data travels from an application on one computer to an application on another, how the OSI layers work together, and how this knowledge helps troubleshoot real-world networking problems.

By the end of this lesson, you'll understand why an HTTP request needs ports, IP addresses, MAC addresses, and physical signals to reach its destination.

---

# 1. What Is the OSI Model?

**OSI** stands for **Open Systems Interconnection**.

It is a conceptual framework that divides network communication into **seven layers**. Each layer has a particular responsibility, making it easier to understand, design, and troubleshoot networks.

Think about sending a parcel to someone:

1. You prepare the contents.
2. You package and label the parcel.
3. A delivery service determines where it should go.
4. The parcel travels through different transportation networks.
5. It eventually reaches the recipient.

Network communication works similarly. Different layers perform different jobs to deliver data from a source application to a destination application.

## The Seven OSI Layers



| Layer | Number | Name | Main responsibility | Common examples |
|---|---:|---|---|---|
| 7 | Application | Application | Provides network services to applications | HTTP, SMTP, FTP, SSH |
| 6 | Presentation | Presentation | Data representation, encryption, compression | UTF-8, TLS, gzip |
| 5 | Session | Session | Manages communication sessions | Session management, RPC |
| 4 | Transport | Transport | Process-to-process delivery | TCP, UDP, port numbers |
| 3 | Network | Network | IP addressing and routing | IPv4, IPv6, ICMP |
| 2 | Data Link | Data Link | Local network delivery using frames and MAC addresses | Ethernet, Wi-Fi link layer |
| 1 | Physical | Physical | Transmits bits as physical signals | Radio waves, electrical signals, optical signals |

**Remember:** Layer 7 is at the top, closest to the application. Layer 1 is at the bottom, closest to the physical transmission medium.

Let's understand each layer from top to bottom, following your lecture.

---

# 2. Layer 7 — Application Layer

## What does it do?

The Application Layer provides network communication services to applications.

It is the layer closest to the software you use directly.

For example, when you:
- Open a website in a browser.
- Connect to a remote Linux server using SSH.
- Send an email.
- Download a file from a server.
- Make an HTTP request from a React application.

Your application uses network protocols and software libraries to communicate.

### Common protocols

| Protocol | Purpose |
|---|---|
| HTTP | Transfers web requests and responses |
| HTTPS | HTTP protected using TLS |
| SMTP | Sends email |
| FTP | Transfers files |
| SSH | Secure remote access to computers |

### Example: Opening a website

Suppose you enter a website address into your browser.

Your browser uses HTTP or HTTPS to request resources from a web server.

A simplified HTTP request might look like this:

```http
GET / HTTP/1.1
Host: example.com
```

This tells the server that the client wants to retrieve the resource at `/`.

The browser does not independently transmit this text as electrical signals. Other networking components and layers are involved in getting the request to the server.

### DevOps connection

As a DevOps engineer, you'll frequently work with application-layer tools:

```bash
curl https://example.com
```

`curl` sends an HTTP request and displays the response.

You might use it to check whether an application is responding correctly after deployment.

For example:

```bash
curl -I https://example.com
```

The `-I` option requests response headers without downloading the full response body.

If the application returns an HTTP status such as `200`, `301`, `403`, or `500`, that gives you useful information about the HTTP-level result.

However, a successful HTTP response doesn't necessarily mean every component of the application is healthy.

**Key takeaway:** The Application Layer concerns the network services and protocols used by applications.

---

# 3. Layer 6 — Presentation Layer

## What does it do?

The Presentation Layer concerns how data is represented so that communicating systems can interpret it correctly.

Your lecture covers three important functions:

1. Text encoding
2. Encryption and decryption
3. Compression and decompression

Let's examine each one.

## A. Text encoding

Computers process data as bits. Text must be represented in a form that software can encode and decode consistently.

**UTF-8** is a widely used text encoding.

For example:

```text
Hello
```

A computer represents the characters using an agreed encoding. If the sender and receiver interpret the bytes differently, the resulting text may be incorrect.

Encoding and encryption are different:

- **Encoding** represents data in an agreed format.
- **Encryption** transforms data so that it cannot ordinarily be understood without the appropriate key.

Encoding alone does not provide security.

## B. Encryption and decryption

Encryption protects data from being read by unauthorized parties.

HTTPS uses **TLS** (Transport Layer Security) to protect HTTP communication.

A simplified example:

```text
HTTP data
    ↓
TLS protection
    ↓
Protected data sent across the network
```

At the receiving end, the TLS implementation verifies and decrypts the protected data as appropriate.

Your lecture associates encryption with OSI Layer 6. This is a useful conceptual placement, although real-world TLS does not map perfectly to one OSI layer.

## C. Compression

Compression reduces the size of data.

Common examples include:

- gzip
- zlib

Suppose an application needs to transfer a large response. Compression may reduce the number of bytes that must be transmitted.

```text
Original data: 100 KB
       ↓ Compression
Compressed data: 30 KB
```

These figures are only illustrative; the actual reduction depends on the data.

### DevOps connection

You may configure:
- HTTPS certificates on web servers.
- TLS settings on reverse proxies.
- HTTP compression in applications or proxies.
- Secure communication between services.

For example, a reverse proxy might terminate TLS, process an HTTPS connection, and forward a request to an internal application.

**Key takeaway:** The Presentation Layer is a useful way to think about data representation, encryption, and compression.

---

# 4. Layer 5 — Session Layer

## What does it do?

The Session Layer represents the functions involved in establishing, managing, and ending communication sessions between applications.

Your lecture mentions:
- Session management
- Authentication state
- Remote Procedure Calls (RPC)
- Checkpointing during file transfers

Let's understand these ideas.

## A. Session management

Imagine logging into an application.

The application may establish a session that allows it to recognize subsequent requests as belonging to the same logged-in user.

A simplified flow:

```text
User logs in
     ↓
Application validates credentials
     ↓
Session or token is established
     ↓
Subsequent requests carry session information
```

A crucial distinction: **login sessions and HTTP sessions are application-level concepts in modern systems**, even though they help illustrate the Session Layer's conceptual role.

## B. Remote Procedure Call (RPC)

RPC allows software to invoke a function or operation on another system as though it were calling a local function.

For example:

```text
Application A
      |
      | Request: get_user(10)
      v
Application B
      |
      | Returns user data
      v
Application A
```

The actual request must still travel through the network. RPC frameworks handle the details of communicating between the systems.

RPC is a communication pattern or mechanism, not one universal protocol assigned exclusively to OSI Layer 5.

## C. File-transfer checkpointing

Imagine transferring a very large file.

If the connection fails after 80% of the file has transferred, a transfer system that supports checkpoints may resume from a saved position rather than restarting from the beginning.

This is another example of managing the state of an ongoing operation. The exact implementation depends on the protocol or application.

### DevOps connection

In cloud and distributed systems, you will encounter:
- Application sessions.
- Session persistence behind load balancers.
- RPC-based communication between services.
- Distributed applications that need to maintain state.

For example, if an application stores session data only in one server's memory, sending the user's next request to another server might cause a problem. Teams may use shared session storage or appropriate token-based approaches to handle this.

**Key takeaway:** The Session Layer provides a conceptual way to understand the management of ongoing communication.

---

# 5. Layer 4 — Transport Layer

This is one of the most important layers for DevOps engineers.

The Transport Layer provides communication between application processes running on different hosts.

The two major transport protocols you'll study are **TCP and UDP**.

## A. TCP — Transmission Control Protocol

TCP provides a reliable, ordered byte stream.

Its important features include:
- Establishing a connection.
- Retransmitting lost data when necessary.
- Delivering data in order.
- Detecting transmission errors.
- Using flow control and congestion control.

For example, HTTPS commonly uses TCP when running over HTTP/1.1 or HTTP/2.

A simplified TCP connection establishment is called the **three-way handshake**:

```text
Client                     Server
   |                          |
   |-------- SYN ------------>|
   |                          |
   |<----- SYN + ACK ----------|
   |                          |
   |-------- ACK ------------>|
   |                          |
   |   TCP connection ready   |
```

The handshake establishes the TCP connection before application data is exchanged.

This is a simplified view; real connections have additional details and states.

## B. UDP — User Datagram Protocol

UDP sends independent datagrams without establishing a TCP-style connection.

UDP does not itself guarantee:
- Delivery
- In-order arrival
- Retransmission of lost datagrams

Applications can implement reliability themselves if they need it.

UDP is used in situations where low overhead or application-controlled delivery behavior is useful.

Examples include:
- DNS queries in common configurations.
- Many real-time audio/video systems.
- HTTP/3, which uses QUIC over UDP.

## TCP vs UDP

| Feature | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented | Connectionless |
| Delivery guarantee | Provides reliable delivery | No built-in delivery guarantee |
| Ordering | Preserves byte order | No built-in ordering guarantee |
| Retransmission | Built in | Must be handled by the application if needed |
| Data representation | Byte stream | Individual datagrams |
| Examples | HTTPS over HTTP/1.1 or HTTP/2 | DNS in common cases, QUIC transport |

### Important: What is a port number?

An IP address identifies a network interface or host destination in a network context. A port number helps the operating system deliver incoming transport traffic to the appropriate application endpoint.

For example:

```text
192.168.1.1:3000
```

Here:
- `192.168.1.1` is the IP address.
- `3000` is the port number.

A server might listen on port `443` for HTTPS traffic.

Ports are associated with TCP or UDP; a TCP port and a UDP port with the same number are separate endpoints.

### Example

Imagine a server running two services:

```text
Server IP: 10.0.0.1

HTTPS service: TCP port 443
Application service: TCP port 3000
```

The IP address helps route packets to the server. The transport protocol and port help the operating system deliver traffic to the appropriate service.

### Linux practical

Check listening TCP and UDP sockets:

```bash
ss -tuln
```

Meaning:

- `ss`: displays socket information.
- `-t`: TCP sockets.
- `-u`: UDP sockets.
- `-l`: listening sockets.
- `-n`: numeric addresses and ports.

To see process information, you can use:

```bash
sudo ss -tulpn
```

Some process details may require elevated privileges.

### DevOps troubleshooting example

Suppose your application should listen on port `3000`, but users cannot reach it.

Check:

```bash
ss -tuln
```

If nothing is listening on the expected port, investigate whether the application started correctly and whether it is configured to listen on the expected address and port.

If the service is listening, the issue might instead involve:
- A host firewall.
- A cloud security group.
- A routing problem.
- A container port mapping.
- A reverse proxy.
- An incorrect destination address.

**Key takeaway:** The Transport Layer helps deliver data to the correct application endpoint using protocols such as TCP and UDP and their port numbers.

---

# 6. Layer 3 — Network Layer

The Network Layer is responsible for logical addressing and routing packets between networks.

This is where **IP addresses and routers** become central.

You already studied IP addressing, subnets, default gateways, and routers in Lectures 3–7.

Let's connect those lessons to the OSI model.

## A. IP addressing

Suppose a frontend application communicates with a backend server:

```text
Frontend: 192.168.1.1
Backend:  10.0.0.1
```

These addresses belong to different IPv4 networks in this example.

The sender uses its routing information to determine how to reach the destination.

Because the destination is remote, the sender generally sends the packet to the appropriate next hop, often its default gateway.

## B. Routing

Routers forward IP packets between networks.

A simplified journey:

```text
Frontend
192.168.1.1
     |
     v
Local router
     |
     v
Intermediate networks
     |
     v
Backend network
     |
     v
Backend server
10.0.0.1
```

Each router examines the packet's destination IP address and uses its routing information to determine where to forward it.

Actual networks can contain many routers and intermediate devices.

## C. ICMP, ping, and traceroute

Your lecture includes ICMP, `ping`, and `traceroute`.

**ICMP** is used for network control, error reporting, and diagnostic purposes.

On Linux, try:

```bash
ping -c 4 8.8.8.8
```

This sends four ping requests to the destination.

A response can help establish that ICMP echo communication works along the path, but a failed ping does not prove that the destination is completely unreachable. Firewalls and network policies may block ICMP while allowing other traffic.

You can also run:

```bash
traceroute 8.8.8.8
```

If `traceroute` is installed, it attempts to reveal intermediate hops along the route.

If the command is unavailable on Zorin OS, you can check for it with:

```bash
command -v traceroute
```

Some systems use `tracepath` instead:

```bash
tracepath 8.8.8.8
```

Traceroute results can contain unanswered hops because routers may not respond to the probes. This does not necessarily mean the network path is broken.

## D. What is the Layer 3 data unit?

At this layer, the data unit is commonly called an **IP packet**.

For IPv4, the IP header contains information such as:
- Source IP address.
- Destination IP address.
- TTL (Time to Live).
- Protocol identifying the next-layer payload, such as TCP or UDP.

### What happens to the IP packet when it crosses a router?

Normally, the source and destination IP addresses remain the same across routed hops, unless something such as Network Address Translation (NAT) modifies them.

The router decreases the IPv4 TTL when forwarding the packet. If the TTL expires, the packet is discarded.

The router then creates a new Layer 2 frame for the outgoing link.

This leads directly to the next layer.

**Key takeaway:** The Network Layer is responsible for logical addressing and routing packets between networks.

---

# 7. Layer 2 — Data Link Layer

The Data Link Layer handles communication across a local network link.

It uses **frames** and, on Ethernet and Wi-Fi links, MAC addressing to deliver frames to the appropriate local destination.

You already studied MAC addresses in Lecture 8, IP versus MAC in Lecture 9, and ARP in Lecture 10.

Now let's connect them.

## A. MAC addresses

A typical MAC address looks like this:

```text
AA:BB:CC:11:22:33
```

For Ethernet, a MAC address is normally 48 bits long.

MAC addresses help network interfaces identify the sender and intended recipient of frames on the local link.

## B. Frames

An Ethernet frame contains fields including:
- Destination MAC address.
- Source MAC address.
- Payload, which may carry an IP packet.
- Error-detection information.

A simplified representation:

```text
+---------------------+
| Destination MAC     |
+---------------------+
| Source MAC          |
+---------------------+
| Type / Length       |
+---------------------+
| Payload: IP packet  |
+---------------------+
| Frame check sequence|
+---------------------+
```

This is a simplified illustration, not a complete description of every Ethernet frame format.

## C. What does a switch do?

An Ethernet switch learns which MAC addresses are reachable through its ports and uses that information to forward frames within a local network.

For example:

```text
Computer A
MAC: AA:AA:AA:AA:AA:AA
       |
       v
     Switch
       |
       v
Computer B
MAC: BB:BB:BB:BB:BB:BB
```

If the switch knows which port leads to Computer B, it can forward the frame through that port.

## D. What happens when traffic crosses a router?

This is a key concept from Lecture 12.

Suppose the frontend sends a packet to a remote backend.

On the frontend's local network, the frame might look like this:

```text
Source MAC:      Frontend's MAC
Destination MAC: Gateway's MAC

Payload:
  Source IP:      192.168.1.1
  Destination IP: 10.0.0.1
```

The destination MAC is the gateway's MAC, **not the remote backend's MAC**.

The router receives the frame, removes the incoming Layer 2 framing, examines the IP packet, and forwards the packet using a new frame on the outgoing link.

Conceptually:

```text
First link:
Frontend MAC → Router MAC

Next link:
Router's outgoing MAC → Next-hop MAC
```

The exact MAC addresses change according to each link. The IP addresses normally remain unchanged, except when address translation or another relevant mechanism modifies them.

### Linux practical

Display network interfaces and MAC addresses:

```bash
ip link show
```

Inspect your routing table:

```bash
ip route
```

Display neighboring devices and their IP-to-link-layer mappings:

```bash
ip neigh show
```

These commands connect your earlier lessons on interfaces, routing, and ARP.

**Key takeaway:** The Data Link Layer handles local link delivery using frames. Routers create new frames when forwarding packets across links.

---

# 8. Layer 1 — Physical Layer

The Physical Layer concerns the actual transmission of bits over a physical medium.

Examples include:

- Electrical signals travelling over copper Ethernet cables.
- Radio waves carrying Wi-Fi signals.
- Light signals travelling through fiber-optic cables.

At this level, the focus is on transmitting and receiving bits rather than interpreting IP addresses or HTTP requests.

Consider this simplified chain:

```text
Application data
      ↓
TCP segment
      ↓
IP packet
      ↓
Ethernet frame
      ↓
Bits transmitted as physical signals
```

The receiving system detects the signals and reconstructs the transmitted bits.

### Does this mean the entire internet uses Ethernet cables?

No.

Ethernet may be used on local wired networks, while Wi-Fi uses radio communication on the wireless link. Other technologies can carry data across other parts of a network.

The higher-level protocols allow applications to communicate without needing to know every detail of the underlying physical medium.

### DevOps connection

Physical-layer problems can include:
- A disconnected Ethernet cable.
- A faulty network adapter.
- Weak or interrupted Wi-Fi.
- A physical switch or port failure.
- A damaged fiber connection.

Cloud users typically do not manage the physical network directly, but understanding the layer helps distinguish physical connectivity issues from routing or application problems.

**Key takeaway:** The Physical Layer transmits bits using the underlying physical medium.

---

# 9. Why Are Networking Layers Separated?

Your lecture emphasizes that layer separation allows one part of the system to change without requiring every other part to change.

This is called **abstraction**.

Imagine that you develop a Node.js application.

Your code might make an HTTP request:

```javascript
fetch("https://example.com");
```

The application does not need to implement radio transmission, Ethernet framing, or router forwarding itself.

Other parts of the system handle those responsibilities.

The same application can potentially communicate over:
- Wi-Fi.
- Ethernet.
- Fiber-backed networks.
- A virtual network interface.

The application code usually doesn't need to change just because the underlying network connection changes.

## What if one layer changes?

| Change | What usually remains independent? |
|---|---|
| Switch from Wi-Fi to Ethernet | Application logic |
| Change the router's route configuration | Application code |
| Change the application listening port | Physical transmission technology |
| Replace a copper link with a fiber link | HTTP request structure |

These are conceptual examples. Some changes still require configuration updates. For example, changing a service's port may require updates to firewall rules, reverse-proxy configuration, or client settings.

**The main idea:** Layers divide responsibilities, making networks easier to build, maintain, and troubleshoot.

---

# 10. OSI Model vs. TCP/IP Model

The OSI model is a seven-layer conceptual framework. The TCP/IP model describes the architecture commonly used to understand internet communication.

Your lecture uses the **five-layer TCP/IP teaching model**.

## Comparing the models

| OSI Model | Five-layer TCP/IP Model | Examples |
|---|---|---|
| Layer 7 — Application | Application | HTTP, SSH, SMTP |
| Layer 6 — Presentation | Application | Data representation, TLS-related functions, compression |
| Layer 5 — Session | Application | Session-management concepts |
| Layer 4 — Transport | Transport | TCP, UDP |
| Layer 3 — Network | Network | IP, ICMP |
| Layer 2 — Data Link | Data Link | Ethernet, Wi-Fi link-layer framing |
| Layer 1 — Physical | Physical | Radio waves, electrical and optical signals |

### Why does TCP/IP merge the top three OSI layers?

In practical networking, application software and libraries commonly handle functions that the OSI model separates into Session, Presentation, and Application layers.

For example, a web application may rely on:
- HTTP libraries for application communication.
- TLS libraries for encrypted communication.
- Application code for login sessions.
- Compression libraries or middleware for compression.

These functions are not always implemented as three distinct layers.

That is why the five-layer model groups the top three OSI layers under a single **Application Layer**.

### Important nuance

You may also encounter a **four-layer TCP/IP model**. In that version, the Data Link and Physical layers are grouped into a single Link or Network Access layer.

Therefore, don't assume every book or course uses exactly the same number of TCP/IP layers.

For your current lecture, use the five-layer model:

1. Application
2. Transport
3. Network
4. Data Link
5. Physical

---

# 11. Encapsulation — How Data Travels Through the Layers

Now let's connect the concepts.

When an application sends data, each layer adds the information needed for its own responsibility. This process is called **encapsulation**.

At the receiving end, the layers interpret and remove their respective protocol information. This is called **decapsulation**.

## Encapsulation from top to bottom

```text
Application Layer
       |
       | Application data
       v
Transport Layer
       |
       | TCP segment or UDP datagram
       v
Network Layer
       |
       | IP packet
       v
Data Link Layer
       |
       | Frame
       v
Physical Layer
       |
       | Bits transmitted as signals
       v
     NETWORK
```

A simplified way to remember the process:

| Layer | Data unit |
|---|---|
| Application | Data |
| Presentation | Data |
| Session | Data |
| Transport | TCP segment / UDP datagram |
| Network | IP packet |
| Data Link | Frame |
| Physical | Bits |

The exact terminology can vary by protocol and textbook. For example, a TCP segment and a UDP datagram are not the same thing.

## What does each layer add?

Imagine that a browser sends an HTTP request.

### Step 1: Application data

The application creates an HTTP request.

```http
GET / HTTP/1.1
Host: example.com
```

### Step 2: Transport information

TCP adds its header, which includes source and destination ports and other information needed for TCP communication.

```text
[TCP header][HTTP data]
```

The resulting data unit is a TCP segment.

### Step 3: IP information

IP adds its own header, including source and destination IP addresses.

```text
[IP header][TCP header][HTTP data]
```

The result is an IP packet.

### Step 4: Data Link information

The local link layer adds framing information, including source and destination MAC addresses on an Ethernet link.

```text
[Ethernet header][IP header][TCP header][HTTP data][trailer]
```

This forms an Ethernet frame.

### Step 5: Physical transmission

The frame is encoded into bits and transmitted using the underlying link technology.

The receiving system reverses the process to deliver the data to the appropriate application.

**Important:** The diagram simplifies the protocol stack. Real implementations may include additional headers, options, tunnels, encryption layers, and other encapsulation.

---

# 12. Complete Packet Journey: React Frontend to Backend Server

Your lecture uses this example:

- Frontend: `192.168.1.1:3000`
- Backend: `10.0.0.1:443`

Let's trace the request.

These addresses and ports are illustrative. We'll assume the frontend is using TCP to connect to the backend on port `443`, with routing and security rules configured to allow the connection.

One important distinction: port `443` is commonly used for HTTPS, but the port number alone does not prove that the service is using HTTPS.

## Step 1: The frontend creates a request

Imagine a frontend application needs information from the backend.

```text
Frontend IP:   192.168.1.1
Frontend port: 3000

Backend IP:    10.0.0.1
Backend port:  443
```

The application creates the request.

The frontend's source port might be an automatically selected ephemeral port rather than `3000`.

**Why?** In this example, `3000` identifies the frontend application's listening service. If that application initiates an outgoing connection, the operating system normally selects a separate local source port for that connection.

For clarity, let's represent the connection as:

```text
Frontend: 192.168.1.1:52000
Backend:  10.0.0.1:443
```

Here, `52000` is an illustrative client-side ephemeral port.

## Step 2: Transport Layer

The frontend establishes a TCP connection if the application protocol requires TCP.

The TCP segment contains transport information, including the source and destination ports.

```text
Source:      192.168.1.1:52000
Destination: 10.0.0.1:443
```

The TCP segment is handed to IP for delivery.

## Step 3: Network Layer

The IP packet contains:

```text
Source IP:      192.168.1.1
Destination IP: 10.0.0.1
```

The operating system checks its routing information to decide where to send the packet.

Because the backend is on a different network in this example, the packet must be forwarded through a suitable next hop.

## Step 4: Data Link Layer

Suppose the frontend's default gateway is `192.168.1.254`.

The frontend needs the gateway's MAC address to send the frame across its local Ethernet link.

It may already have the mapping in its neighbor cache. Otherwise, it can use ARP to discover the gateway's MAC address.

The resulting frame is conceptually:

```text
Ethernet frame
┌────────────────────────────────────┐
│ Source MAC:      Frontend MAC       │
│ Destination MAC: Gateway MAC        │
├────────────────────────────────────┤
│ IP packet                          │
│  Source IP:      192.168.1.1        │
│  Destination IP: 10.0.0.1           │
└────────────────────────────────────┘
```

Notice the difference:

- **Destination MAC:** the next hop on the local link.
- **Destination IP:** the final IP destination, the backend.

This distinction is central to understanding how routing works.

## Step 5: Physical Layer

The frame is transmitted over the local link.

If the frontend uses Wi-Fi, the wireless link uses radio signals. If it uses Ethernet, the frame is transmitted over the wired link.

The router receives the traffic and processes it.

## Step 6: The router forwards the packet

The router examines the destination IP address and consults its routing information.

If it has a valid route and forwarding is permitted, it forwards the packet towards the backend network.

For each routed link, the router sends a new Layer 2 frame appropriate to the outgoing interface and next hop.

```text
Frontend
   |
   | Frame addressed to local gateway
   v
Router
   |
   | New frame on outgoing link
   v
Next hop / network path
   |
   v
Backend network
   |
   v
Backend server
```

The IP packet's source and destination addresses normally remain the same, except where mechanisms such as NAT modify them.

## Step 7: The backend receives the packet

At the destination network, the final link delivers a frame to the backend's network interface.

The backend processes the received information:

1. The Data Link Layer processes the frame.
2. The Network Layer processes the IP packet.
3. The Transport Layer processes the TCP segment.
4. TCP delivers the byte stream to the application associated with the connection.
5. The application processes the request.

If the connection uses HTTPS, TLS processing also occurs before the HTTP request is delivered to the application in readable form.

The exact internal ordering depends on implementation, but the layered model is useful for understanding the responsibilities involved.

## Step 8: The backend sends a response

The backend processes the request and creates a response.

The response travels back through the networking stack.

Conceptually:

```text
Backend application
       |
       v
Transport Layer
       |
       v
Network Layer
       |
       v
Data Link Layer
       |
       v
Physical Layer
       |
       v
Network path back to frontend
```

The response uses the established connection, with the backend's port `443` as the server-side source port and the client's ephemeral port as the destination port.

The frontend then receives and processes the response.

### Complete flow at a glance

```text
FRONTEND APPLICATION
192.168.1.1
     |
     | Create request
     v
TRANSPORT
TCP: client-port → 443
     |
     v
NETWORK
IP: 192.168.1.1 → 10.0.0.1
     |
     v
DATA LINK
MAC: frontend → local gateway
     |
     v
PHYSICAL
Bits transmitted over local link
     |
     v
ROUTER / NETWORK PATH
Routing and new frames at routed hops
     |
     v
BACKEND SERVER
10.0.0.1:443
     |
     | Decapsulation and application processing
     v
BACKEND RESPONSE
     |
     v
REVERSE COMMUNICATION FLOW
     |
     v
FRONTEND RECEIVES RESPONSE
```

**The key concept:** The request is not sent directly from the frontend application to the backend application in one step. Multiple protocols and layers cooperate to deliver it.

---

# 13. Hands-On Linux Lab: Observe the Layers on Zorin OS

Now let's connect this lecture to your actual Linux environment.

You don't need to configure anything for these initial checks.

## Lab 1: Inspect network interfaces

Run:

```bash
ip link show
```

This displays your network interfaces and their link-layer information.

You may see interfaces such as:

```text
lo
wlp2s0
docker0
```

The names depend on your machine and installed software.

- `lo`: loopback interface.
- `wlp2s0`: an example wireless interface name.
- `docker0`: a Docker bridge interface, if Docker has created it.

Your actual interface names may differ.

**Related layers:** Mainly Layer 2 and Layer 3 information, depending on the fields you inspect.

## Lab 2: Inspect IP addresses

Run:

```bash
ip addr show
```

Look for lines containing `inet`, such as:

```text
inet 192.168.1.10/24
```

This represents an IPv4 address with a `/24` prefix.

You studied how the prefix determines the network portion of an address in Lectures 4 and 5.

**Related layer:** Layer 3.

## Lab 3: Inspect the routing table

Run:

```bash
ip route
```

You might see entries similar to:

```text
default via 192.168.1.1 dev wlp2s0
192.168.1.0/24 dev wlp2s0
```

These are illustrative examples; your actual output may be different.

The first line represents a default route through a gateway. The second indicates a directly connected network.

**Related layer:** Layer 3.

## Lab 4: Inspect neighbor mappings

Run:

```bash
ip neigh show
```

You may see entries containing IP addresses, link-layer addresses, and states such as `REACHABLE` or `STALE`.

This is related to your Lecture 10 lesson on ARP and the Linux neighbor table.

**Related layer:** The command exposes neighbor information used for local link delivery.

## Lab 5: Check an HTTP response

Run:

```bash
curl -I https://example.com
```

If your internet connection and the remote service allow the request, `curl` should display HTTP response headers.

This tests several parts of the communication process, including name resolution if required, network connectivity, transport communication, TLS, and HTTP.

If it fails, the error message can help narrow down the problem. A failure does not automatically identify which layer is responsible.

**Related layer:** Application-level request, relying on lower-layer services.

---

# 14. DevOps Troubleshooting: Which Layer Should You Investigate?

Knowing the layers helps you avoid troubleshooting the wrong part of a system.

| Symptom | Possible area to investigate | Useful checks |
|---|---|---|
| Wi-Fi is disconnected | Physical/link connectivity | Desktop network settings, `ip link` |
| Interface has no expected IP address | Network configuration | `ip addr show` |
| Cannot reach a remote network | Routing | `ip route`, `ip route get <IP>` |
| Cannot resolve a domain name | DNS/application configuration | `getent hosts example.com`, `resolvectl status` |
| Connection is refused on a port | Service or transport endpoint | `ss -tuln`, application logs |
| Connection times out | Several possibilities, including routing or filtering | `ip route`, firewall and cloud rules, `curl -v` |
| TCP connection works, but HTTPS fails | TLS, certificate, or application configuration | `curl -v https://example.com` |
| HTTP returns `500` | Server-side application or dependency issue | Application logs, service health |
| Works locally but not from the internet | Binding, routing, firewall, cloud, or proxy configuration | `ss -tuln`, routes, security rules |

These are **starting points, not one-to-one diagnoses**. The same symptom can originate from different layers.

For example, a connection timeout could be caused by a routing issue, a firewall dropping packets, a server that is unavailable, or a service listening only on a different interface.

A DevOps engineer narrows the possibilities using evidence.

---

# 15. Interview Questions and Answers

## Q1. What is the OSI model?

The OSI model is a seven-layer conceptual framework for understanding network communication. It separates networking functions into layers so they can be studied and troubleshot independently.

## Q2. Name the seven OSI layers from bottom to top.

1. Physical
2. Data Link
3. Network
4. Transport
5. Session
6. Presentation
7. Application

## Q3. What is the difference between Layer 2 and Layer 3?

Layer 2 handles local link delivery using frames and link-layer addressing, such as MAC addresses on Ethernet. Layer 3 handles logical IP addressing and routing between networks.

## Q4. What is the difference between TCP and UDP?

TCP provides a reliable, ordered byte stream with built-in retransmission and flow/congestion control. UDP sends independent datagrams without built-in delivery or ordering guarantees.

## Q5. What is a port number?

A port number identifies a transport-layer endpoint used to deliver traffic to the appropriate application or service. For example, TCP port `443` is commonly used for HTTPS.

## Q6. What is encapsulation?

Encapsulation is the process of adding protocol information as data moves down the networking stack. Transport information is added, then IP information, then link-layer framing, before transmission.

## Q7. What is decapsulation?

Decapsulation is the receiving-side process of interpreting and removing the relevant protocol headers as data moves up the networking stack towards the destination application.

## Q8. Why does a router change the MAC addresses but usually preserve the IP addresses?

A router forwards the IP packet across different links. Each outgoing link requires a suitable Layer 2 frame, so the frame's source and destination MAC addresses are set for that link. The IP addresses normally remain unchanged unless NAT or another mechanism modifies them.

## Q9. What is the difference between the OSI and TCP/IP models?

The OSI model has seven conceptual layers. The five-layer TCP/IP teaching model groups OSI's Application, Presentation, and Session functions into one Application Layer while retaining separate Transport, Network, Data Link, and Physical layers.

## Q10. Which layers are involved when a browser accesses an HTTPS website?

The application uses HTTP, TLS protects the communication, TCP typically provides transport for HTTP/1.1 or HTTP/2, IP handles addressing and routing, the link layer handles local frame delivery, and the physical medium carries the signals.

For HTTP/3, the transport uses QUIC over UDP instead of TCP.

## Q11. If `curl` returns HTTP `500`, does that prove the network is broken?

No. An HTTP `500` response indicates a server-side HTTP error response. It generally means that the request reached an HTTP server or intermediary that generated the error, although the underlying cause could involve an application or dependency failure.

## Q12. Why is the OSI model useful to a DevOps engineer?

It provides a structured way to reason about problems. Instead of randomly changing settings, an engineer can investigate application behavior, transport connections, routing, link connectivity, and the underlying medium systematically.

---

# 16. Quick Revision Cheat Sheet

| Concept | Remember |
|---|---|
| OSI | Seven-layer conceptual model |
| Application | Network services used by applications |
| Presentation | Data representation, encryption, compression concepts |
| Session | Communication-session management concepts |
| Transport | TCP, UDP, ports |
| Network | IP addresses and routing |
| Data Link | Frames and local link delivery |
| Physical | Bits carried by physical signals |
| TCP | Reliable, ordered byte stream |
| UDP | Datagram transport without built-in delivery guarantees |
| IP packet | Carries IP source and destination addresses |
| Frame | Carries link-layer addressing on Ethernet |
| Encapsulation | Adding protocol information as data moves down the stack |
| Decapsulation | Processing protocol information as data moves up the stack |
| Router | Forwards IP packets between networks |
| Switch | Forwards local network frames |
| ARP | Resolves local IPv4 next-hop addresses to link-layer addresses |
| TCP/IP model | Commonly taught using four or five layers |

### Memorize the data-unit sequence

```text
Application → Data
Transport   → Segment (TCP) / Datagram (UDP)
Network     → Packet
Data Link   → Frame
Physical    → Bits
```

### Memorize the encapsulation sequence

```text
Data
  ↓
TCP segment / UDP datagram
  ↓
IP packet
  ↓
Frame
  ↓
Bits
```

---

# 17. Practice Questions

Try these questions to reinforce the lesson.

### Question 1
Which OSI layer is responsible for routing IP packets between different networks?

### Question 2
What is the difference between an IP address and a MAC address?

### Question 3
A server has an application listening on TCP port `443`. Which OSI layer is associated with that port?

### Question 4
A frontend sends a packet to a backend on a different network. Which device commonly forwards the packet between networks?

### Question 5
Why does the destination MAC address normally change when a packet crosses a router?

### Question 6
Put these data units in the correct order, from application to physical transmission:

- Frame
- Data
- Bits
- IP packet
- TCP segment

### Question 7
A service is running, but a client cannot connect to it. Name three possible causes you would investigate.

### Question 8
What is the difference between encapsulation and decapsulation?

---

## Solutions

**1. Network Layer (Layer 3).** It handles IP addressing and routing.

**2.** An IP address provides logical addressing used for routing. A MAC address is used for local link-layer delivery on technologies such as Ethernet.

**3. Transport Layer (Layer 4).** TCP and UDP use port numbers to identify transport endpoints.

**4. A router.** It uses routing information to forward packets between networks.

**5.** Each routed link requires a new Layer 2 frame with addresses appropriate for that link. The IP packet normally continues towards the same IP destination.

**6.** Data → TCP segment → IP packet → Frame → Bits.

**7.** Possible causes include:
- The application is not listening on the expected port.
- A firewall or cloud security rule blocks the connection.
- The destination IP address or route is incorrect.

Other causes are possible, too.

**8.** Encapsulation adds protocol information as data moves down the sending stack. Decapsulation processes that information as data moves up the receiving stack.

---

# Lecture 11 Complete

You have now connected your previous lessons on IP addresses, subnet masks, gateways, MAC addresses, ARP, switches, and routers to the OSI model.

The most important idea to retain is that **network communication is a chain of responsibilities**. The application creates data, transport protocols deliver it to an endpoint, IP routes it across networks, the link layer delivers it over each local link, and the physical medium carries the signals.

For DevOps, this mental model becomes especially useful when troubleshooting applications, Linux servers, Docker containers, cloud networks, and Kubernetes services.

**Next in your course:** Lecture 12 — Switches vs. Routers and How They Forward Traffic. You previously summarized this topic, so we can continue with that lecture when you're ready.