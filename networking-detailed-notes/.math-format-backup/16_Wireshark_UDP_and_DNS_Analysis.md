# Lecture 16: Analyzing UDP Traffic with Wireshark and DNS

## 1. Introduction

In the previous lecture, we learned about the **structure of a UDP datagram**, including its four header fields:

- Source Port
- Destination Port
- Length
- Checksum

In this lecture, we'll examine a real UDP datagram using **Wireshark**. Instead of studying UDP only through theory, we'll inspect actual network packets and see how the different layers work together.

We'll use a DNS query for `github.com` sent to Google's Public DNS server, `8.8.8.8`, on port `53`.

### What you'll learn

- How to generate UDP traffic using `nslookup`.
- How to filter packets in Wireshark.
- How Ethernet, IP, UDP, and DNS information appear in a packet.
- How to calculate and verify UDP datagram length.
- How DNS uses transaction IDs to match queries with responses.

---

## 2. Understanding Wireshark

**Wireshark** is a network protocol analyzer that captures and displays packets sent and received by a computer.

It allows us to inspect network traffic at different layers, including:

| Layer | What we can inspect |
|---|---|
| Layer 2 — Data Link | Ethernet frame and MAC addresses |
| Layer 3 — Network | IP packet and IP addresses |
| Layer 4 — Transport | UDP header, ports, length, and checksum |
| Layer 7 — Application | DNS query and response information |

For example, when your laptop queries a DNS server, Wireshark can help you examine the packet's journey through these layers.

### Why is Wireshark useful for DevOps?

Network problems are common in cloud and infrastructure environments. Wireshark helps you investigate issues such as:

- Why a DNS query is failing.
- Whether a machine is sending network requests.
- Which IP addresses are communicating.
- Whether traffic uses TCP or UDP.
- Whether packets are being retransmitted at protocols that support retransmission.
- Whether a response is reaching your machine.

**Important:** Wireshark can show you what was captured at a particular network interface. It cannot, by itself, prove that every packet reached its final destination or identify the cause of every network failure.

---

## 3. Understanding the Test Environment

We'll generate a DNS query for `github.com` and direct it to Google's Public DNS server.

### Components involved

| Component | Value | Purpose |
|---|---|---|
| Your laptop | Your local IP address | Sends the DNS query |
| DNS server | `8.8.8.8` | Resolves the domain name |
| DNS port | `53` | Standard DNS port |
| Transport protocol | UDP, usually | Carries the DNS query |
| DNS query | `github.com` | Domain name being resolved |

### What is DNS?

**Domain Name System (DNS)** translates domain names into information such as IP addresses.

For example:

```text
github.com
    |
    | DNS query
    v
DNS server: 8.8.8.8
    |
    | DNS response
    v
IP address information
```

Your computer generally needs an IP address to establish a network connection to a destination identified by a domain name.

DNS commonly uses UDP port 53, although it can also use TCP and other transport mechanisms.

### What is `nslookup`?

`nslookup` is a command-line utility used to query DNS servers.

The command below requests DNS information for `github.com` from the specified server:

```bash
nslookup github.com 8.8.8.8
```

Here is what each part means:

- `nslookup` — starts the DNS lookup utility.
- `github.com` — specifies the domain name to look up.
- `8.8.8.8` — specifies the DNS server to query.

The command output typically includes the DNS server used and the answer returned.

**Note:** The command requests a DNS lookup; it does not guarantee that the traffic will use UDP in every circumstance. DNS can fall back to TCP or use other mechanisms. We will inspect the actual packets to confirm the protocol used.

---

## 4. Capturing DNS Traffic in Wireshark

### Step 1: Open Wireshark

Launch Wireshark on your Linux system.

Select the network interface through which your laptop communicates.

For example, your Wi-Fi interface may be named:

```text
wlp2s0
```

Your actual interface name may differ.

To list your network interfaces in the terminal, run:

```bash
ip link show
```

To identify the interface associated with your current route, run:

```bash
ip route
```

Look for a route beginning with `default`; its `dev` field identifies the interface used for that default route.

### Step 2: Start capturing packets

Select the appropriate interface and start the capture.

Wireshark may display many packets because your laptop is continuously communicating with other systems.

Examples include:

- DNS traffic
- TCP connections
- HTTPS traffic
- ARP packets
- Other local network communication

We need to narrow down the captured packets to the traffic relevant to our experiment.

### Step 3: Generate a DNS query

With the capture running, execute:

```bash
nslookup github.com 8.8.8.8
```

Your laptop will attempt to send a DNS query to `8.8.8.8`.

If the request and response are visible on the selected interface, Wireshark should capture them.

**Practical tip:** Start capturing first, run the command second, and stop the capture after the exchange. This makes the relevant packets easier to find.

---

## 5. Filtering Traffic in Wireshark

Wireshark captures many kinds of packets. A **display filter** lets us hide packets that do not match a particular condition.

For this lecture, use:

```wireshark
ip.dst == 8.8.8.8 || ip.src == 8.8.8.8
```

### Understanding the filter

| Expression | Meaning |
|---|---|
| `ip.dst == 8.8.8.8` | Show IPv4 packets whose destination IP is `8.8.8.8` |
| `ip.src == 8.8.8.8` | Show IPv4 packets whose source IP is `8.8.8.8` |
| `||` | Logical OR |

The complete expression means:

> Display IPv4 packets sent to `8.8.8.8` or received from `8.8.8.8`.

This helps you identify both the outgoing DNS request and the incoming response.

### Display filter versus capture filter

These are different:

- **Capture filter:** Determines which packets Wireshark records during capture.
- **Display filter:** Determines which already-captured packets are shown.

The expression above is a **display filter**. It does not prevent other packets from being captured.

### A more specific filter

To narrow the display to UDP traffic involving that server on port 53, you can use:

```wireshark
udp.port == 53 && ip.addr == 8.8.8.8
```

This displays UDP packets involving port 53 and the IP address `8.8.8.8`.

If DNS traffic is carried over TCP, this UDP filter will not show it.

---

## 6. Inspecting the Packet Layer by Layer

Select a DNS packet in Wireshark. In the packet details pane, expand the relevant protocol sections.

A typical DNS request sent over Ethernet and IPv4 using UDP has this structure:

```text
+-----------------------------------+
| Ethernet Frame                    |
|  Source MAC                       |
|  Destination MAC                  |
|                                   |
|  +-----------------------------+  |
|  | IPv4 Packet                 |  |
|  | Source IP                   |  |
|  | Destination IP: 8.8.8.8     |  |
|  |                             |  |
|  |  +-----------------------+  |  |
|  |  | UDP Datagram          |  |  |
|  |  | Source Port           |  |  |
|  |  | Destination Port: 53  |  |  |
|  |  | Length                |  |  |
|  |  | Checksum              |  |  |
|  |  |                       |  |  |
|  |  |  +-----------------+  |  |  |
|  |  |  | DNS Payload     |  |  |  |
|  |  |  | Query: github.com| |  |  |
|  |  |  +-----------------+  |  |  |
|  |  +-----------------------+  |  |
|  +-----------------------------+  |
+-----------------------------------+
```

This is an example of **encapsulation**: each lower layer carries the data from the layer above it.

Let's inspect each part.

### 6.1 Layer 2 — Ethernet frame

Expand the **Ethernet II** section.

You should see fields such as:

- Source MAC address
- Destination MAC address
- Ethernet type

#### Source MAC address

Identifies the interface that transmitted the Ethernet frame on the local link.

#### Destination MAC address

Identifies the next link-layer destination.

This is an important distinction: if `8.8.8.8` is outside your local subnet, the destination MAC address in the outgoing Ethernet frame will normally belong to your **default gateway**, not to Google's DNS server.

Why?

Ethernet delivers frames across the current local link. Routers forward IP packets between networks and construct new link-layer frames for the next link.

Therefore:

```text
Ethernet destination MAC = next-hop device
IP destination address   = 8.8.8.8
```

These values serve different purposes and do not need to identify the same device.

**Wi-Fi note:** On a Wi-Fi interface, the link-layer headers visible to Wireshark can depend on the capture mode and driver. The familiar Ethernet II view may not always appear exactly as it does on a wired Ethernet capture.

### 6.2 Layer 3 — IPv4 packet

Expand the **Internet Protocol Version 4** section.

Inspect:

| Field | What it tells you |
|---|---|
| Source IP | IP address sending the request |
| Destination IP | IP address receiving the request |
| TTL | Remaining IPv4 hop limit |
| Protocol | Identifies the next protocol, UDP in this case |
| Total Length | Total IPv4 packet size, including its IP header |

For an outgoing request, the destination IP should be:

```text
8.8.8.8
```

The source IP will normally be an address assigned to your machine or an address selected for the connection. It may be a private IPv4 address.

For example:

```text
Source IP:      192.168.1.10
Destination IP: 8.8.8.8
```

These are illustrative values; your actual source IP may differ.

**Important:** A private source IP can be translated by NAT as traffic passes through your router. The address visible in a laptop capture may therefore differ from the public source address seen by the external DNS server.

### 6.3 Layer 4 — UDP datagram

Expand the **User Datagram Protocol** section.

You should see four fields:

| Field | Size | Purpose |
|---|---:|---|
| Source Port | 16 bits | Identifies the sending endpoint's UDP port |
| Destination Port | 16 bits | Identifies the receiving service's UDP port |
| Length | 16 bits | Total UDP header and payload length |
| Checksum | 16 bits | Detects certain transmission errors |

#### Source port

Your operating system typically selects an available ephemeral port for the DNS query.

For example:

```text
Source Port:  49152
```

This is only an example. Your actual port may be different.

The source port allows the operating system to associate the response with the appropriate local socket and application.

#### Destination port

For a conventional DNS query over UDP, the destination port is:

```text
53
```

The DNS server listens for DNS requests on port 53.

#### Checksum

The UDP checksum is an error-detection mechanism. It is **not a cryptographic hash and does not provide protection against deliberate tampering**.

Wireshark may display checksum information or a checksum-validation status. The status can depend on capture conditions and checksum offloading, so an apparently incorrect checksum in a local outgoing capture does not automatically mean the packet was transmitted incorrectly.

#### Length

The UDP Length field counts:

```text
UDP header + UDP payload
```

It does **not** include the Ethernet header or IPv4 header.

We will calculate this value in Section 7.

### 6.4 Layer 7 — DNS payload

Expand the **Domain Name System** section.

For a DNS query, you can inspect:

- Transaction ID
- Flags
- Questions
- Queried domain name
- Query type
- Query class

For example, a query may contain:

```text
Name:   github.com
Type:   A
Class:  IN
```

Here:

- `github.com` is the domain being queried.
- `A` requests an IPv4 address record.
- `IN` means the Internet class.

Other DNS record types include:

| Record type | Purpose |
|---|---|
| `A` | IPv4 address |
| `AAAA` | IPv6 address |
| `CNAME` | Canonical name or alias |
| `MX` | Mail exchange |
| `NS` | Authoritative name server |
| `TXT` | Text information associated with a domain |

The actual response can contain multiple records, and the records returned depend on the query and DNS configuration.

---

## 7. Calculating UDP Length Manually

One of the main practical goals of this lecture is to verify the UDP Length field.

The UDP header contains four fields, each 16 bits long.

Therefore:

\[
4 \times 16 = 64 \text{ bits}
\]

Since 8 bits equal one byte:

\[
64 \div 8 = 8 \text{ bytes}
\]

**The UDP header is always 8 bytes long.**

The UDP Length field includes the header and the payload.

\[
\boxed{\text{UDP Length} = \text{UDP Header Length} + \text{UDP Payload Length}}
\]

### Example from the lecture

Suppose Wireshark shows:

```text
UDP header:  8 bytes
DNS payload: 28 bytes
```

The calculation is:

\[
8 + 28 = 36 \text{ bytes}
\]

Therefore:

```text
UDP Length = 36 bytes
```

The UDP Length field should report `36` for that particular datagram.

### What does the 28-byte DNS payload represent?

It represents the size of the DNS message carried inside UDP for this example. It is not a fixed size for every DNS query.

DNS messages vary depending on factors such as:

- The domain name.
- The query type.
- Additional DNS fields or records.
- EDNS options.
- The size and content of the response.

So, **do not memorize 36 bytes as the standard size of a DNS datagram**. It is the result for the example described in this lecture.

### Comparing UDP length with IP total length

This is another important distinction.

Assume the packet contains:

- IPv4 header: 20 bytes, without IP options.
- UDP datagram: 36 bytes.

Then:

\[
\text{IPv4 Total Length} = 20 + 36
\]

\[
\boxed{\text{IPv4 Total Length} = 56 \text{ bytes}}
\]

The values differ because the IPv4 Total Length field includes the IPv4 header, while the UDP Length field does not.

| Field | Example value | Includes |
|---|---:|---|
| UDP header length | 8 bytes | UDP header only |
| UDP Length | 36 bytes | UDP header + DNS payload |
| IPv4 header length | 20 bytes | IPv4 header only |
| IPv4 Total Length | 56 bytes | IPv4 header + UDP datagram |

These values apply to the example, assuming a standard 20-byte IPv4 header and no additional IP options.

---

## 8. DNS Transaction IDs: Matching Queries and Responses

UDP does not provide TCP-style connection establishment, guaranteed delivery, or built-in retransmission.

So how can an application determine which DNS response belongs to which query?

DNS uses a **Transaction ID** in its message header.

### How it works

Suppose your laptop sends a DNS query:

```text
Client → DNS Server

Transaction ID: 0x4A2B
Question: github.com
```

The DNS server processes the query and sends a response:

```text
DNS Server → Client

Transaction ID: 0x4A2B
Answer: DNS records for github.com
```

The matching transaction IDs help the client associate the response with the corresponding outstanding query.

The ID is a 16-bit field, so it can represent values from `0` to `65535`.

### Visual flow

```text
Your laptop                         DNS server
    |                                    |
    | DNS query                          |
    | Transaction ID: 0x4A2B             |
    |----------------------------------->|
    |                                    |
    | DNS response                       |
    | Transaction ID: 0x4A2B             |
    |<-----------------------------------|
    |                                    |
    | Match response to query            |
```

In Wireshark, expand the DNS section of both the outgoing query and incoming response. Compare their Transaction ID fields.

For a conventional query-response exchange, the IDs should match.

### Does the transaction ID make UDP reliable?

**No.** It helps DNS correlate messages, but it does not guarantee that a request or response will arrive.

Packets can still be:

- Lost.
- Delayed.
- Duplicated.
- Delivered out of order.

DNS implementations can use timeouts and retry queries when needed. A response must also be validated appropriately; matching a transaction ID alone is not sufficient security against forged responses.

The transaction ID is one part of DNS message correlation, not a replacement for transport reliability.

---

## 9. Putting Everything Together

When you run:

```bash
nslookup github.com 8.8.8.8
```

a typical DNS query over UDP follows this sequence:

1. The DNS client constructs a query for `github.com`.
2. The operating system determines how to route the packet to `8.8.8.8`.
3. If the destination is remote, the operating system normally resolves the next-hop gateway's MAC address if necessary.
4. The DNS message is placed inside a UDP datagram.
5. The UDP datagram is placed inside an IP packet.
6. The IP packet is carried in a link-layer frame.
7. The packet travels toward the DNS server.
8. The DNS server processes the query and sends a response.
9. The response returns to the client.
10. The DNS client correlates the response with its query, including using the DNS Transaction ID.

The encapsulation looks like this:

```text
DNS Message
    ↓
UDP Datagram
    ↓
IP Packet
    ↓
Link-Layer Frame
    ↓
Physical or wireless transmission
```

At the receiving end, the layers process the information in the reverse order.

---

## 10. Practical Lab on Zorin OS

You can perform this experiment on your Linux laptop.

### Step 1: Check the network interfaces

```bash
ip link show
```

Identify the interface you are using.

### Step 2: Check your IP address and routing

```bash
ip -4 addr show
ip route
```

These commands help you identify your IPv4 address and default route.

### Step 3: Open Wireshark

Start a capture on the active interface.

### Step 4: Generate the DNS query

Run:

```bash
nslookup github.com 8.8.8.8
```

### Step 5: Apply the display filter

```wireshark
ip.dst == 8.8.8.8 || ip.src == 8.8.8.8
```

For a more specific UDP DNS filter:

```wireshark
udp.port == 53 && ip.addr == 8.8.8.8
```

### Step 6: Inspect the outgoing request

Expand these sections in the packet details pane:

1. Ethernet II
2. Internet Protocol Version 4
3. User Datagram Protocol
4. Domain Name System

Record the actual values Wireshark shows.

### Step 7: Inspect the response

Select the response packet and compare:

- Source and destination IP addresses.
- Source and destination UDP ports.
- UDP Length.
- DNS Transaction ID.
- DNS answer records.

The response normally reverses the IP and UDP endpoint directions relative to the query, although the exact source port and packet details should be confirmed from the capture.

### Step 8: Verify the length

Use the UDP Length field shown by Wireshark.

Calculate:

```text
UDP Length = 8 + UDP payload length
```

Compare your result with the displayed value.

**Important:** Your captured packet may not have the example's 28-byte DNS payload or 36-byte UDP Length. Use your actual packet values when checking the calculation.

---

## 11. Common Mistakes to Avoid

| Mistake | Correct understanding |
|---|---|
| Assuming every DNS query uses UDP | DNS can also use TCP and other transport mechanisms. |
| Assuming the destination MAC is `8.8.8.8` | A MAC address is used on the local link; remote traffic normally goes to the gateway's MAC first. |
| Confusing UDP Length with IP Total Length | UDP Length includes the UDP header and payload; IP Total Length includes the IP header as well. |
| Assuming every DNS query has a 28-byte payload | DNS message size varies. |
| Treating the DNS Transaction ID as a reliability mechanism | It helps correlate messages but does not guarantee delivery. |
| Assuming a checksum provides encryption | The UDP checksum detects certain errors; it does not provide confidentiality or cryptographic authentication. |
| Thinking a Wireshark display filter limits capture | Display filters control visibility, not which packets were captured. |

---

## 12. Quick Revision Sheet

### Wireshark

- **Purpose:** Capture and inspect network packets.
- **Display filter:** `ip.dst == 8.8.8.8 || ip.src == 8.8.8.8`
- **DNS query command:** `nslookup github.com 8.8.8.8`

### UDP

- Transport layer: Layer 4.
- Header size: **8 bytes**.
- Source port: Identifies the sending endpoint's UDP port.
- Destination port: Identifies the receiving service's UDP port.
- Length: UDP header + UDP payload.
- Checksum: Error detection, not cryptographic security.

### DNS

- Common UDP port: `53`.
- Transaction ID: Helps match a response with its query.
- `A`: IPv4 address record.
- `AAAA`: IPv6 address record.

### Length formulas

\[
\boxed{\text{UDP Length} = 8 + \text{UDP Payload Length}}
\]

For the lecture's example:

\[
8 + 28 = 36 \text{ bytes}
\]

With a 20-byte IPv4 header:

\[
20 + 36 = 56 \text{ bytes for the IPv4 packet}}
\]

### The key concept

**Wireshark lets you observe how application data is encapsulated in UDP, IP, and link-layer frames. DNS Transaction IDs help correlate UDP requests and responses, while UDP itself does not guarantee delivery.**

These concepts are useful when troubleshooting DNS failures, examining cloud network traffic, and understanding how applications communicate across networks.