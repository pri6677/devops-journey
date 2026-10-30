# Lecture 07: How Default Gateways Facilitate Network Communication

**Networking for DevOps — Lecture 07**

In this lesson, we'll connect the concepts from Lectures 03–06: IP addresses, network and host portions, CIDR, subnet masks, and default gateways. We'll see how devices communicate **within the same network and across different networks**.

## 1. Learning Objectives

By the end of this lecture, you should understand:

- How a device determines whether a destination is on its local network.
- Why devices can communicate directly within the same subnet.
- Why communication between different subnets requires routing.
- How a router forwards packets between networks.
- How to inspect routing information on Linux.
- How these concepts apply to AWS and DevOps infrastructure.

---

## 2. Understanding the Network Setup

Our example contains two separate networks connected by a router.

- **Network A:** `192.168.1.0/24`
- **Network B:** `192.168.2.0/24`

Each network contains three hosts. The router has an interface connected to each network.

### Network topology

```text
             NETWORK A
           192.168.1.0/24
                  |
       +----------+----------+
       |          |          |
      A1         A2         A3
 192.168.1.2  .1.3       .1.4
       |          |          |
       +----------+----------+
                  |
          Router Interface A
           192.168.1.1
                  |
             +---------+
             | ROUTER  |
             +---------+
                  |
          Router Interface B
           192.168.2.1
                  |
       +----------+----------+
       |          |          |
      B1         B2         B3
 192.168.2.2  .2.3       .2.4
       |          |          |
       +----------+----------+
                  |
             NETWORK B
           192.168.2.0/24
```

*Note: This is a logical diagram. In a typical Ethernet setup, hosts connect through switches, and the router connects to each network.*

### IP addressing table

| Device | IP address | Network |
|---|---|---|
| A1 | `192.168.1.2/24` | Network A |
| A2 | `192.168.1.3/24` | Network A |
| A3 | `192.168.1.4/24` | Network A |
| Router interface A | `192.168.1.1/24` | Network A |
| B1 | `192.168.2.2/24` | Network B |
| B2 | `192.168.2.3/24` | Network B |
| B3 | `192.168.2.4/24` | Network B |
| Router interface B | `192.168.2.1/24` | Network B |

Both networks use the subnet mask `255.255.255.0`, equivalent to `/24`.

**Important:** The router has an IP address on each network. Hosts in Network A use `192.168.1.1` as their gateway, while hosts in Network B use `192.168.2.1`.

---

## 3. Scenario 1: Communication Within the Same Network

Suppose **A1 wants to send data to A3**.

- A1's IP: `192.168.1.2`
- A3's IP: `192.168.1.4`
- Subnet mask: `255.255.255.0`

### Step 1: A1 identifies its network

A1 applies its subnet mask to its own IP address.

```text
IP address:  192.168.1.2
Subnet mask: 255.255.255.0
             ----------------
Network ID:  192.168.1.0
```

A1 belongs to the network `192.168.1.0/24`.

### Step 2: A1 checks the destination

A1 checks A3's destination IP using the same subnet mask.

```text
Destination IP: 192.168.1.4
Subnet mask:    255.255.255.0
                ----------------
Network ID:     192.168.1.0
```

Both calculations produce the same network address:

```text
A1 network: 192.168.1.0
A3 network: 192.168.1.0
```

### Step 3: A1 decides how to send the data

Because both devices are on the same subnet, A1 knows it can communicate directly with A3 at the network layer without sending the packet to its default gateway.

But how does A1 deliver the Ethernet frame to A3?

If A1 does not already know A3's MAC address, it uses **ARP (Address Resolution Protocol)** to discover the MAC address associated with A3's IPv4 address.

A1 then sends an Ethernet frame addressed to A3's MAC address. A switch can forward the frame to A3's port.

### Communication flow

```text
A1
192.168.1.2
   |
   | 1. Checks destination IP
   | 2. Finds destination on same subnet
   | 3. Resolves A3's MAC address if needed
   |
   v
Ethernet Switch
   |
   v
A3
192.168.1.4
```

**Key takeaway:** Communication between devices on the same subnet does not normally require the default gateway.

---

## 4. Scenario 2: Communication Across Different Networks

Now suppose **A1 wants to send data to B3**.

- A1's IP: `192.168.1.2`
- B3's IP: `192.168.2.4`
- Subnet mask: `255.255.255.0`

### Step 1: A1 identifies its own network

```text
A1 IP:       192.168.1.2
Subnet mask: 255.255.255.0
Network ID:  192.168.1.0
```

### Step 2: A1 checks B3's destination IP

A1 applies its own subnet mask to B3's IP address.

```text
B3 IP:       192.168.2.4
Subnet mask: 255.255.255.0
Network ID:  192.168.2.0
```

### Step 3: A1 compares the network addresses

| Comparison | Result |
|---|---|
| A1's network | `192.168.1.0/24` |
| B3's network | `192.168.2.0/24` |
| Do they match? | No |
| Communication type | Across different networks |

A1 determines that B3 is outside its local subnet.

### Step 4: A1 sends the packet to its default gateway

A1 checks its routing table and selects a route to the destination. In this example, assume the applicable route is the default route through `192.168.1.1`.

A1 must send the packet to the router's MAC address on Network A.

If A1 doesn't already know that MAC address, it uses ARP to resolve the gateway's IP address.

The resulting frame has:

- **Source MAC:** A1's MAC address.
- **Destination MAC:** The router's Network A interface MAC address.
- **Source IP:** `192.168.1.2`.
- **Destination IP:** `192.168.2.4`.

Notice the important difference: **the Ethernet frame is addressed to the router, but the IP packet is addressed to B3.**

### Step 5: The router forwards the packet

The router receives the frame through its Network A interface.

It then:

1. Removes the incoming Ethernet frame header and trailer.
2. Examines the destination IP address, `192.168.2.4`.
3. Checks its routing table.
4. Finds that `192.168.2.0/24` is directly connected through its Network B interface.
5. Resolves B3's MAC address if necessary.
6. Creates a new Ethernet frame and forwards the packet toward B3.

The outgoing frame has:

- **Source MAC:** The router's Network B interface MAC address.
- **Destination MAC:** B3's MAC address.
- **Source IP:** Normally still `192.168.1.2`.
- **Destination IP:** Normally still `192.168.2.4`.

The source and destination IP addresses normally remain unchanged across this routing step, assuming there is no NAT or other address translation.

### Complete communication flow

```text
A1                    ROUTER                     B3
 |                       |                        |
 |  IP packet for B3     |                        |
 |---------------------->|                        |
 |  Frame addressed      |                        |
 |  to router's MAC      |                        |
 |                       |                        |
 |                 Checks routing table           |
 |                 Finds Network B                 |
 |                       |                        |
 |                       |  New Ethernet frame     |
 |                       |-----------------------> |
 |                       |                        |
 |                       |             Receives packet
```

**Key takeaway:** When a destination is outside the local subnet, the sending device forwards the packet to an appropriate router. The router determines the next hop using its routing table.

---

## 5. Same-Network vs. Cross-Network Communication

| Feature | Same network | Different networks |
|---|---|---|
| Example | A1 → A3 | A1 → B3 |
| Destination network matches? | Yes | No |
| Default gateway normally required for this destination? | No | Yes, in this example |
| ARP resolves the MAC address of | Destination host | Next-hop gateway |
| Router forwards the packet between networks? | Not normally | Yes |
| Ethernet frame | Addressed to destination host | Initially addressed to gateway |
| Destination IP | Destination host | Destination host |

Remember that ARP is used to resolve IPv4 addresses to MAC addresses on the local link. A host does not normally ARP directly for a remote destination; it resolves the next-hop gateway's MAC address instead.

---

## 6. Practical Linux Lab

Let's connect this lesson to your Linux environment.

### Step 1: Check your IP address and subnet

Run:

```bash
ip -4 addr show
```

Look for an interface such as `wlp2s0`.

You might see an address similar to:

```text
inet 192.168.1.10/24
```

This means the interface has IPv4 address `192.168.1.10` with a `/24` prefix.

Your actual address and subnet may be different.

### Step 2: Check your routing table

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

- `default via 192.168.1.1`: The default route uses `192.168.1.1` as its next hop.
- `dev wlp2s0`: Traffic uses the Wi-Fi interface.
- `192.168.1.0/24 ... scope link`: The connected subnet is directly reachable through that interface.

Your output may differ based on your network configuration.

### Step 3: Check the route to a local destination

Replace the example IP with the IP address of another device on your own network:

```bash
ip route get 192.168.1.20
```

If that destination is on your connected subnet, the result will typically show the local interface without a gateway next hop.

### Step 4: Check the route to an external destination

Run:

```bash
ip route get 8.8.8.8
```

If your default route applies, the output may look similar to:

```text
8.8.8.8 via 192.168.1.1 dev wlp2s0
```

This tells you that the next hop is `192.168.1.1`.

**Note:** `ip route get` performs a local route lookup. It doesn't guarantee that the destination is reachable or that the gateway will successfully forward the packet.

### Step 5: Inspect neighboring devices

Run:

```bash
ip neigh
```

This displays the Linux neighbor table, including discovered IPv4-to-MAC mappings.

You may see entries for your router or other local devices.

---

## 7. How This Connects to AWS and DevOps

The same principles apply when working with cloud infrastructure.

### Example AWS architecture

Imagine an AWS VPC with the CIDR block `10.0.0.0/16`.

Inside it, you create two subnets:

| Component | CIDR |
|---|---|
| VPC | `10.0.0.0/16` |
| Subnet A | `10.0.1.0/24` |
| Subnet B | `10.0.2.0/24` |

Suppose an EC2 instance in Subnet A wants to communicate with an instance in Subnet B.

The communication depends on more than IP addressing:

1. The destination must be covered by an applicable route.
2. The subnet route table must provide a valid path.
3. Security groups and network ACLs must allow the relevant traffic.
4. The destination service must be listening and reachable.

Within a VPC, the local route normally enables communication between VPC subnets, subject to network controls. An internet gateway or NAT gateway is **not automatically required** for communication between those two subnets.

This is why understanding routing and gateways is important when troubleshooting EC2 connectivity, private subnets, and multi-tier applications.

---

## 8. Common Mistakes to Avoid

**Mistake 1: Assuming all communication requires a router**

Devices on the same subnet can normally communicate directly at the IP layer over their local link.

**Mistake 2: Thinking the destination IP changes to the gateway's IP**

The destination IP remains the intended destination, `192.168.2.4`, in our example. The Ethernet frame is addressed to the gateway's MAC address for the first hop.

**Mistake 3: Confusing a gateway with a switch**

- A switch typically forwards Ethernet frames within a Layer 2 network.
- A router forwards IP packets between networks.

**Mistake 4: Assuming the gateway alone guarantees connectivity**

A correct route is necessary, but firewalls, security rules, interface configuration, and the destination service can still prevent communication.

---

## 9. Interview Questions and Answers

### Q1. How does a computer determine whether a destination is on its local network?

It compares the network portion of its own IP address with the network portion of the destination IP address using its subnet mask or prefix.

### Q2. Why does A1 need a gateway to reach B3?

A1 and B3 belong to different IP subnets. A1 forwards the packet to an appropriate next-hop router, which can route it to Network B.

### Q3. Does the destination IP address change when a router forwards a packet?

Normally, no. The destination IP remains the intended destination unless a process such as NAT changes it.

### Q4. Does the destination MAC address change when a packet crosses a router?

Yes. A router creates a new link-layer frame for the outgoing network. The destination MAC address is appropriate for the next hop on that link.

### Q5. Why does A1 not send traffic for B3 directly to B3's MAC address?

A1 cannot ordinarily resolve a remote host's MAC address using ARP across a router. Instead, it resolves the local gateway's MAC address and sends the frame to the router.

### Q6. What is the difference between a routing table and a default gateway?

A routing table contains routes used to choose how traffic should be forwarded. A default gateway is the next-hop router used by a default route when that route is selected.

---

## 10. Quick Revision Cheat Sheet

| Concept | Remember |
|---|---|
| Network A | `192.168.1.0/24` |
| Network B | `192.168.2.0/24` |
| Network A gateway | `192.168.1.1` |
| Network B gateway | `192.168.2.1` |
| Same-subnet destination | Send directly over the local link |
| Different-subnet destination | Send to the selected next hop, often the default gateway |
| ARP | Resolves a local IPv4 next hop to a MAC address |
| Switch | Forwards Ethernet frames |
| Router | Routes IP packets between networks |
| Linux route inspection | `ip route` |
| Linux route lookup | `ip route get <destination-IP>` |
| Linux neighbor table | `ip neigh` |

### The most important rule

**Same subnet → direct local delivery. Different subnet → route through an appropriate next hop.**

---

## 11. Practice Exercises

Try these to strengthen your understanding.

**Exercise 1:** A computer has IP `192.168.1.10/24`. Is `192.168.1.50` on the same subnet?

**Exercise 2:** The same computer wants to reach `192.168.2.50`. Is the destination on the same subnet? What will the computer normally do next?

**Exercise 3:** A1 sends a packet to B3. Which device's MAC address does A1 use in its outgoing Ethernet frame?

**Exercise 4:** When the router forwards the packet from Network A to Network B, does it normally create a new Ethernet frame?

**Exercise 5:** On Linux, which command shows the next hop selected for destination `8.8.8.8`?

---

## Lecture 07 Completed

You have now connected subnet masks, network addresses, default gateways, ARP, switches, and routers into one communication flow.

**Next in your supplied lecture breakdown:** Lecture 08 has not been specified yet, so I won't invent its topic or numbering. Share the Lecture 08 topic breakdown when you're ready, and we'll continue with the same format.