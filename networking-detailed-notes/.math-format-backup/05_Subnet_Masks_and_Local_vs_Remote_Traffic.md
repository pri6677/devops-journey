# Networking for DevOps — Lecture 05
## Subnet Masks and Local vs. External Traffic

**Roadmap position:** Networking — Lecture 05  
**Previous lecture:** Network vs. Host, CIDR Notation, and IPv4 Address Capacity  
**Today's goal:** Understand how your computer uses a subnet mask to determine whether a destination is on the local network or must be reached through a router.

This is a fundamental networking concept. Once you understand it, you'll be better prepared to understand routing, default gateways, AWS VPCs, and network troubleshooting.

---

# 1. What Is a Subnet Mask?

A **subnet mask** is a 32-bit value used with an IPv4 address to identify which bits belong to the network prefix and which bits belong to the host portion.

For example:

```text
IP address:  192.168.1.10
Subnet mask: 255.255.255.0
```

The subnet mask tells the computer that the first 24 bits represent the network prefix.

In CIDR notation, this is written as:

```text
192.168.1.10/24
```

Here, `/24` means 24 network bits and 8 host bits.

### Why do we need a subnet mask?

Imagine your laptop is connected to a network containing several devices.

Your laptop needs to determine whether the destination is:

- On its own local subnet, or
- On another network that requires routing.

The subnet mask helps your laptop make this decision.

Without the appropriate network prefix information, the computer cannot correctly determine the subnet from the IP address alone.

---

# 2. Understanding the Subnet Mask in Binary

Let's examine this configuration:

```text
IP address:  192.168.1.10
Subnet mask: 255.255.255.0
```

The subnet mask in binary is:

```text
11111111.11111111.11111111.00000000
```

Notice the pattern:

- The first 24 bits are `1`.
- The final 8 bits are `0`.

The `1` bits identify the network prefix. The `0` bits identify the host portion.

Visual representation:

```text
IP address:
192.168.1.10

Network portion          Host portion
       24 bits               8 bits
+------------------------+----------+
| 192.168.1              |    10    |
+------------------------+----------+

Subnet mask:
255.255.255.0

Binary:
11111111.11111111.11111111.00000000
```

This is the conventional subnet mask for a `/24` IPv4 subnet.

## Common subnet masks

| CIDR prefix | Subnet mask | Network bits | Host bits |
|---|---|---:|---:|
| `/8` | `255.0.0.0` | 8 | 24 |
| `/16` | `255.255.0.0` | 16 | 16 |
| `/24` | `255.255.255.0` | 24 | 8 |
| `/25` | `255.255.255.128` | 25 | 7 |
| `/26` | `255.255.255.192` | 26 | 6 |
| `/27` | `255.255.255.224` | 27 | 5 |
| `/28` | `255.255.255.240` | 28 | 4 |

**Remember:** A subnet mask and a CIDR prefix express the same network-prefix information in different forms.

For example:

```text
255.255.255.0 = /24
```

---

# 3. What Is the Bitwise AND Operation?

To understand how a computer identifies the network portion of an IP address, you need to understand a simple logical operation called **bitwise AND**.

AND compares two bits and produces a result.

| First bit | Second bit | Result |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

The rule is straightforward:

**The result is `1` only when both input bits are `1`. Otherwise, the result is `0`.**

Why is this useful for networking?

When a computer performs a bitwise AND between an IPv4 address and its subnet mask, the result identifies the network address.

Let's work through an example.

---

# 4. Calculating the Network Address

Suppose your laptop has this configuration:

```text
IP address:  192.168.1.10
Subnet mask: 255.255.255.0
```

We want to determine the network address.

### Step 1: Convert the IP address to binary

```text
192.168.1.10

11000000.10101000.00000001.00001010
```

### Step 2: Convert the subnet mask to binary

```text
255.255.255.0

11111111.11111111.11111111.00000000
```

### Step 3: Perform bitwise AND

```text
IP address:
11000000.10101000.00000001.00001010

Subnet mask:
11111111.11111111.11111111.00000000
------------------------------------------------
Result:
11000000.10101000.00000001.00000000
```

### Step 4: Convert the result back to decimal

```text
11000000 = 192
10101000 = 168
00000001 = 1
00000000 = 0
```

Therefore:

\[
\boxed{\text{Network address} = 192.168.1.0}
\]

This means that `192.168.1.10/24` belongs to the subnet `192.168.1.0/24`.

### The formula

\[
\boxed{\text{Network address}=\text{IP address AND subnet mask}}
\]

This is one of the most important formulas in IPv4 subnetting.

---

# 5. How Does a Computer Decide Whether Traffic Is Local?

Now let's connect subnet masks to real network communication.

Suppose your laptop has this configuration:

```text
Your laptop IP: 192.168.1.10
Subnet mask:    255.255.255.0
```

Your laptop wants to communicate with two destinations:

**Destination A:**

```text
192.168.1.20
```

**Destination B:**

```text
192.168.2.20
```

Are both destinations on the same subnet?

Let's find out.

## Case A: Destination is `192.168.1.20`

Your laptop's network address:

```text
192.168.1.10 AND 255.255.255.0
= 192.168.1.0
```

Destination's network address:

```text
192.168.1.20 AND 255.255.255.0
= 192.168.1.0
```

The results match.

```text
Your network:       192.168.1.0
Destination network: 192.168.1.0

Result: Same subnet
```

The laptop can send the traffic directly on the local network, assuming the destination is reachable and local network rules permit communication.

It does not need to send the packet to the default gateway for this destination.

## Case B: Destination is `192.168.2.20`

Your laptop's network address:

```text
192.168.1.10 AND 255.255.255.0
= 192.168.1.0
```

Destination's network address:

```text
192.168.2.20 AND 255.255.255.0
= 192.168.2.0
```

The results do not match.

```text
Your network:        192.168.1.0
Destination network: 192.168.2.0

Result: Different subnets
```

The laptop needs to use an appropriate route to reach the destination. If the routing table contains a default route, the default gateway is generally used when no more-specific route matches.

### Summary

| Destination | Your network | Destination network | Typical action |
|---|---|---|---|
| `192.168.1.20` | `192.168.1.0` | `192.168.1.0` | Send directly on the local network |
| `192.168.2.20` | `192.168.1.0` | `192.168.2.0` | Use a route toward the other network |

This is the core concept of Lecture 05.

---

# 6. What Happens When Traffic Is Local?

Imagine your laptop wants to communicate with a printer on the same subnet.

```text
Laptop                            Printer
192.168.1.10                      192.168.1.20
     |                                  |
     +----------------------------------+
              Local network
```

Your laptop compares the destination address with its own subnet.

Because both addresses belong to `192.168.1.0/24`, it determines that the destination is local.

For communication over a typical Ethernet or Wi-Fi LAN, the laptop needs the destination's link-layer address, usually its MAC address.

If that mapping is not already cached, the laptop can use ARP to discover the MAC address for the destination IPv4 address.

It can then send a frame addressed to that destination.

The local traffic does not need to pass through the router as an IP-routing hop.

**Important:** The subnet mask determines whether the destination is considered on-link; ARP helps resolve the local IPv4 destination to a MAC address on an IPv4 Ethernet network.

---

# 7. What Happens When Traffic Is External?

Suppose your laptop wants to contact a server on a different subnet.

```text
Laptop
192.168.1.10
     |
     | Local network
     |
Router / Default Gateway
192.168.1.1
     |
     | Other networks
     |
Remote server
```

Your laptop determines that the destination does not belong to its local subnet.

It consults its routing table to find an appropriate route.

If the matching route specifies a gateway, the laptop sends the traffic toward that next hop.

On a typical IPv4 Ethernet LAN, this means:

1. The destination IP address remains the remote server's IP address.
2. The Ethernet frame is addressed to the gateway's MAC address.
3. The router receives the frame.
4. The router examines the destination IP and its routing table.
5. The router forwards the packet toward the next network if a valid route exists.

This is an important distinction:

**For remote traffic, the destination IP is the remote server's IP, but the immediate link-layer destination is usually the gateway's MAC address.**

We'll study the default gateway and routing process in more detail in Lecture 06.

---

# 8. Practical Linux Lab

Let's inspect how these concepts appear on your Zorin OS system.

## Step 1: Display network interfaces

Run:

```bash
ip addr
```

Look for your Wi-Fi interface, previously identified as `wlp2s0`.

You might see something similar to:

```text
inet 192.168.1.10/24
```

Your actual address and prefix may differ.

Interpretation:

- `192.168.1.10` — the IPv4 address.
- `/24` — the network prefix.
- The corresponding subnet mask is `255.255.255.0`.

## Step 2: Display your routing table

Run:

```bash
ip route
```

Example:

```text
default via 192.168.1.1 dev wlp2s0
192.168.1.0/24 dev wlp2s0 proto kernel scope link
```

The first entry describes the default route through the gateway.

The second entry describes the directly connected subnet.

Your output may look different depending on your network configuration.

## Step 3: Inspect the route to a local destination

If your local address is `192.168.1.10/24`, try:

```bash
ip route get 192.168.1.20
```

This asks Linux to show the route it would use to reach the specified destination.

Then try:

```bash
ip route get 8.8.8.8
```

This asks Linux to look up a route to an external IPv4 address.

**Note:** These commands inspect route selection. They do not prove that either destination is reachable.

---

# 9. DevOps Connection: Why Subnet Masks Matter

As a Cloud or DevOps Engineer, you'll encounter subnet prefixes in several environments.

### AWS VPC

An AWS VPC may use:

```text
10.0.0.0/16
```

A subnet inside it might use:

```text
10.0.1.0/24
```

The subnet prefix defines which IPv4 addresses belong to that subnet.

AWS then uses route tables and other network configuration to determine how traffic moves between subnets and other destinations.

### Docker

Docker networks also use IP address ranges and subnet prefixes.

For example, a Docker network might use:

```text
172.20.0.0/16
```

Containers connected to that network receive addresses from the configured address pool, subject to Docker's network configuration.

### Kubernetes

Kubernetes networking involves IP address ranges for Pods and Services, along with routing and network policy considerations.

Understanding CIDR notation is therefore essential for understanding Kubernetes networking.

### Troubleshooting

Subnet misunderstandings can cause problems such as:

- Incorrect static IP configuration.
- Overlapping network ranges.
- Incorrect assumptions about whether two systems are on the same subnet.
- Incorrect routing configurations.

A strong understanding of subnet masks will help you diagnose these issues.

---

# 10. Common Mistakes

### Mistake 1: Assuming matching IP prefixes always mean the same subnet

Two addresses that start with `192.168.1` do not necessarily belong to the same subnet. Their prefix lengths matter.

### Mistake 2: Thinking the subnet mask is the gateway

They serve different purposes.

| Subnet mask | Default gateway |
|---|---|
| Defines the network prefix | Provides a next hop toward other networks |
| Helps determine whether a destination is on-link | Helps forward traffic toward remote destinations |
| Example: `255.255.255.0` | Example: `192.168.1.1` |

### Mistake 3: Thinking all external traffic must use the default gateway

A routing table can contain more-specific routes for other networks. Linux selects the most specific matching route, subject to routing policy and other configuration.

### Mistake 4: Thinking the subnet mask changes the IP address

The subnet mask does not change the configured IP address. It is used with the address to determine the network prefix.

### Mistake 5: Assuming a matching subnet guarantees connectivity

Two devices can belong to the same subnet and still be unable to communicate because of firewall rules, wireless client isolation, missing ARP resolution, or other problems.

---

# 11. Interview Questions and Answers

**Q1. What is a subnet mask?**

A subnet mask is a 32-bit value that identifies the network prefix and host portion of an IPv4 address.

**Q2. What is the subnet mask for `/24`?**

`255.255.255.0`.

**Q3. How do you calculate a network address?**

Perform a bitwise AND between the IPv4 address and its subnet mask.

**Q4. How does a computer determine whether an IPv4 destination is local?**

It uses its IP configuration and routing table to determine whether the destination is on-link or should be reached through a next hop.

**Q5. What happens when the destination is on a different subnet?**

The computer selects a matching route. If that route uses a gateway, it sends the packet toward that gateway.

**Q6. Does a remote destination's IP address change when the laptop sends traffic through a router?**

Normally, the destination IP remains unchanged as the packet traverses routers. NAT and other specialized network functions can modify IP addresses.

**Q7. What is the difference between a subnet mask and a CIDR prefix?**

They express the same prefix information in different forms. For example, `255.255.255.0` is equivalent to `/24`.

---

# 12. Quick Revision

Remember these five points:

1. **A subnet mask identifies the network prefix of an IPv4 address.**
2. **A `/24` prefix corresponds to `255.255.255.0`.**
3. **The network address is calculated using IP address AND subnet mask.**
4. **A computer uses its network configuration and routing table to determine how to reach a destination.**
5. **Local traffic is sent directly on the local network; remote traffic is forwarded according to the routing table.**

## Practice Exercises

Use these configurations:

**Exercise 1**

```text
Your IP:       192.168.10.15
Subnet mask:   255.255.255.0
Destination:   192.168.10.50
```

Calculate both network addresses. Is the destination on the same subnet?

**Exercise 2**

```text
Your IP:       192.168.10.15/24
Destination:   192.168.20.50
```

Determine whether the destination belongs to the same subnet.

**Exercise 3**

On Linux, run:

```bash
ip addr
ip route
```

Identify your interface's IPv4 address, prefix length, directly connected route, and default route if present.

---

**Next lecture: Lecture 06 — Default Gateways and Router Roles.**

We'll explore how packets leave the local network and how routers forward them toward remote destinations.