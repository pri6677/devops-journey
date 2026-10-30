# Lecture 02: What Happens When You Send an HTTP Request?

This lecture explains the complete, high-level journey of an HTTP request—from a frontend application running on your computer to a backend server hosted in the cloud.

We'll use this example throughout the lecture:

- **Frontend:** React application running locally on port `3000`.
- **Backend:** Node.js application hosted on AWS EC2.
- **Domain:** `api.example.com`.
- **Destination port:** `443`.

We'll study how DNS, TCP, ports, IP addresses, MAC addresses, ARP, and physical transmission work together to deliver a request.

## 1. The Complete HTTP Request Lifecycle

When a frontend application sends an HTTP request to a backend server, several networking operations take place.

The request follows this general sequence:

1. DNS resolution
2. Preparing the HTTP request
3. Operating system networking and TCP handshake
4. TCP segments, ports, and sequence numbers
5. IP packet encapsulation
6. Ethernet frames, MAC addresses, and ARP
7. Physical transmission

Each step prepares the request for the next stage of communication.

## 2. Step-by-Step Request Journey

### Step 1: DNS Resolution

The frontend application wants to communicate with:

```text
api.example.com
```

Computers use IP addresses to identify network destinations, so the application needs to determine the IP address associated with this domain.

DNS performs this name-resolution function.

```text
Frontend application
        |
        | api.example.com
        v
   DNS resolution
        |
        v
 Destination IP address
```

The application can then use the resolved address when connecting to the backend.

**Key concept:** DNS translates domain names into DNS records, which can include IP addresses. It does not itself transport the HTTP request to the backend.

### Step 2: Preparing the HTTP Request

After resolving the domain, the application prepares its HTTP request.

Conceptually, a request might look like this:

```http
GET /users HTTP/1.1
Host: api.example.com
```

The request contains information such as:
- The HTTP method, such as `GET` or `POST`.
- The requested resource path.
- HTTP headers.
- An optional body, depending on the request.

The application represents this information as bytes so that it can be transmitted over the network.

For example:

```text
HTTP request
     |
     v
Encoded bytes
     |
     v
Ready for transport
```

**Key concept:** HTTP defines the application-level request. Lower networking layers are responsible for transporting it between the communicating endpoints.

### Step 3: The Operating System and TCP Three-Way Handshake

The application passes the request data to the operating system's networking stack through its networking APIs.

When the connection uses TCP, the client generally establishes a TCP connection before sending application data.

TCP uses a three-way handshake:

```text
Client                              Server
  |                                    |
  |----------- SYN ------------------->|
  |                                    |
  |<---------- SYN-ACK ----------------|
  |                                    |
  |----------- ACK ------------------->|
  |                                    |
  |        TCP connection established  |
```

The three messages are:

| Message | Meaning |
|---|---|
| SYN | The client requests to establish a TCP connection. |
| SYN-ACK | The server acknowledges the client's SYN and sends its own SYN. |
| ACK | The client acknowledges the server's SYN. |

Once the handshake succeeds, the endpoints can exchange application data over the TCP connection.

**Important:** This describes TCP-based communication. HTTP/3 uses QUIC over UDP rather than TCP.

### Step 4: TCP Segments, Ports, and Sequence Numbers

TCP provides a reliable, ordered byte stream.

It places transport-layer information around the application data, including source and destination ports, sequence numbers, and other control fields.

For example:

```text
Source IP:       Client's IP
Destination IP:  Backend server's IP

Source port:     Client's selected port
Destination port: 443
```

The frontend application's local port `3000` is not necessarily the TCP source port of an outgoing request.

Port `3000` commonly identifies the local development server that serves the React application. When the browser or frontend runtime makes an API request, the operating system typically selects a separate ephemeral source port for the outgoing connection.

An example connection might look like:

```text
Client IP:       192.168.1.10
Client port:     51824

Server IP:       Example destination IP
Server port:     443
```

These addresses and ports are illustrative.

#### Why does TCP use sequence numbers?

TCP represents data as a byte stream. Sequence numbers help the receiving endpoint identify where data belongs in that stream.

If data is transmitted across multiple TCP segments, sequence numbers allow TCP to:
- Track which bytes have been received.
- Detect missing data.
- Reassemble data in the correct order.
- Support retransmission when required.

TCP divides the byte stream into segments according to factors such as the connection's MSS and available transmission constraints.

**Key concept:** TCP sequence numbers help manage an ordered byte stream; TCP does not promise that each application write corresponds to exactly one TCP segment.

### Step 5: IP Packet Encapsulation

The TCP segment is encapsulated inside an IP packet.

The IP header includes source and destination IP addresses, which routers use when forwarding packets toward their destinations.

Conceptually:

```text
+----------------------------------+
| IP Header                        |
| Source IP                        |
| Destination IP                   |
+----------------------------------+
| TCP Header                       |
| Source Port                      |
| Destination Port                 |
| Sequence and Acknowledgment Data |
+----------------------------------+
| Application Data                 |
+----------------------------------+
```

As the packet crosses routers, the routers examine the destination IP address and their routing information to decide where to forward it.

The source and destination IP addresses normally remain the same end-to-end, except when mechanisms such as NAT modify them.

**Key concept:** IP addressing enables communication across multiple networks, while routing determines how packets travel between them.

### Step 6: Ethernet Frames, MAC Addresses, and ARP

Before the IP packet can be transmitted over an Ethernet network, it is carried inside an Ethernet frame.

The frame includes source and destination MAC addresses.

For a remote destination, the laptop normally does not send the Ethernet frame directly to the remote server's MAC address. Instead, it sends the frame to the MAC address of the next-hop router, usually the default gateway.

If the gateway's MAC address is not already known, the laptop can use ARP to resolve it.

```text
Laptop
  |
  | IP destination: Remote server
  |
  | Ethernet destination: Gateway MAC
  v
Default gateway
  |
  v
Next network
```

ARP is used to discover the link-layer address associated with an IPv4 address on the local network.

At each routed hop, a router removes the incoming link-layer frame and creates a new frame for the next link.

This means:
- The IP packet normally continues toward the same destination.
- The MAC addresses used for local delivery change as the packet crosses routed links.

**Key concept:** IP addresses support routing between networks; MAC addresses support delivery over the current link.

### Step 7: Physical Transmission

At the physical transmission stage, the frame is represented as signals that travel through the network medium.

Depending on the technology, these may involve:

- Electrical signals over copper cables.
- Optical signals over fiber.
- Radio signals over Wi-Fi.

At a simplified level, the process looks like this:

```text
Application data
       |
       v
TCP segment
       |
       v
IP packet
       |
       v
Link-layer frame
       |
       v
Bits and physical signals
       |
       v
Network transmission
```

The receiving network interface processes the incoming signals, reconstructs the frame, and passes the data up through the networking stack.

The destination system then processes the IP packet, TCP data, and HTTP request.

---

## 3. Complete Journey at a Glance

```text
React Frontend
      |
      | 1. Resolve api.example.com
      v
DNS Resolution
      |
      | 2. Prepare HTTP request
      v
Operating System
      |
      | 3. Establish TCP connection
      v
TCP Segment
      |
      | 4. Add ports and sequence information
      v
IP Packet
      |
      | 5. Add source and destination IP addresses
      v
Ethernet Frame
      |
      | 6. Add local-link MAC addresses
      v
Physical Transmission
      |
      v
Routers Forward the Packet
      |
      v
Backend Server
      |
      v
TCP and HTTP Processing
```

This diagram presents the main concepts in sequence. In real networking, routing, address resolution, connection establishment, and transmission interact according to the operating system and network configuration.

## 4. Concepts Introduced in This Lecture

| Concept | Purpose |
|---|---|
| DNS | Resolves domain names into DNS records, including IP addresses. |
| HTTP | Defines application-level requests and responses. |
| Ports | Identify transport-layer endpoints and services. |
| TCP handshake | Establishes a TCP connection. |
| Sequence numbers | Help TCP deliver an ordered byte stream. |
| IP packets | Carry data between IP endpoints across networks. |
| MAC addresses | Identify link-layer endpoints for local delivery. |
| ARP | Resolves local IPv4-to-MAC mappings. |
| Default gateway | Provides a next hop for traffic destined outside the local network. |
| Physical transmission | Carries encoded information across a network medium. |

### Final takeaway

An HTTP request is not simply sent directly from one application to another. It passes through several layers, each adding information needed for communication.

This introduces the overall journey. The nxt we'll examine these components individually and explain how they work internally.