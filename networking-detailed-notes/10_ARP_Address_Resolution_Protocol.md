# Lecture 10: ARP (Address Resolution Protocol) — How IP Addresses Are Mapped to MAC Addresses

**Course:** Networking for DevOps  
**Lecture:** 10  
**Topics:** ARP fundamentals, the problem ARP solves, ARP requests and replies, ARP caching, remote communication, and Linux ARP table inspection.

In Lecture 09, you learned that IP addresses and MAC addresses have different purposes. Now we'll explore how they work together.

The central question of this lesson is:

**If a computer knows the destination IP address, how does it discover the MAC address needed to send an Ethernet frame?**

The answer for IPv4 on a local Ethernet network is **ARP — Address Resolution Protocol**.

---

# 1. What Is ARP?

**ARP stands for Address Resolution Protocol.**

ARP allows a device to discover the link-layer address associated with an IPv4 address on the local network.

For example, suppose your laptop knows that another computer has this IP address:

```text
Destination IP: 192.168.1.20
```

But your laptop doesn't know the computer's MAC address.

It needs that MAC address to send an Ethernet frame directly to the computer.

ARP helps it discover the mapping:

```text
IPv4 address                  MAC address
192.168.1.20  ──────────────> BB:BB:BB:BB:BB:BB
```

The MAC address above is an illustrative example.

### What does ARP actually do?

ARP helps resolve an IPv4 address to a link-layer address on the local network.

It does not:
- Assign IP addresses to devices.
- Determine the route to a remote network.
- Resolve domain names into IP addresses.
- Discover the MAC address of a remote internet server across routers.

Those are different networking tasks.

## Why is ARP important?

Recall the two addressing systems from Lecture 09:

| Address | Main purpose |
|---|---|
| IP address | Identifies the IP-layer source and destination and supports routing |
| MAC address | Supports frame delivery over a local link |

ARP connects these two addressing systems when a device needs to send an IPv4 packet over an Ethernet-style local network.

---

# 2. The Problem ARP Solves

Imagine two computers connected to the same local network.

```text
Computer A                         Computer B
IP: 192.168.1.10                   IP: 192.168.1.20
MAC: AA:AA:AA:AA:AA:AA             MAC: BB:BB:BB:BB:BB:BB
       |                                  |
       +------------ Switch --------------+
```

Computer A wants to send data to Computer B.

It knows Computer B's IP address:

```text
192.168.1.20
```

However, it doesn't know Computer B's MAC address.

**How can Computer A create an Ethernet frame addressed to Computer B?**

It needs to discover the destination MAC address first.

That's the problem ARP solves.

### Analogy: Asking who owns an address

Imagine you're in a building and know someone's room number, but you don't know which person is in that room.

You ask everyone nearby:

"Who is in room 20?"

The person in room 20 responds with their identity.

ARP works similarly, except the request asks which network interface is associated with a particular IPv4 address.

The analogy is only illustrative: ARP messages are network packets, not spoken questions.

---

# 3. How ARP Works: Step-by-Step

Let's examine the complete process using our two computers.

### Network information

| Device | IPv4 address | MAC address |
|---|---|---|
| Computer A | `192.168.1.10` | `AA:AA:AA:AA:AA:AA` |
| Computer B | `192.168.1.20` | `BB:BB:BB:BB:BB:BB` |

Assume both computers are connected to the same IPv4 subnet and Computer A doesn't already have a usable ARP cache entry for Computer B.

## Step 1: Computer A checks the destination network

Computer A wants to communicate with:

```text
192.168.1.20
```

Its own configuration is:

```text
IP address:  192.168.1.10
Subnet mask: 255.255.255.0
```

Computer A determines that its own network is:

```text
192.168.1.0/24
```

It also determines that `192.168.1.20` belongs to that subnet.

Therefore, the destination is directly reachable on the local network.

**Important:** This subnet check determines whether the computer should resolve the destination's MAC address or use a router as the next hop.

## Step 2: Computer A checks its ARP cache

Before broadcasting anything, Computer A checks whether it already has a mapping for:

```text
192.168.1.20
```

If a valid entry exists, it can use the cached MAC address.

If no usable entry exists, Computer A needs to discover it.

## Step 3: Computer A broadcasts an ARP request

Computer A sends an ARP request asking which interface owns `192.168.1.20`.

Conceptually, the message says:

> Who has IP address 192.168.1.20? Tell 192.168.1.10.

Because Computer A doesn't know the target's MAC address, it sends the request in an Ethernet broadcast frame.

The Ethernet broadcast destination is:

```text
FF:FF:FF:FF:FF:FF
```

An Ethernet switch forwards this broadcast within the relevant Layer 2 broadcast domain, subject to its configuration.

### What happens to the broadcast?

```text
                   ARP REQUEST
             "Who has 192.168.1.20?"
                         |
                         v
                 Ethernet Switch
                 /      |      \
                /       |       \
           Device C  Computer B  Device D
```

The devices in the same broadcast domain receive the broadcast frame.

Devices that do not own the requested IP address ordinarily do not reply to the request.

## Step 4: Computer B recognizes its IP address

Computer B receives the ARP request and sees that it asks for:

```text
192.168.1.20
```

That is Computer B's own IPv4 address.

Computer B can therefore respond with its MAC address.

## Step 5: Computer B sends an ARP reply

Computer B sends an ARP reply to Computer A.

Conceptually:

> 192.168.1.20 is at BB:BB:BB:BB:BB:BB.

The reply is normally unicast to Computer A's MAC address.

```text
Computer A                         Computer B
    |                                   |
    | ARP request: broadcast            |
    |---------------------------------->|
    |                                   |
    | ARP reply: B's MAC address        |
    |<----------------------------------|
    |                                   |
```

Computer A now knows the MAC address associated with Computer B's IPv4 address.

## Step 6: Computer A stores the mapping

Computer A can store the discovered mapping in its local neighbor cache.

Conceptually:

```text
192.168.1.20 -> BB:BB:BB:BB:BB:BB
```

The operating system can use this mapping for subsequent communication while the entry remains valid.

## Step 7: Computer A sends the actual data

Now Computer A can create an Ethernet frame containing the IP packet.

```text
Ethernet frame
+----------------------------------+
| Source MAC: AA:AA:AA:AA:AA:AA    |
| Destination MAC: BB:BB:BB:BB:BB:BB|
+----------------------------------+
| IP packet                        |
| Source IP: 192.168.1.10          |
| Destination IP: 192.168.1.20     |
+----------------------------------+
| Actual application data          |
+----------------------------------+
```

Computer A sends the frame through the switch, which forwards it toward Computer B.

**The key point:** ARP discovers the MAC address; the actual application data is then carried in the normal network traffic.

---

# 4. Understanding the ARP Table and Cache

An ARP table stores mappings between IPv4 addresses and link-layer addresses that a device has learned or configured.

On modern Linux systems, this information is generally exposed through the **neighbor table**.

Example:

| IPv4 address | MAC address | Interface |
|---|---|---|
| `192.168.1.1` | `11:22:33:44:55:66` | `wlp2s0` |
| `192.168.1.20` | `BB:BB:BB:BB:BB:BB` | `wlp2s0` |
| `192.168.1.30` | `CC:CC:CC:CC:CC:CC` | `wlp2s0` |

These are example entries.

### Why cache the mappings?

Imagine a computer sends 1,000 packets to the same local device.

Without caching, it might need to repeat address resolution unnecessarily.

With caching, the computer can reuse the learned mapping while it remains valid.

Benefits include:

- Fewer ARP broadcasts.
- Less unnecessary network traffic.
- Faster subsequent communication.
- More efficient delivery of packets to local destinations.

### Do ARP entries last forever?

No.

Neighbor entries have states and can become stale or be removed. The operating system may need to refresh address resolution when an entry is no longer usable.

On Linux, you may see states such as:

| State | General meaning |
|---|---|
| `REACHABLE` | The neighbor is considered reachable based on recent confirmation. |
| `STALE` | The entry exists, but recent reachability has not been confirmed. |
| `DELAY` | The system is delaying further probing while waiting for confirmation. |
| `PROBE` | The system is actively probing to confirm reachability. |
| `FAILED` | Neighbor resolution or reachability confirmation failed. |

The exact state transitions depend on the operating system and networking circumstances.

---

# 5. What Happens When the Destination Is Outside the Local Network?

This is one of the most important parts of the lesson.

Suppose your laptop wants to communicate with a server at:

```text
203.0.113.50
```

Assume your laptop is configured as follows:

```text
Laptop IP:  192.168.1.10/24
Gateway IP: 192.168.1.1
```

The destination `203.0.113.50` is outside the laptop's local subnet.

The address `203.0.113.50` is used here only as a documentation example.

## Step 1: The laptop identifies a remote destination

The laptop compares the destination with its configured routes.

It determines that the destination is not directly reachable through its local subnet.

## Step 2: The laptop selects the default gateway

Assuming the default route applies, the next hop is:

```text
192.168.1.1
```

The laptop needs the gateway's MAC address to send the first Ethernet frame.

## Step 3: The laptop resolves the gateway's MAC address

If the gateway's MAC address is not already cached, the laptop sends an ARP request asking:

> Who has 192.168.1.1?

The router responds with the MAC address of its local interface.

## Step 4: The laptop sends the packet to the gateway

The first Ethernet frame contains:

```text
Source MAC:      Laptop's MAC
Destination MAC: Gateway's MAC

Source IP:       192.168.1.10
Destination IP:  203.0.113.50
```

Notice that the destination MAC address belongs to the gateway, but the destination IP belongs to the remote server.

## Step 5: The router forwards the packet

The router examines the destination IP and forwards the packet according to its routing table.

**The laptop does not normally ARP for the remote server's MAC address. It ARPs for the MAC address of its local next-hop gateway.**

### Complete flow

```text
Laptop
192.168.1.10
    |
    | ARP: Who has 192.168.1.1?
    v
Local Router
192.168.1.1
    |
    | Routes packet toward remote destination
    v
Other Networks
    |
    v
Remote Server
203.0.113.50
```

This is the connection between ARP and your previous lessons about subnet masks and default gateways.

---

# 6. Practical Linux Lab: Inspect Your ARP Table

Let's perform the practical work on your Zorin OS laptop.

## Step 1: View the ARP table using `arp -a`

Your lecture introduces:

```bash
arp -a
```

This command displays the local ARP table when the `arp` utility is installed.

Example output:

```text
? (192.168.1.1) at aa:bb:cc:dd:ee:ff [ether] on wlp2s0
? (192.168.1.20) at bb:bb:bb:bb:bb:bb [ether] on wlp2s0
```

Interpretation:

- `192.168.1.1` is an IPv4 address.
- `aa:bb:cc:dd:ee:ff` is its associated link-layer address.
- `wlp2s0` is the interface through which the neighbor is reachable.

Your actual output may be different.

### What if `arp -a` doesn't work?

On some Linux installations, the `arp` utility is not installed by default.

You can use the modern Linux command instead:

```bash
ip neigh show
```

This is generally the preferred way to inspect the Linux neighbor table.

## Step 2: Inspect a particular neighbor

Run:

```bash
ip neigh show
```

You may see something like:

```text
192.168.1.1 dev wlp2s0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
```

This indicates that Linux has a neighbor entry for `192.168.1.1`.

Here is what each part means:

| Output | Meaning |
|---|---|
| `192.168.1.1` | Neighbor's IPv4 address |
| `dev wlp2s0` | Interface used to reach the neighbor |
| `lladdr` | Link-layer address |
| `aa:bb:cc:dd:ee:ff` | Example MAC address |
| `REACHABLE` | Neighbor is considered reachable |

## Step 3: Check the route to your gateway

First, inspect the routing table:

```bash
ip route
```

Look for a default route such as:

```text
default via 192.168.1.1 dev wlp2s0
```

Your gateway may use a different address.

Now inspect the selected route to the gateway:

```bash
ip route get 192.168.1.1
```

Replace the example IP with the gateway address shown by your own `ip route` output.

## Step 4: Generate traffic and check the neighbor table again

You can try pinging your gateway:

```bash
ping -c 4 192.168.1.1
```

Replace the IP with your actual gateway address.

Then run:

```bash
ip neigh show
```

The gateway may now appear in the neighbor table.

**Note:** If the gateway already had a cached entry, the ping may not trigger a new ARP request. A successful ping also depends on the gateway allowing and responding to ICMP traffic.

---

# 7. How to Observe ARP Requests Directly

If you want to understand what ARP looks like on the network, you can use `tcpdump`.

Check whether it is installed:

```bash
tcpdump --version
```

If available, start a capture on your Wi-Fi interface:

```bash
sudo tcpdump -i wlp2s0 -nn arp
```

Replace `wlp2s0` with your actual interface name.

You might see output resembling:

```text
ARP, Request who-has 192.168.1.1 tell 192.168.1.10
ARP, Reply 192.168.1.1 is-at aa:bb:cc:dd:ee:ff
```

The addresses above are examples.

### What do these messages mean?

**Request:**

```text
Who has 192.168.1.1?
Tell 192.168.1.10.
```

The source is asking for the MAC address associated with the gateway's IPv4 address.

**Reply:**

```text
192.168.1.1 is at aa:bb:cc:dd:ee:ff
```

The reply supplies the mapping.

Stop the capture using **Ctrl+C**.

A capture may show no ARP traffic if the mapping is already cached and no new resolution occurs. On Wi-Fi, capture visibility also depends on the interface and capture mode.

---

# 8. Common Misunderstandings About ARP

### Mistake 1: ARP converts domain names into IP addresses

Incorrect.

DNS resolves domain names to IP addresses. ARP resolves IPv4 addresses to link-layer addresses on the local network.

### Mistake 2: ARP finds the MAC address of any device on the internet

Incorrect.

ARP requests are broadcast within the local Layer 2 broadcast domain. They do not ordinarily travel across routers.

For a remote destination, the sender resolves the MAC address of its next-hop gateway.

### Mistake 3: ARP assigns IP addresses

Incorrect.

DHCP is commonly used to assign IPv4 configuration automatically. ARP resolves IPv4 addresses to link-layer addresses.

### Mistake 4: Every outgoing packet requires a new ARP request

Incorrect.

The operating system can reuse valid neighbor-cache entries.

### Mistake 5: The destination IP changes to the gateway's IP

Incorrect.

The destination IP normally remains the remote destination's IP. The Ethernet frame is addressed to the gateway's MAC address for the first hop.

---

# 9. How ARP Relates to DevOps and Cloud Engineering

ARP is useful when diagnosing connectivity problems on Linux hosts and local virtual networks.

For example, when a server cannot communicate with another system, you may investigate:

1. Its assigned IP address and subnet.
2. Its routing table.
3. The selected next hop.
4. Its neighbor table.
5. Whether the neighbor can be resolved.
6. Whether a firewall or another network control blocks the traffic.

Useful Linux commands include:

```bash
ip -4 addr show
ip route
ip route get 8.8.8.8
ip neigh show
```

In virtualized environments, neighbor discovery may involve virtual Ethernet interfaces and virtual switches. In AWS, routing and security controls also matter; you should not assume that every cloud connectivity issue is an ARP problem.

**DevOps lesson:** When troubleshooting, first determine whether the problem is IP configuration, routing, local neighbor resolution, security filtering, or the application itself.

---

# 10. Interview Questions and Answers

### Q1. What is ARP?

ARP stands for Address Resolution Protocol. It discovers the link-layer address associated with an IPv4 address on a local network.

### Q2. Why is ARP necessary?

A host may know the destination IPv4 address but need the destination's MAC address to construct a local Ethernet frame.

### Q3. What is an ARP request?

An ARP request asks which device owns a specified IPv4 address. It is normally sent as an Ethernet broadcast on the local network.

### Q4. What is an ARP reply?

An ARP reply provides the requested link-layer address information. It is normally sent directly to the requester.

### Q5. What is an ARP cache?

It is a cache of IPv4-to-link-layer address mappings maintained by the operating system.

### Q6. What happens if the destination is outside the local subnet?

The sender selects a suitable route, usually through its default gateway for an ordinary internet destination, and resolves the gateway's MAC address if necessary.

### Q7. What is the difference between ARP and DNS?

DNS resolves domain names to IP addresses. ARP resolves IPv4 addresses to link-layer addresses on the local network.

### Q8. Which Linux commands can display ARP information?

```bash
arp -a
```

Or, on modern Linux systems:

```bash
ip neigh show
```

### Q9. Does ARP work across routers?

Ordinary ARP broadcasts do not cross routers. A host uses ARP to resolve a local next hop, not to discover the MAC address of a remote server across the internet.

### Q10. Does IPv6 use ARP?

No. IPv6 uses Neighbor Discovery Protocol (NDP) for address resolution and related neighbor functions.

---

# 11. Quick Revision Cheat Sheet

| Topic | Key point |
|---|---|
| ARP full form | Address Resolution Protocol |
| Purpose | Resolve an IPv4 address to a local link-layer address |
| ARP request | Normally broadcast |
| ARP reply | Normally unicast to the requester |
| ARP cache | Stores learned address mappings |
| Same-subnet destination | Resolve the destination's MAC if necessary |
| Remote destination | Resolve the next-hop gateway's MAC if necessary |
| DNS | Resolves domain names to IP addresses |
| DHCP | Commonly assigns IPv4 configuration |
| Linux ARP command | `arp -a` |
| Modern Linux neighbor command | `ip neigh show` |
| IPv6 equivalent | Neighbor Discovery Protocol |

### Remember this communication sequence

**Check the route → identify the next hop → resolve its MAC address if needed → construct the frame → send the packet.**

---

## Lecture 10 Completed

You've covered all five topics from your supplied lecture summary:

1. What ARP is.
2. Why IP-to-MAC resolution is needed.
3. ARP requests and replies.
4. ARP caching and remote communication.
5. Inspecting the local ARP table on Linux.

**Next: Lecture 11 — OSI Model vs. TCP/IP Model and the Journey of a Packet**, based on the lecture sequence you shared earlier.