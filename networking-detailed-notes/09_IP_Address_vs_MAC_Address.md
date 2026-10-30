# Lecture 09: IP Address vs. MAC Address — Understanding the Differences

**Course:** Networking for DevOps  
**Lecture:** 09  
**Main topics:** IP vs. MAC, logical addressing, address stability, routing, local delivery, and introduction to ARP.

This lesson follows the topics in your lecture summary. We'll connect them to what you've already learned about subnet masks, default gateways, and MAC address structure, then practise using Linux commands.

---

# 1. IP Address vs. MAC Address: The Basic Difference

Every time data travels across a network, devices need ways to identify the source and destination.

Two important types of addresses help with this:

- **IP address:** Used for communication at the network layer and for routing packets between networks.
- **MAC address:** Used for link-layer delivery over technologies such as Ethernet.

Let's look at an example.

Suppose your laptop connects to a home Wi-Fi network.

Its network interface might have:

```text
IP address:  192.168.1.10
MAC address: A4:5E:60:C2:10:9B
```

These addresses identify different things at different layers of communication.

The IP address tells the networking system where the device is addressed within the IP network. The MAC address identifies the interface for local link-layer communication.

## Comparison table

| Feature | IP Address | MAC Address |
|---|---|---|
| Full name | Internet Protocol address | Media Access Control address |
| Purpose | Network-layer addressing and routing | Link-layer delivery |
| OSI layer | Layer 3 — Network | Layer 2 — Data Link |
| IPv4 address size | 32 bits | 48 bits for conventional Ethernet |
| Format | `192.168.1.10` | `A4:5E:60:C2:10:9B` |
| Representation | Decimal octets | Hexadecimal bytes |
| Address structure | Network prefix and host portion, as defined by the subnet | Assigned address bits; conventional global addresses include an OUI |
| Can it change? | Yes | Yes, although factory-assigned addresses commonly remain stable |
| Used by routers for path selection? | Yes | Not for IP route selection |
| Used for local Ethernet delivery? | Not by itself | Yes |

**Remember:** IP addresses and MAC addresses are not alternatives to each other. They perform different jobs and work together.

---

# 2. IP Addresses: Logical Addressing

An IP address is a logical network-layer address.

For IPv4, it contains 32 bits, usually written as four decimal octets separated by dots.

Example:

```text
192.168.1.10
```

Each octet represents eight bits.

```text
192 . 168 . 1 . 10
 8      8    8    8  = 32 bits
```

## 2.1 Why is an IP address called logical?

An IP address is assigned or configured according to the network in which an interface operates.

For example, the same laptop could use different IP addresses on different networks:

| Location | Example IPv4 address |
|---|---|
| Home network | `192.168.1.10` |
| College network | `10.20.5.18` |
| Cloud virtual network | `10.0.1.25` |

These are illustrative addresses.

The physical laptop does not have to change for its IP address to change.

The network configuration determines which IP address is appropriate.

## 2.2 Static and dynamic IP addresses

There are two common ways an IP address can be assigned.

### Static IP address

An address is configured manually or reserved through network infrastructure so that the interface consistently receives the intended address.

For example:

```text
192.168.1.10/24
```

Static configuration is useful when a predictable address is needed, although the correct configuration depends on the network.

### Dynamic IP address

An address is assigned automatically, commonly through DHCP in IPv4 networks.

For example:

```text
First connection: 192.168.1.10
Later connection: 192.168.1.15
```

A change is possible, but not guaranteed. A DHCP server may give the same address to a device again.

### Why this matters

A device's IP address can change when it moves between networks or receives a different DHCP lease.

This flexibility allows IP addressing to reflect the network where the device is currently connected.

---

# 3. MAC Addresses: Link-Layer Addressing

A conventional Ethernet MAC address contains 48 bits, represented as six hexadecimal byte pairs.

Example:

```text
A4:5E:60:C2:10:9B
```

A MAC address is associated with a network interface, such as a Wi-Fi or Ethernet adapter.

## 3.1 Why is it different from an IP address?

A factory-assigned MAC address normally remains associated with the same network interface even when the interface receives a different IP address.

For example:

```text
Network 1:
IP:  192.168.1.10
MAC: A4:5E:60:C2:10:9B

Network 2:
IP:  10.0.0.25
MAC: A4:5E:60:C2:10:9B
```

In this example, the IP address changes, but the MAC address remains the same.

This illustrates the difference between network-layer addressing and link-layer addressing.

**Important technical detail:** MAC addresses are not guaranteed to be permanent. They can be randomized or changed by software, and virtual interfaces can have their own MAC addresses.

For this lesson, the useful distinction is that IP addresses are assigned according to network configuration, while factory-assigned MAC addresses commonly remain stable for a particular interface.

---

# 4. Understanding the Hierarchical Structure of IP Addresses

One of the most important differences between IP addresses and MAC addresses is how their structure is used.

IP addressing supports hierarchical routing.

Let's revisit CIDR from Lecture 04.

Suppose a computer has this address:

```text
192.168.1.10/24
```

The `/24` indicates that the first 24 bits form the network prefix.

The remaining eight bits form the host portion of the address.

For this example:

```text
IP address: 192.168.1.10/24
Network:    192.168.1.0/24
Host:       10 (last octet)
```

The network contains addresses from:

```text
192.168.1.0
       to
192.168.1.255
```

In a conventional IPv4 `/24` subnet, `.0` is the network address and `.255` is the broadcast address. The ordinary assignable host range is `.1` through `.254`.

## 4.1 Why does this structure matter?

Routers examine destination IP addresses and compare them with routes in their routing tables.

For example:

```text
Destination: 192.168.2.20
Route:       192.168.2.0/24
```

A route for `192.168.2.0/24` covers the destination `192.168.2.20`.

This allows routers to select an appropriate next hop.

Routers generally use the **most specific matching route**, subject to routing policy and other route-selection rules.

### Example routing table

```text
192.168.1.0/24  -> Directly connected
192.168.2.0/24  -> Via 192.168.1.1
0.0.0.0/0       -> Via 192.168.1.254
```

This is an illustrative table.

It means:

- Destinations in `192.168.1.0/24` use the directly connected network.
- Destinations in `192.168.2.0/24` use the next hop `192.168.1.1`.
- Destinations without a more-specific matching route may use the default route through `192.168.1.254`.

This is why IP addresses have logical significance for routing.

## 4.2 Does a MAC address provide the same routing hierarchy?

Not in the same way.

A conventional MAC address may contain an OUI associated with an assigned address block, but Ethernet switches do not use that prefix to determine an IP route across the internet.

Instead, a switch learns MAC addresses and associates them with local switch ports.

For example:

| MAC address | Switch port |
|---|---|
| `AA:AA:AA:AA:AA:AA` | Port 1 |
| `BB:BB:BB:BB:BB:BB` | Port 2 |
| `CC:CC:CC:CC:CC:CC` | Port 3 |

If a switch receives a frame addressed to `BB:BB:BB:BB:BB:BB`, it can use its MAC address table to determine the appropriate port.

**Key distinction:** IP addressing supports hierarchical routing between networks. MAC addressing supports delivery over a local link.

---

# 5. Why Do We Need Both IP and MAC Addresses?

Imagine you want to send a parcel to someone in another country.

You need two kinds of information:

1. Information identifying the destination and helping the parcel move through the delivery system.
2. Information that helps the local delivery service deliver it to the intended recipient at the final location.

This is a simplified analogy for IP and MAC addressing.

- **IP address:** Helps packets reach their destination across interconnected networks.
- **MAC address:** Helps deliver frames over the current local link.

Neither address replaces the other.

## Example: Your laptop communicates with an AWS EC2 server

Suppose your laptop wants to reach an application running on an EC2 instance.

For illustration:

```text
Laptop private IP: 192.168.1.10
Router:            192.168.1.1
EC2 public IP:     203.0.113.50
```

`203.0.113.50` is a documentation-only example address, not a real EC2 endpoint.

The communication involves several steps.

### Step 1: Your laptop identifies the destination IP

Your laptop determines that the destination is outside its local subnet.

It looks up a suitable route and selects the next hop, commonly the default gateway.

### Step 2: Your laptop determines the gateway's MAC address

For IPv4 on a conventional Ethernet or Wi-Fi LAN, the laptop can use ARP to discover the gateway's local MAC address if it is not already cached.

### Step 3: Your laptop creates a frame for the gateway

The outgoing frame contains:

```text
Source MAC:      Laptop's MAC
Destination MAC: Gateway's MAC

Source IP:       Laptop's IP
Destination IP:  EC2 server's IP
```

Notice that the destination MAC is the gateway's MAC, while the destination IP is the remote server's IP.

### Step 4: Routers forward the packet

The router examines the IP packet and forwards it toward the next hop.

Each router uses its routing information to select where the packet should go next.

### Step 5: Link-layer addressing changes along the path

When a router forwards an IP packet onto another link, it creates a new link-layer frame appropriate for that link.

Consequently, the frame's source and destination MAC addresses normally change at each routed hop.

The IP addresses generally remain the same end-to-end, except where mechanisms such as NAT or other address translation modify them.

### Visual summary

```text
YOUR LAPTOP
     |
     | Ethernet/Wi-Fi frame
     | Destination MAC = local gateway
     | Destination IP  = remote server
     v
LOCAL ROUTER
     |
     | Routes IP packet
     | Creates frame for next link
     v
OTHER NETWORKS
     |
     | Additional routing hops
     v
DESTINATION NETWORK
     |
     | Final local-link delivery
     v
EC2 SERVER
```

This is the fundamental reason both addressing systems are needed.

---

# 6. MAC Addresses Are Local to Each Link

Your lecture describes MAC addresses as being used strictly inside local networks. For introductory learning, think of them as link-layer addresses used for local delivery.

There is an important nuance: Ethernet is used in many networks, including data centres and cloud infrastructure, but a MAC address is not normally carried unchanged across a routed internet path.

Let's revisit the two networks from Lecture 07.

```text
Network A                         Network B

A1 -------- Router --------------- B3
192.168.1.2                       192.168.2.4
```

Suppose A1 sends an IP packet to B3.

### On Network A

The Ethernet frame is addressed to the router's Network A MAC address.

```text
Source MAC:      A1's MAC
Destination MAC: Router A's MAC

Source IP:       192.168.1.2
Destination IP:  192.168.2.4
```

### On Network B

The router forwards the packet in a new Ethernet frame.

```text
Source MAC:      Router B's MAC
Destination MAC: B3's MAC

Source IP:       192.168.1.2
Destination IP:  192.168.2.4
```

The IP destination remains B3, but the MAC addresses differ between the two links.

This is why you should not think of a MAC address as an internet-wide delivery address.

---

# 7. Introduction to ARP: Connecting IP and MAC Addresses

Now we reach the final topic in your Lecture 09 summary: **ARP (Address Resolution Protocol).**

ARP helps IPv4 devices discover the MAC address associated with an IPv4 address on the local network.

Imagine your computer knows:

```text
Destination IP: 192.168.1.20
```

But it doesn't know the destination's MAC address.

How can it construct an Ethernet frame?

It needs to resolve the IPv4 address to a MAC address.

That is where ARP comes in.

## 7.1 Example ARP process

Suppose:

```text
Computer A
IP:  192.168.1.10
MAC: AA:AA:AA:AA:AA:AA

Computer B
IP:  192.168.1.20
MAC: BB:BB:BB:BB:BB:BB
```

Computer A wants to send an IP packet to Computer B.

### Step 1: Computer A checks its ARP cache

The operating system checks whether it already knows the MAC address associated with `192.168.1.20`.

If it has a usable entry, it can use that information.

### Step 2: Computer A broadcasts an ARP request

If the address is unknown, Computer A can send an ARP request on the local network asking which device owns `192.168.1.20`.

Conceptually:

```text
"Who has 192.168.1.20?
Tell 192.168.1.10."
```

### Step 3: Computer B responds

Computer B recognizes its IP address and replies with its MAC address.

Conceptually:

```text
"192.168.1.20 is at BB:BB:BB:BB:BB:BB."
```

### Step 4: Computer A stores the mapping

Computer A can store the result in its neighbor cache for future communication.

### Step 5: Computer A sends the frame

Computer A now knows the destination MAC address and can construct the Ethernet frame.

```text
Source MAC:      AA:AA:AA:AA:AA:AA
Destination MAC: BB:BB:BB:BB:BB:BB
```

### ARP flow diagram

```text
Computer A                         Computer B
192.168.1.10                       192.168.1.20
      |                                  |
      | ARP request (broadcast)          |
      |--------------------------------->|
      |                                  |
      | ARP reply: B's MAC address       |
      |<---------------------------------|
      |                                  |
      | Ethernet frame containing IP     |
      | packet for B                     |
      |--------------------------------->|
```

**Important:** ARP is used to resolve IPv4 addresses to link-layer addresses on the local network. When a destination is remote, the computer typically resolves the MAC address of its next-hop gateway rather than ARPing for the remote server.

ARP is not used to resolve IPv6 addresses. IPv6 uses Neighbor Discovery Protocol (NDP) for related functions.

We'll explore ARP more deeply in Lecture 10.

---

# 8. Practical Linux Lab

Let's verify these concepts on your Linux laptop.

## Step 1: Check your IPv4 address

Run:

```bash
ip -4 addr show
```

Look for an entry such as:

```text
inet 192.168.1.10/24
```

This shows an IPv4 address and prefix assigned to an interface.

Your actual address may differ.

## Step 2: Check your MAC address

Run:

```bash
ip link show
```

Example:

```text
link/ether a4:5e:60:c2:10:9b
```

The value following `link/ether` is the interface's current Ethernet-style MAC address.

## Step 3: Check your routing table

Run:

```bash
ip route
```

Example:

```text
default via 192.168.1.1 dev wlp2s0
192.168.1.0/24 dev wlp2s0 proto kernel scope link
```

The first route indicates the default next hop. The second indicates a directly connected subnet.

Your actual routing table may differ.

## Step 4: Inspect the route to an external IP

Run:

```bash
ip route get 8.8.8.8
```

This shows which route and next hop Linux selects for that destination.

It does not guarantee that the destination is reachable.

## Step 5: Inspect the neighbor cache

Run:

```bash
ip neigh
```

You may see output resembling:

```text
192.168.1.1 dev wlp2s0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
```

This means Linux has a neighbor entry associating the gateway's IPv4 address with a link-layer address.

The example MAC address is illustrative.

## Step 6: Observe ARP with a packet capture

If `tcpdump` is installed, you can inspect ARP traffic on your Wi-Fi interface:

```bash
sudo tcpdump -i wlp2s0 -nn arp
```

This listens for ARP packets. It may show nothing if no ARP traffic occurs while the capture is running.

To generate traffic that may require address resolution, communicate with a device on your local network that is not already in the neighbor cache.

Stop the capture with **Ctrl+C**.

Replace `wlp2s0` with your actual interface name if necessary.

---

# 9. How This Connects to Cloud and DevOps

These concepts become useful when you work with AWS, virtual machines, Docker, and Kubernetes.

### AWS

When an EC2 instance communicates with another IP endpoint, routing tables determine the path. Security groups and network ACLs may also affect whether communication is permitted.

The instance's network interface has associated addressing information, and its private IP address is used for communication within the applicable network configuration.

### Docker

Containers can have virtual network interfaces and IP addresses. Their communication may involve bridges, routing, and network address translation.

A container's virtual interface can also have a MAC address.

### Troubleshooting

If two systems cannot communicate, ask:

1. Does the source have a valid IP address?
2. Is the destination on the same subnet or a remote network?
3. Does the routing table select an appropriate next hop?
4. Can the source resolve the next-hop MAC address when needed?
5. Are firewalls or security controls blocking traffic?
6. Is the destination service running and listening?

This sequence helps separate addressing problems from routing, link-layer, and application problems.

---

# 10. Interview Questions and Answers

### Q1. Why do networks need both IP and MAC addresses?

IP addresses support network-layer communication and routing. MAC addresses support link-layer delivery over the local network link.

### Q2. Which address is used by a router to choose the next hop?

The router uses the destination IP address and its routing information to select the next hop.

### Q3. Does a MAC address normally remain unchanged when a device moves to another IP network?

A factory-assigned MAC address commonly remains stable, but the active address can be changed or randomized. It is not guaranteed to remain unchanged.

### Q4. What happens to MAC addresses when an IP packet crosses a router?

The router normally removes the incoming link-layer encapsulation and creates a new frame for the outgoing link. The frame's MAC addresses therefore change.

### Q5. What does ARP do?

ARP resolves an IPv4 address to a link-layer address on the local network.

### Q6. Does a computer use ARP to discover the MAC address of a remote internet server?

Normally, no. If the server is outside the local subnet, the computer resolves the MAC address of its next-hop gateway.

### Q7. What does `/24` mean in an IPv4 address?

It means the first 24 bits are the network prefix, leaving eight bits outside the prefix for the host portion.

### Q8. What is the difference between an IP routing table and a MAC address table?

An IP routing table helps determine where to forward IP packets. A switch's MAC address table associates learned MAC addresses with switch ports.

---

# 11. Quick Revision Cheat Sheet

| Concept | Key point |
|---|---|
| IPv4 address | 32 bits |
| Conventional Ethernet MAC address | 48 bits |
| IP address | Supports network-layer addressing and routing |
| MAC address | Supports local link-layer delivery |
| Static IP | Manually configured or predictably assigned |
| Dynamic IP | Commonly assigned through DHCP |
| CIDR `/24` | 24-bit network prefix |
| Router | Forwards IP packets between networks |
| Switch | Uses MAC address information to forward Ethernet frames |
| ARP | Resolves IPv4 addresses to local link-layer addresses |
| Linux IP command | `ip -4 addr show` |
| Linux MAC command | `ip link show` |
| Linux routing command | `ip route` |
| Linux neighbor command | `ip neigh` |

## The most important rule

**IP gets the packet routed toward the destination; MAC addressing delivers the frame over the current local link.**

---

## Lecture 09 Completed

You have now covered all five topics from your supplied summary:

1. IP and MAC address structures.
2. Address mutability and stability.
3. IP hierarchy versus MAC addressing.
4. Why both addressing systems are needed.
5. Introduction to ARP.

**Next in your lecture sequence: Lecture 10 — ARP (Address Resolution Protocol).**

That lesson will build on the introduction here and explain ARP requests, replies, caches, and how Linux uses neighbor information.