# Networking for DevOps — Lecture 04
## Network vs. Host, CIDR Notation, and IPv4 Address Capacity

**Roadmap position:** Networking — Lecture 04  
**Previous lecture:** IP Address Structure and Binary Representation  
**Today's focus:** Understanding how an IP address is divided into network and host portions, how CIDR notation works, and how to calculate the number of addresses in a subnet.

These concepts are essential for your upcoming topics, including subnet masks, routing, AWS VPCs, Docker networking, and Kubernetes networking.

---

# 1. What Is a Network?

A **network** is a collection of connected devices that can communicate with one another.

For example, imagine your home Wi-Fi network:

```text
                 Internet
                    |
                 Router
                    |
             Home Wi-Fi Network
              /      |      \
          Laptop   Mobile   Tablet
```

Your laptop, mobile phone, and tablet can communicate through the network, subject to the network configuration and security rules.

Each device's network interface can have an IP address.

For example:

| Device | Example IPv4 address |
|---|---|
| Laptop | `192.168.1.10` |
| Mobile | `192.168.1.11` |
| Tablet | `192.168.1.12` |
| Printer | `192.168.1.13` |

These addresses are examples of addresses that could be used on a private home network.

Notice that the first three octets are the same in these examples. However, **matching the first three octets does not, by itself, prove that two addresses belong to the same subnet**. We need the subnet prefix or subnet mask to determine that.

We'll understand why shortly.

---

# 2. What Is a Host?

A **host** is a device connected to a network that can communicate using network protocols.

Examples include:

- A laptop
- A mobile phone
- A web server
- A database server
- A virtual machine on AWS
- A Docker container with its own network interface

Consider this example:

```text
Network: 192.168.1.0/24

        +--------------------------+
        |       Local Network      |
        |                          |
        | Laptop: 192.168.1.10     |
        | Mobile: 192.168.1.11     |
        | Server: 192.168.1.20     |
        |                          |
        +--------------------------+
```

The laptop, mobile, and server are hosts on this network.

### Network vs. host

| Network | Host |
|---|---|
| Identifies a group of addresses belonging to a subnet | A device or network interface using an IP address |
| Describes the network portion of an IP address | Uses an address that includes a host portion |
| Example: `192.168.1.0/24` | Example: `192.168.1.10` |

**Important:** The network address and the host addresses are not interchangeable. The network address identifies the subnet; an ordinary host address identifies an interface within it.

---

# 3. Understanding Network and Host Portions

An IPv4 address contains 32 bits.

Recall from Lecture 03:

```text
IPv4 address: 192.168.1.10

Binary:
11000000.10101000.00000001.00001010
```

But how do computers determine which bits identify the network and which bits identify the host?

They use the **subnet mask**, also represented by a network prefix such as `/24`.

The prefix tells the computer how many leading bits belong to the network portion.

For example:

```text
192.168.1.10/24
```

The `/24` means:

- First 24 bits: network portion
- Remaining 8 bits: host portion

Visual representation:

```text
IPv4 address: 192.168.1.10/24

Network portion          Host portion
       24 bits               8 bits
+------------------------+----------+
| 192.168.1              |    10    |
+------------------------+----------+
```

This dotted-decimal illustration is a convenient shortcut for `/24`. The actual division is between bits, not inherently between decimal octets.

### Why is this division important?

The network portion allows a device to determine which subnet an IP address belongs to.

The host portion identifies an address within that subnet.

This information helps devices decide whether traffic can be sent directly on the local network or should be forwarded through a router.

We'll explore that decision in detail in Lecture 05.

---

# 4. What Is CIDR Notation?

**CIDR** stands for **Classless Inter-Domain Routing**.

CIDR notation expresses an IP address together with a prefix length.

For example:

```text
192.168.1.10/24
```

The components are:

| Component | Meaning |
|---|---|
| `192.168.1.10` | IPv4 address |
| `/24` | Network prefix length |
| `24` | Number of leading network bits |

IPv4 has 32 bits in total.

Therefore, the number of bits left for the host portion is:

$$
\text{Host bits} = 32 - \text{Prefix length}
$$

For `/24`:

$$
32 - 24 = 8
$$

So the host portion has 8 bits.

For `/16`:

$$
32 - 16 = 16
$$

For `/26`:

$$
32 - 26 = 6
$$

### Remember

**A larger CIDR prefix means more bits are reserved for the network portion and fewer bits remain for host addresses.**

For example, `/26` has fewer addresses than `/24`, assuming both are ordinary IPv4 subnet prefixes.

---

# 5. Understanding Common CIDR Prefixes

Let's examine several common prefix lengths.

| CIDR prefix | Network bits | Host bits | Total addresses |
|---|---:|---:|---:|
| `/8` | 8 | 24 | 16,777,216 |
| `/16` | 16 | 16 | 65,536 |
| `/24` | 24 | 8 | 256 |
| `/25` | 25 | 7 | 128 |
| `/26` | 26 | 6 | 64 |
| `/27` | 27 | 5 | 32 |
| `/28` | 28 | 4 | 16 |
| `/29` | 29 | 3 | 8 |
| `/30` | 30 | 2 | 4 |
| `/32` | 32 | 0 | 1 |

The total number of addresses is calculated using:

$$
\boxed{\text{Total addresses} = 2^{\text{Host bits}}}
$$

This is the number of possible address combinations in the subnet.

**Caution:** Total addresses and usable host addresses are not always the same. Traditional IPv4 subnets usually reserve the network and broadcast addresses, while special cases such as `/31` point-to-point networks and `/32` host routes follow different rules.

---

# 6. Calculating the Number of Addresses

Let's work through three examples.

## Example 1: `/24`

Suppose you have:

```text
192.168.1.0/24
```

Step 1: Calculate the host bits.

$$
32 - 24 = 8
$$

Step 2: Calculate the total number of addresses.

$$
2^8 = 256
$$

Therefore:

**A `/24` subnet contains 256 IPv4 addresses.**

For a conventional `/24` subnet, the addresses are:

```text
Network address:   192.168.1.0
First host:        192.168.1.1
Last host:         192.168.1.254
Broadcast address: 192.168.1.255
```

The conventional usable-host count is:

$$
256 - 2 = 254
$$

The two excluded addresses are the network address and the broadcast address.

## Example 2: `/25`

Consider:

```text
192.168.1.0/25
```

Step 1:

$$
32 - 25 = 7
$$

Step 2:

$$
2^7 = 128
$$

Therefore, this subnet contains 128 addresses.

Its conventional range is:

```text
Network address:   192.168.1.0
First host:        192.168.1.1
Last host:         192.168.1.126
Broadcast address: 192.168.1.127
```

Conventional usable-host count:

$$
128 - 2 = 126
$$

## Example 3: `/26`

Consider:

```text
192.168.1.0/26
```

Step 1:

$$
32 - 26 = 6
$$

Step 2:

$$
2^6 = 64
$$

Therefore, this subnet contains 64 addresses.

Its conventional range is:

```text
Network address:   192.168.1.0
First host:        192.168.1.1
Last host:         192.168.1.62
Broadcast address: 192.168.1.63
```

Conventional usable-host count:

$$
64 - 2 = 62
$$

### Compare the results

| Subnet | Total addresses | Conventional usable hosts |
|---|---:|---:|
| `192.168.1.0/24` | 256 | 254 |
| `192.168.1.0/25` | 128 | 126 |
| `192.168.1.0/26` | 64 | 62 |

As the prefix length increases, the subnet becomes smaller.

---

# 7. Understanding DHCP

**DHCP** stands for **Dynamic Host Configuration Protocol**.

It allows devices to obtain network configuration automatically instead of requiring an administrator to configure every address manually.

A DHCP server can provide information such as:

- An IP address
- A subnet mask or prefix
- A default gateway
- DNS server addresses
- A lease duration

For example, when your laptop connects to your home Wi-Fi, it may receive a configuration like this:

```text
IP address:      192.168.1.10
Subnet mask:     255.255.255.0
Default gateway: 192.168.1.1
DNS server:      192.168.1.1
```

The values are illustrative; your actual settings may differ.

## How DHCP works

A typical DHCPv4 exchange follows four steps, often remembered as DORA:

```text
Laptop                         DHCP Server
  |                                 |
  |-------- DHCP Discover -------->|
  |                                 |
  |<--------- DHCP Offer -----------|
  |                                 |
  |-------- DHCP Request ---------->|
  |                                 |
  |<--------- DHCP ACK -------------|
  |                                 |
  |       Configuration received    |
```

The steps are:

1. **Discover:** The client searches for a DHCP server.
2. **Offer:** A server offers configuration.
3. **Request:** The client requests the offered configuration.
4. **Acknowledgment:** The server confirms the assignment.

This is the usual sequence for a new DHCPv4 lease.

### Does DHCP create the network?

No. DHCP provides network configuration. The network and its subnet are defined by the network's design and configuration.

### Does every device always receive its IP address through DHCP?

No. Devices can also use manually configured static IP addresses, and some networks use other address-configuration mechanisms.

---

# 8. Practical Linux Lab

Let's inspect the network configuration on your Zorin OS system.

## Step 1: Find your IP addresses

Run:

```bash
ip addr
```

Look for your Wi-Fi interface, which in your earlier networking work was named `wlp2s0`.

You may see an entry resembling:

```text
inet 192.168.1.10/24
```

This tells you:

- `192.168.1.10` is the configured IPv4 address.
- `/24` is the network prefix.
- The interface has a 24-bit network prefix and 8 host bits.

Your actual address and prefix may be different.

## Step 2: Inspect your routing table

Run:

```bash
ip route
```

Example output:

```text
default via 192.168.1.1 dev wlp2s0
192.168.1.0/24 dev wlp2s0 proto kernel scope link
```

Interpretation:

| Output | Meaning |
|---|---|
| `default` | Default route used when no more-specific route matches |
| `via 192.168.1.1` | Next-hop gateway for that route |
| `dev wlp2s0` | Network interface |
| `192.168.1.0/24` | An on-link subnet route |

This connects the concepts from Lecture 04 to the routing and default-gateway topics in Lectures 05 and 06.

---

# 9. DevOps Connection: CIDR in AWS

CIDR notation is especially important when designing cloud networks.

In AWS, a Virtual Private Cloud (VPC) uses IPv4 CIDR blocks to define address ranges.

For example:

```text
VPC CIDR: 10.0.0.0/16
```

A `/16` contains:

$$
32 - 16 = 16 \text{ host bits}
$$

$$
2^{16} = 65,536 \text{ total IPv4 addresses}
$$

You might divide the VPC address space into smaller subnets, such as:

```text
VPC: 10.0.0.0/16
|
+-- Subnet A: 10
