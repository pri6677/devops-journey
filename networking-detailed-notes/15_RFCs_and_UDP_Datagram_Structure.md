# Networking for DevOps — Lecture 15
## RFCs and the Anatomy of a UDP Datagram

**Roadmap position:** Networking → Lecture 15  
**Previous lecture:** UDP — Connectionless Communication, Ports, and Real-World Uses  
**Focus:** Understanding protocol specifications, the structure of a UDP datagram, its four header fields, and how application data is carried.

---

# 1. Introduction to RFCs (Request for Comments)

## 1.1 What is an RFC?

**RFC stands for Request for Comments.**

RFCs are documents that describe technical standards, protocols, procedures, and other specifications used across the Internet.

They provide a common reference so that developers, operating systems, network devices, and services can implement protocols consistently.

For example, when Linux, Windows, a router, and a cloud server communicate using UDP, they need to follow compatible rules for formatting and processing UDP datagrams.

RFCs document those rules.

### Why are RFCs important?

Imagine that every operating system implemented UDP differently:

- One operating system placed the source port in a different position.
- Another interpreted the length field differently.
- A third calculated checksums using a different algorithm.

These implementations could fail to communicate correctly.

Protocol specifications help prevent this by defining how protocol fields are formatted and interpreted.

RFCs are important because they:

- Document protocol behavior.
- Define packet and header formats.
- Specify how protocol fields should be interpreted.
- Help developers implement interoperable networking software.
- Provide a technical reference for troubleshooting and security analysis.

### RFCs in real-world networking

RFCs describe many Internet technologies, including IP, TCP, UDP, DNS, and HTTP.

For example:

| Protocol | Specification |
|---|---|
| IPv4 | RFC 791 |
| UDP | RFC 768 |
| TCP | RFC 9293 |
| DNS concepts and facilities | RFC 1034 and RFC 1035 |

An RFC's number identifies a particular document. A protocol can have multiple related RFCs, and newer documents may update or obsolete earlier ones.

**Important:** Not every RFC is an Internet Standard. RFCs can also document informational material, experimental work, and other technical specifications.

## 1.2 UDP's specification

UDP is specified in **RFC 768**, titled *User Datagram Protocol*.

The original specification is very short compared with many other networking specifications. This reflects UDP's relatively simple transport-layer design.

However, a short specification does not mean UDP is unimportant or that implementing a complete networking stack is trivial. UDP relies on IP and operates within a much larger networking ecosystem.

You can read the original specification here:

$$
RFC 768 — User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768?utm_source=chatgpt.com)

When studying networking, learning to read RFCs is useful because they provide the formal technical rules behind the concepts you learn in lectures.

---

# 2. Anatomy of a UDP Datagram

A UDP datagram consists of two main parts:

1. **UDP header** — contains the information needed to process the datagram at the transport layer.
2. **Data payload** — contains the application data being transported.

The UDP header contains four fields, each **16 bits (2 bytes)** long.

Therefore:

$$
\text{UDP Header Size} = 4 \times 2 = 8\text{ bytes}
$$

The total UDP datagram size is:

$$
\boxed{\text{UDP Datagram Size}=\text{Header Size}+\text{Payload Size}}
$$

Since the header is always 8 bytes:

$$
\boxed{\text{UDP Datagram Size}=8+\text{Payload Size}}
$$

Here, the payload size is measured in bytes.

## 2.1 UDP datagram structure

```text
                 UDP DATAGRAM
+------------------------------------------------+
|                                                |
|                  UDP HEADER                    |
|                  8 bytes                       |
|                                                |
+----------------------+-------------------------+
| Source Port          | Destination Port        |
| 16 bits (2 bytes)    | 16 bits (2 bytes)       |
+----------------------+-------------------------+
| Length               | Checksum                |
| 16 bits (2 bytes)    | 16 bits (2 bytes)       |
+----------------------+-------------------------+
|                                                |
|                  DATA PAYLOAD                  |
|                                                |
|        DNS message, media data, etc.           |
|                                                |
+------------------------------------------------+
```

This structure is defined by UDP's protocol specification.

Let's understand each field individually.

---

# 3. Source Port — 16 Bits

The **Source Port** identifies the sender's UDP port.

It occupies:

- 16 bits
- 2 bytes

The source port helps the receiving application or operating system identify the transport endpoint associated with the sender.

For example, suppose your laptop sends a DNS query.

```text
Client
IP Address: 192.168.1.10
UDP Source Port: 53000
```

The source port in this example is `53000`.

This is an illustrative ephemeral port, not a fixed port that every client must use.

### Why is the source port useful?

Suppose a client sends a DNS query to a server and expects a response.

The source port helps the client identify the local UDP endpoint to which the response should be delivered.

A typical query might contain:

```text
Source Port:      53000
Destination Port: 53
```

The response normally reverses these port values:

```text
Source Port:      53
Destination Port: 53000
```

This example assumes the same endpoints and no relevant port translation.

### Important detail

A source port is not necessarily a unique identifier for an application process across the entire computer.

Port numbers are associated with transport endpoints and sockets. The operating system uses socket information, local and remote addresses, protocol, and other relevant details to determine how incoming traffic should be delivered.

The source port may also be zero when an application has no source port to specify.

---

# 4. Destination Port — 16 Bits

The **Destination Port** identifies the UDP port to which the datagram is being sent on the destination host.

It occupies:

- 16 bits
- 2 bytes

The destination port helps the receiving operating system deliver the datagram to the appropriate UDP socket.

## Example: Sending a DNS query

Suppose your laptop wants to resolve `example.com`.

The DNS resolver sends a query to a DNS server.

```text
Client                         DNS Server
192.168.1.10                   192.168.1.53
     |                              |
     |  UDP datagram                |
     |----------------------------->|
     |                              |
     | Destination port: 53         |
```

A typical UDP query might contain:

| UDP field | Value |
|---|---:|
| Source Port | 53000 |
| Destination Port | 53 |

Port `53` is the standard port used by DNS over UDP and DNS over TCP.

When the datagram reaches the destination host, the operating system uses its transport information to deliver the data to the appropriate socket.

**Remember:** The IP address identifies the network-layer destination, while the UDP destination port identifies the relevant transport endpoint on that destination.

## 4.1 How many UDP ports exist?

UDP uses a 16-bit port field.

Therefore, the numerical range is:

$$
2^{16}=65,536
$$

So UDP port numbers range from:

$$
\boxed{0\text{ to }65,535}
$$

Ports are commonly grouped into three ranges:

| Port range | Category | General use |
|---|---|---|
| 0–1023 | System or well-known ports | Common standard services |
| 1024–49151 | User or registered ports | Registered services and applications |
| 49152–65535 | Dynamic or private ports | Commonly used for temporary client ports |

The exact allocation and use of ports depend on the relevant standards and operating system. Client applications do not always select ports from the same range.

---

# 5. Length — 16 Bits

The **Length** field specifies the total size of the UDP datagram, including both the UDP header and its payload.

It occupies:

- 16 bits
- 2 bytes

The formula is:

$$
\boxed{\text{UDP Length}=8+\text{Payload Length}}
$$

Why add 8?

Because the UDP header itself is 8 bytes long.

## Example 1: A UDP datagram with 20 bytes of data

Suppose an application generates a payload of 20 bytes.

The UDP header contributes another 8 bytes.

Therefore:

$$
\text{UDP Length}=8+20
$$

$$
\boxed{\text{UDP Length}=28\text{ bytes}}
$$

The resulting structure is:

```text
+---------------------------+
| UDP Header: 8 bytes       |
+---------------------------+
| Payload: 20 bytes         |
+---------------------------+
| Total: 28 bytes           |
+---------------------------+
```

## Example 2: A UDP datagram with 100 bytes of data

Payload:

$$
100\text{ bytes}
$$

Header:

$$
8\text{ bytes}
$$

Total:

$$
8+100=108\text{ bytes}
$$

Therefore, the Length field contains `108`.

## Why is the Length field important?

The Length field tells the receiving system how much data belongs to the UDP datagram.

It is useful for interpreting the boundary between the UDP header and the payload.

Without an appropriate length, the receiving system could not correctly interpret the UDP datagram's size.

### Important distinction: UDP length vs. IP packet length

These are not the same measurement.

For an ordinary IPv4 packet without IP options:

```text
IPv4 packet
+----------------+--------------------------+
| IPv4 Header    | UDP Datagram             |
| 20 bytes       | Header + Payload         |
+----------------+--------------------------+
```

Suppose the UDP payload is 100 bytes.

The UDP datagram length is:

$$
8+100=108\text{ bytes}
$$

If the IPv4 header is 20 bytes, the IPv4 total length is:

$$
20+108=128\text{ bytes}
$$

Thus:

- UDP Length = 108 bytes.
- IPv4 Total Length = 128 bytes.

This example excludes link-layer headers and assumes there are no IPv4 options.

**DevOps connection:** Understanding these length fields helps when analyzing packet captures, troubleshooting packet-size issues, and investigating fragmentation or path MTU problems.

---

# 6. Checksum — 16 Bits

The **Checksum** field is used for error detection.

It occupies:

- 16 bits
- 2 bytes

The checksum helps the receiving system detect certain kinds of corruption in the UDP datagram and the associated IP addressing information.

For example, a datagram may be corrupted during transmission because of a hardware problem or other error.

A checksum provides a way to detect many such changes.

## 6.1 Is a checksum a cryptographic hash?

No.

Your lecture describes the checksum as a hash-like verification mechanism. The analogy can help introduce the idea, but technically, a UDP checksum is **not a cryptographic hash**.

UDP uses a one's-complement checksum calculation.

It is designed for error detection, not for proving who sent a packet or preventing deliberate modification.

A cryptographic integrity mechanism, such as a message authentication code, provides security properties that a UDP checksum does not.

### UDP checksum purposes

The checksum helps detect accidental corruption in:

- The UDP header.
- The UDP payload.
- The relevant IP pseudo-header information.

The pseudo-header includes information such as the source and destination IP addresses, the transport protocol identifier, and the UDP length. It is used in the checksum calculation but is not itself transmitted as part of the UDP header.

This also helps detect certain cases where a datagram has been delivered with incorrect IP addressing information.

## 6.2 What happens if the checksum fails?

If a receiver determines that a UDP checksum is invalid, it normally discards the datagram.

UDP itself does not automatically request retransmission.

The application may notice a missing response or message and decide whether to retry, depending on the protocol's design.

For example:

```text
Sender                         Receiver
  |                                |
  |------ UDP datagram ----------->|
  |                                |
  |                  Checksum fails|
  |                                |
  |                  Datagram drops|
  |                                |
  |       No UDP retransmission    |
  |             by itself          |
```

The sender might never know the datagram was dropped unless a higher-level protocol provides feedback.

### IPv4 and IPv6 checksum nuance

For UDP over IPv4, a checksum value of zero indicates that no UDP checksum was supplied, which IPv4 permits.

For UDP over IPv6, a checksum is generally required, subject to narrowly defined exceptions.

This is an important technical distinction when studying packet captures or protocol specifications.

---

# 7. Data Payload

The **payload** contains the actual data that the application wants to transmit.

Unlike the UDP header, the payload is not restricted to a particular application format by UDP itself.

UDP transports the bytes; the application or higher-level protocol defines how those bytes should be interpreted.

Examples include:

- DNS queries and responses.
- Real-time media data.
- Multiplayer game updates.
- QUIC packets.
- Other application-specific messages.

## Example: DNS payload

Suppose your laptop sends a DNS query for `example.com`.

The application creates a DNS message containing the information required for the query.

UDP places that message after its header.

```text
+----------------------+-------------------------+
| UDP Header           | Data Payload            |
|                      |                         |
| Source Port: 53000   | DNS query for           |
| Destination Port: 53 | example.com             |
| Length: 40           |                         |
| Checksum: ...        |                         |
+----------------------+-------------------------+
```

This is an illustrative example in which the DNS payload is 32 bytes and the total UDP datagram is 40 bytes. Actual DNS message sizes vary.

UDP does not need to understand the meaning of `example.com`. It carries the data, while the DNS application interprets the query.

## Payload size and practical limits

The UDP Length field is 16 bits, so it can represent values up to 65,535.

However, the maximum practical payload depends on the underlying IP version and packet-size constraints.

For example, under ordinary IPv4 datagram rules, the UDP datagram cannot exceed the IPv4 packet's total-length limit. With a standard 20-byte IPv4 header, the theoretical maximum UDP payload is:

$$
65,535-20-8=65,507\text{ bytes}
$$

This is a theoretical upper bound, not a recommendation to send datagrams that large.

In practice, network MTUs, fragmentation behavior, path MTU limitations, and application requirements often favor smaller datagrams.

Large UDP datagrams can be more vulnerable to loss because fragmentation may cause the entire original IP datagram to become unusable if a fragment is lost.

---

# 8. Putting All Four Header Fields Together

Let's combine the concepts into one example.

Suppose a client sends a UDP datagram containing a 32-byte DNS message.

Assume:

- Source port: `53000`
- Destination port: `53`
- Payload length: `32` bytes
- UDP header length: `8` bytes

The UDP Length field is:

$$
8+32=40\text{ bytes}
$$

The UDP header looks like this:

```text
+----------------------+-------------------------+
| Source Port          | Destination Port        |
| 53000                | 53                      |
| 16 bits              | 16 bits                 |
+----------------------+-------------------------+
| Length               | Checksum                |
| 40 bytes             | Calculated value        |
| 16 bits              | 16 bits                 |
+----------------------+-------------------------+
|                                                  |
|                  DNS PAYLOAD                     |
|                    32 bytes                      |
|                                                  |
+--------------------------------------------------+
```

The complete UDP datagram is 40 bytes.

The checksum field contains the calculated checksum value when a checksum is supplied.

The datagram is then encapsulated inside an IP packet and carried over the relevant link-layer network.

### Complete encapsulation flow

```text
Application data
      |
      v
+-----------------------+
| UDP Header            |
| Source Port           |
| Destination Port      |
| Length                |
| Checksum              |
+-----------------------+
| Application Payload   |
+-----------------------+
      |
      v
+-----------------------+
| IP Header             |
+-----------------------+
| UDP Datagram          |
+-----------------------+
      |
      v
+-----------------------+
| Link-layer Header     |
+-----------------------+
| IP Packet             |
+-----------------------+
| Link-layer Trailer    |
| (where applicable)    |
+-----------------------+
      |
      v
   Transmission
```

The precise link-layer format depends on the technology being used.

---

# 9. UDP Header: Final Revision Table

| Field | Size | Main purpose | Example |
|---|---:|---|---|
| Source Port | 16 bits / 2 bytes | Identifies the sender's UDP port | `53000` |
| Destination Port | 16 bits / 2 bytes | Identifies the receiving UDP port | `53` |
| Length | 16 bits / 2 bytes | Specifies the total UDP datagram size | `40` bytes |
| Checksum | 16 bits / 2 bytes | Detects certain types of corruption | Calculated checksum |
| **Total header** | **64 bits / 8 bytes** | **Transport-layer header** | — |
| Payload | Variable | Contains application data | DNS message |

Remember the relationship:

$$
\boxed{\text{UDP Datagram}=\text{8-byte Header}+\text{Payload}}
$$

And the header fields in order:

**Source Port → Destination Port → Length → Checksum**

---

## Lecture 15 Complete

You have now covered RFCs and the complete structure of a UDP datagram, including its four header fields and payload.

These concepts will help you read packet captures, understand network protocol specifications, and troubleshoot communication problems in Linux and cloud environments.
