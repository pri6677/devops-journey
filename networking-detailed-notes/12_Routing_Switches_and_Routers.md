# Networking for DevOps — Lecture 12
# Routing, Switches vs. Routers, and How Packets Travel

**Roadmap position:** Networking → Lecture 12  
**Previous lecture:** Lecture 11 — OSI Model, TCP/IP Model, and the Journey of a Packet

In this lesson, we'll connect several concepts you've already learned:

- IP addresses and subnet masks
- Local networks and remote networks
- MAC addresses and ARP
- Default gateways
- Switches and routers
- NAT and public/private IP addresses
- Communication between your laptop, the internet, and an AWS EC2 instance

The goal is to understand **what actually happens to a packet when it travels from one machine to another**.

---

# 1. What Is Routing?

**Routing is the process of determining where an IP packet should go to reach its destination.**

Imagine sending a parcel from your home to a person in another country. The parcel may travel through several distribution centers before reaching its destination.

Network communication works similarly.

A packet might travel through:

1. The sender's network interface.
2. A local switch or wireless access point.
3. A default gateway router.
4. One or more intermediate routers.
5. The destination network.
6. The destination machine.

Each router uses its routing information to decide where to forward the packet next.

That next step is called a **hop**.

### Example

Suppose your laptop sends a packet to a remote server:

```text
Your Laptop
     |
     v
Home Router
     |
     v
ISP Router
     |
     v
Another Router
     |
     v
Destination Network
     |
     v
Server
```

Each router doesn't necessarily know the complete physical path to the destination. It uses its routing table to select an appropriate next hop or outgoing interface.

The packet moves through the network until it reaches its destination, assuming the route exists and forwarding is permitted.

## What information does a router use?

A router primarily examines the packet's **destination IP address** and consults its routing table.

A simplified routing table might look like this:

| Destination network | Next hop or route |
|---|---|
| `192.168.1.0/24` | Directly connected |
| `192.168.2.0/24` | Via `192.168.1.2` |
| `0.0.0.0/0` | Via `192.168.1.254` |

The actual entries depend on the network.

The route `0.0.0.0/0` is the IPv4 default route. It matches destinations not covered by a more-specific applicable route.

Routers generally use **longest-prefix matching** to select the most specific matching route, subject to routing policies and other forwarding rules.

### Connection to your previous lessons

In Lecture 5, you learned that a device uses its IP address and subnet mask to determine whether a destination is on its local subnet.

In Lecture 6, you learned that a default gateway is used when the routing decision selects the default route.

Now we'll apply those ideas to three practical scenarios.

---

# 2. Switches vs. Routers

Switches and routers both help move network traffic, but they operate differently.

## A. Switches — Layer 2

A network switch connects devices within a local network, such as computers, printers, and servers.

An Ethernet switch forwards frames primarily using **destination MAC addresses**.

For example:

```text
Laptop A                 Laptop B
    |                        |
    |                        |
    +------ Ethernet Switch-+
```

Suppose Laptop A sends a frame to Laptop B.

The switch examines the destination MAC address and checks its MAC address table to determine which port should receive the frame.

### How does a switch learn MAC addresses?

A switch learns from the **source MAC address** of incoming frames.

Imagine Laptop A sends a frame through switch port 1.

The switch learns that Laptop A's source MAC address is reachable through port 1. It performs similar learning for other devices.

A simplified MAC address table might look like this:

| MAC address | Switch port |
|---|---|
| `AA:AA:AA:AA:AA:AA` | Port 1 |
| `BB:BB:BB:BB:BB:BB` | Port 2 |
| `CC:CC:CC:CC:CC:CC` | Port 3 |

When the switch receives a frame destined for a known MAC address, it can forward that frame through the appropriate port.

This is called **unicast forwarding**.

If the destination MAC address is unknown, a typical Ethernet switch floods the frame out eligible ports in the same VLAN, excluding the incoming port. Broadcast frames are also flooded within their broadcast domain, subject to the switch's configuration.

### Important distinction

A switch does not normally need to inspect the destination IP address to decide where to forward an ordinary Ethernet frame.

Its main forwarding decision is based on Layer 2 information.

**Remember:** Switches forward frames within a Layer 2 network using MAC addresses.

---

## B. Routers — Layer 3

A router connects different IP networks and forwards packets between them.

For example:

```text
Network 1                         Network 2
192.168.1.0/24                    192.168.2.0/24

Laptop A                          Laptop X
192.168.1.10                      192.168.2.20
     |                                  |
     v                                  v
     +-------- Router -----------------+
              .1.1             .2.1
```

The router has an interface in each network:

- Network 1 interface: `192.168.1.1`
- Network 2 interface: `192.168.2.1`

When a packet arrives, the router examines its destination IP address and consults its routing table.

If a suitable route exists and forwarding is allowed, the router forwards the packet towards the destination network.

### Switch vs. Router

| Feature | Switch | Router |
|---|---|---|
| Typical OSI layer | Layer 2 | Layer 3 |
| Main forwarding information | MAC address | Destination IP address |
| Data unit handled | Ethernet frame | IP packet |
| Main purpose | Forward traffic within a Layer 2 network | Forward packets between IP networks |
| Routing table | Not required for ordinary Layer 2 switching | Used to select routes |
| Example | Connects laptops within a LAN | Connects a home LAN to an ISP |

**Nuance:** Some switches also perform Layer 3 routing. For this lesson, we're discussing ordinary Layer 2 switches and IP routers.

---

# 3. Scenario A — Laptop A Communicates with Laptop D on the Same Network

Let's consider the first scenario from your lecture.

Suppose four laptops are connected to the same local network.

```text
              Network: 192.168.1.0/24

Laptop A              Switch              Laptop D
192.168.1.10       +-----------+         192.168.1.40
     |-------------|           |--------------|
                   +-----------+
```

Assume these addresses:

| Device | IP address | Subnet |
|---|---|---|
| Laptop A | `192.168.1.10/24` | `192.168.1.0/24` |
| Laptop D | `192.168.1.40/24` | `192.168.1.0/24` |

Both laptops belong to the same IPv4 subnet.

Let's follow the communication.

## Step 1: Laptop A checks the destination

Laptop A wants to send data to:

```text
192.168.1.40
```

It uses its routing information and subnet configuration to determine that the destination is directly reachable on the local network.

It does **not** need to send the packet to its default gateway for ordinary communication with this directly connected destination.

## Step 2: Laptop A checks its neighbor cache

Laptop A needs the destination's MAC address to create the local Ethernet frame.

It first checks whether it already has a valid neighbor entry for `192.168.1.40`.

If the mapping is available, it can use it.

If the mapping is not available, Laptop A can use ARP to discover the destination's MAC address.

## Step 3: Laptop A sends an ARP request if needed

Suppose Laptop A does not know Laptop D's MAC address.

It sends an ARP request asking which device owns `192.168.1.40`.

A simplified request looks like this:

```text
Who has 192.168.1.40?

Tell 192.168.1.10.
```

The ARP request is broadcast on the local Layer 2 network.

Laptop D recognizes its IP address and replies with its MAC address.

For example:

```text
192.168.1.40 is at BB:BB:BB:BB:BB:BB
```

These MAC addresses are illustrative.

## Step 4: Laptop A creates an Ethernet frame

Laptop A now knows Laptop D's MAC address.

It creates a frame containing:

```text
Source MAC:      Laptop A's MAC
Destination MAC: Laptop D's MAC

Source IP:       192.168.1.10
Destination IP:  192.168.1.40
```

Notice that the destination MAC belongs to Laptop D, not the default gateway.

## Step 5: The switch forwards the frame

The switch examines the destination MAC address.

If its MAC address table identifies the port connected to Laptop D, it forwards the frame through that port.

Laptop D receives the frame, processes the IP packet, and delivers the data to the appropriate transport endpoint and application.

### Does the packet need a router?

**No, not for ordinary communication between these two devices on the same directly connected subnet.**

The switch forwards the frame locally.

A router may still exist on the network, but it is not required to route this particular communication.

### Scenario A summary

```text
Laptop A
   |
   | Checks destination subnet
   |
   | Same subnet
   v
ARP resolves Laptop D's MAC if needed
   |
   v
Switch forwards the frame
   |
   v
Laptop D
```

**Key takeaway:** For same-subnet communication, the sender normally resolves the destination's MAC address and sends the frame directly across the local network.

---

# 4. Scenario B — Laptop C Communicates with Laptop X on a Different Network

Now consider two separate local networks.

```text
Network 1: 192.168.1.0/24

Laptop C
192.168.1.10
     |
     v
   Switch 1
     |
     v
Router interface: 192.168.1.1
     |
   [ ROUTER ]
     |
Router interface: 192.168.2.1
     |
     v
   Switch 2
     |
     v
Laptop X
192.168.2.20

Network 2: 192.168.2.0/24
```

The router connects both networks.

Let's follow the packet.

## Step 1: Laptop C checks the destination network

Laptop C has:

```text
IP address: 192.168.1.10/24
```

Laptop X has:

```text
IP address: 192.168.2.20
```

Laptop C determines its own network:

```text
192.168.1.0/24
```

The destination belongs to:

```text
192.168.2.0/24
```

These are different networks.

## Step 2: Laptop C consults its routing table

Laptop C looks for a route to the destination.

If no more-specific route matches, it may use its default route, which points to the default gateway.

Suppose the gateway is:

```text
192.168.1.1
```

Laptop C needs the gateway's MAC address to send the frame across its local network.

If the mapping is not already available, Laptop C uses ARP to discover it.

**Important:** Laptop C does not use ARP to discover Laptop X's MAC address across the remote network. ARP is used for local link-layer resolution.

## Step 3: Laptop C sends the frame to the router

The frame contains:

```text
Source MAC:      Laptop C's MAC
Destination MAC: Router's Network 1 MAC

Source IP:       192.168.1.10
Destination IP:  192.168.2.20
```

The destination MAC is the router's MAC on Network 1.

The destination IP remains Laptop X's IP address.

This is the critical difference between MAC addressing and IP addressing.

## Step 4: The router receives the frame

The router receives the Ethernet frame addressed to its local interface.

It removes the incoming Layer 2 framing and examines the IP packet.

It then checks its routing table and determines that `192.168.2.0/24` is reachable through its Network 2 interface.

## Step 5: The router resolves Laptop X's MAC address if needed

The router needs to send a frame over Network 2.

If it does not already know Laptop X's MAC address, it uses ARP on Network 2 to resolve the mapping.

Laptop X responds with its MAC address.

The router can then create a new frame for the outgoing link.

## Step 6: The router forwards the packet

The new frame contains:

```text
Source MAC:      Router's Network 2 MAC
Destination MAC: Laptop X's MAC

Source IP:       192.168.1.10
Destination IP:  192.168.2.20
```

The MAC addresses have changed to match the outgoing network.

The IP addresses remain the same in this example because no NAT is being performed.

The router also decreases the IPv4 TTL when forwarding the packet.

## Step 7: Switch 2 delivers the frame

Switch 2 forwards the frame to Laptop X using its destination MAC address.

Laptop X receives the packet and delivers the data to the appropriate application.

### Scenario B summary

```text
Laptop C
    |
    | Destination is on another subnet
    v
Default gateway
    |
    | Router checks destination IP
    v
Router selects route to Network 2
    |
    | Creates a new Layer 2 frame
    v
Switch 2
    |
    v
Laptop X
```

**Key takeaway:** When a destination is on a different network, the sender forwards the packet to an appropriate next hop, commonly its default gateway. The router forwards the packet towards the destination network.

---

# 5. Scenario C — Your Laptop Communicates with an AWS EC2 Instance Across the Internet

Now let's connect the lecture to your AWS journey.

Suppose you want to connect from your laptop in India to an EC2 instance in AWS.

For this example, assume:
- Your laptop has a private IPv4 address on your home network.
- Your home router provides internet connectivity.
- The EC2 instance has a public IPv4 address.
- The AWS network configuration permits the intended connection.

A simplified diagram:

```text
Your Laptop
Private IP: 192.168.1.10
       |
       v
Home Wi-Fi / Switch
       |
       v
Home Router
       |
       | Source NAT, typically
       v
Internet Service Provider
       |
       v
Intermediate Internet Routers
       |
       v
AWS Network Edge
       |
       v
AWS VPC / Subnet
       |
       v
EC2 Instance
Private IP: 10.0.1.10
Public IP:  example public address
```

The addresses shown are illustrative. The EC2 private address is an example, and the public address is intentionally not specified.

Let's break down the process.

## Step 1: Your laptop prepares the packet

Suppose you connect to an EC2 instance using SSH.

A simplified command might be:

```bash
ssh -i aws-demo.pem ec2-user@<EC2_PUBLIC_IP>
```

Replace `<EC2_PUBLIC_IP>` with the actual public IPv4 address of your instance.

The command assumes that the instance uses the `ec2-user` account. The correct username depends on the operating system image.

SSH commonly uses TCP port `22`.

The SSH client creates a connection to the instance's public IP address.

## Step 2: Your laptop checks its routing table

Run:

```bash
ip route
```

On a typical home network, you'll find a default route through your home router.

For example:

```text
default via 192.168.1.1 dev wlp2s0
```

This is an illustrative example, not a guarantee of your actual routing configuration.

Because the EC2 public IP is not on your local subnet, your laptop sends the traffic to the appropriate next hop, typically the home router.

## Step 3: Your laptop resolves the gateway's MAC address

Your laptop needs the local gateway's MAC address to transmit a frame over the Wi-Fi link.

It checks its neighbor table:

```bash
ip neigh show
```

If the necessary entry is missing, it may use ARP to discover the gateway's MAC address.

Your laptop then creates a frame addressed to the local gateway.

The IP packet's destination remains the EC2 public IP.

## Step 4: Your home router performs NAT

On many home networks, the router performs **Network Address Translation (NAT)**.

Your laptop might have:

```text
Private IP: 192.168.1.10
```

Your home router may have a public IP address assigned by your ISP.

When your laptop initiates an internet connection, the router commonly translates the source address from the private address to its public address and tracks the connection so response traffic can be mapped back to the laptop.

Conceptually:

**Before source NAT:**

```text
Source IP:      192.168.1.10
Destination IP: EC2 public IP
```

**After source NAT:**

```text
Source IP:      Home router's public IP
Destination IP: EC2 public IP
```

The exact translation behavior depends on the router and network configuration.

### Is NAT always required?

No. NAT is common in home IPv4 networks, but it is not a universal requirement for IP routing. Some networks use public addresses directly or use other addressing and translation arrangements.

Also, NAT is not the same thing as a firewall. NAT does not, by itself, guarantee that a connection is secure.

## Step 5: The packet crosses the internet

The traffic travels through the ISP's network and may cross multiple routers.

Each router uses its routing information to forward the packet towards the destination.

The physical path can vary over time.

You can think of this as a series of hops:

```text
Home Router
     |
     v
ISP Router
     |
     v
Transit Router
     |
     v
Another Network
     |
     v
AWS Network
```

Your laptop doesn't need to know every router in advance. It sends the packet to its next hop, and each router makes its own forwarding decision.

## Step 6: The traffic reaches AWS

AWS networking infrastructure delivers traffic towards the relevant destination.

For a typical public IPv4 EC2 instance, the public IPv4 address is associated with a private IPv4 address in the VPC.

AWS provides the networking behavior that connects the public address to the instance's private address.

At a simplified level, traffic must be able to reach the instance through the appropriate AWS network path.

For an SSH connection to succeed, check all relevant requirements, including:

- The instance is running and has the intended public IPv4 address.
- The subnet's route table supports the required path.
- The security group permits inbound TCP port `22` from your source.
- Network ACLs permit the required traffic.
- The operating system's firewall permits the connection.
- The SSH service is running and configured correctly.
- You use the correct username and key.

Having a public IP address alone does not guarantee internet reachability.

## Step 7: The EC2 instance replies

The EC2 instance processes the incoming connection and sends response traffic.

The response follows a suitable return route.

Your home router uses its NAT connection-tracking information, where applicable, to translate the returning traffic back to your laptop's private address.

Your SSH client receives the response and continues the session.

### Scenario C summary

```text
Laptop
   |
   | Private IPv4 source
   v
Home Router
   |
   | Source NAT, if configured
   v
ISP and Internet Routers
   |
   v
AWS Networking
   |
   v
EC2 Instance
   |
   | Response traffic
   v
Return path through the network
   |
   v
Home Router
   |
   | Reverse translation, if applicable
   v
Laptop
```

**Key takeaway:** Connecting to an EC2 instance involves routing through multiple networks. NAT may translate addresses, and AWS routing and security configuration determine whether traffic can reach the instance.

---

# 6. The Golden Rules of Packet Travel

Your lecture summarizes packet travel using two rules. These are excellent starting points, with one important refinement.

## Rule 1: IP addresses normally remain the same end-to-end

Consider the connection in Scenario B:

```text
Source IP:      192.168.1.10
Destination IP: 192.168.2.20
```

As the packet crosses an ordinary router, the source and destination IP addresses normally remain the same.

The router forwards the packet towards the destination and decreases the IPv4 TTL.

However, **IP addresses are not guaranteed to remain unchanged across every network path**.

For example, NAT can modify:
- The source IP address, as with common outbound home-router NAT.
- The destination IP address, as with destination NAT or port forwarding.
- Both source and destination addresses in some configurations.

So the more accurate rule is:

**IP addresses normally remain unchanged across ordinary routing hops, unless a mechanism such as NAT modifies them.**

## Rule 2: MAC addresses change when the packet crosses a router

Consider a packet travelling from Laptop C to Laptop X.

On Network 1:

```text
Source MAC:      Laptop C
Destination MAC: Router's Network 1 interface
```

On Network 2:

```text
Source MAC:      Router's Network 2 interface
Destination MAC: Laptop X
```

The router removes the incoming Layer 2 framing and forwards the IP packet inside a new frame appropriate for the outgoing link.

### Important correction: MAC addresses don't change at every switch hop

Your lecture's phrase "MAC addresses change at every single hop" is a useful simplification, but technically it needs refinement.

**MAC addresses normally change at each routed Layer 2 link transition, not at every switch along a local network.**

For example:

```text
Laptop A → Switch 1 → Switch 2 → Router
```

On a shared Layer 2 network, switches forward the frame without replacing its source and destination MAC addresses.

When the router forwards the packet onto a different Layer 2 network, it creates a new frame with the appropriate MAC addresses for that link.

## Comparison table

| Property | IP addresses | MAC addresses |
|---|---|---|
| Main purpose | Logical addressing and routing | Local link-layer delivery |
| Used by | Layer 3 forwarding | Layer 2 forwarding |
| What happens at an ordinary router? | Normally preserved | Frame addresses are replaced for the outgoing link |
| Can they change? | Yes, for example through NAT | Yes, depending on the interface and link |
| Scope | Can support communication across multiple networks | Used for delivery on the current link |
| Example | `192.168.1.10` | `AA:BB:CC:11:22:33` |

---

# 7. Practical Linux Lab — Investigate Your Own Network

Let's use your Zorin OS terminal to connect this lecture with real network information.

These commands are for inspection and should not require changing your network configuration.

## Lab 1: Find your IP address

```bash
ip -4 addr show
```

Look for an `inet` entry under your active interface.

For example:

```text
inet 192.168.1.10/24
```

This shows an IPv4 address and its prefix.

Your actual address may differ.

## Lab 2: Find your default gateway

```bash
ip route
```

Look for a line beginning with:

```text
default via
```

For example:

```text
default via 192.168.1.1 dev wlp2s0
```

Here:
- `default` identifies the default route.
- `via 192.168.1.1` identifies the next-hop gateway.
- `dev wlp2s0` identifies the interface used by the route.

## Lab 3: Check how Linux would route to a destination

Run:

```bash
ip route get 8.8.8.8
```

This asks Linux to show the route it would select for that destination.

The output may show:
- The selected next hop.
- The outgoing interface.
- The source IP address Linux would use.

The exact output depends on your network.

## Lab 4: Inspect local IP-to-MAC mappings

```bash
ip neigh show
```

You may see an entry similar to:

```text
192.168.1.1 dev wlp2s0 lladdr AA:BB:CC:DD:EE:FF REACHABLE
```

This is an illustrative example.

It shows a neighbor IP address, the interface, the associated link-layer address, and a neighbor state.

## Lab 5: Check whether your laptop can reach a public IP

```bash
ping -c 4 8.8.8.8
```

This sends four ICMP echo requests.

If replies arrive, ICMP communication with the destination is working.

If there are no replies, don't immediately conclude that routing is broken. ICMP might be blocked or rate-limited, or there may be another issue.

## Lab 6: Check an HTTP connection

```bash
curl -I https://example.com
```

If successful, this displays HTTP response headers.

It tests more than routing alone: name resolution, transport connectivity, TLS, and HTTP may all be involved.

### What to record

Run the commands and note:

| Question | Command |
|---|---|
| What is my IPv4 address? | `ip -4 addr show` |
| What is my default gateway? | `ip route` |
| Which route would be used for a public IP? | `ip route get 8.8.8.8` |
| Which neighbor mappings are cached? | `ip neigh show` |
| Can I receive ICMP replies? | `ping -c 4 8.8.8.8` |
| Can I get an HTTP response? | `curl -I https://example.com` |

These observations help you build a mental model of how your laptop communicates with other networks.

---

# 8. Common Misconceptions

### Misconception 1: Every packet must go through a router

**Correction:** Devices on the same directly connected subnet can usually communicate through Layer 2 without routing through a router.

### Misconception 2: A switch uses IP addresses to forward ordinary Ethernet frames

**Correction:** A standard Layer 2 switch primarily uses destination MAC addresses for forwarding.

### Misconception 3: A laptop ARPs for the remote server's MAC address

**Correction:** For a remote destination, the laptop normally resolves the MAC address of its next hop, usually the default gateway.

### Misconception 4: MAC addresses change whenever a packet passes through a switch

**Correction:** Switches normally forward frames without changing their source and destination MAC addresses. Routers create new frames when forwarding packets across Layer 2 networks.

### Misconception 5: IP addresses can never change during packet travel

**Correction:** IP addresses normally remain unchanged across ordinary routing hops, but NAT and other mechanisms can modify them.

### Misconception 6: An EC2 instance with a public IP is automatically reachable

**Correction:** Routing, security groups, network ACLs, host firewalls, service configuration, and other conditions can affect reachability.

### Misconception 7: NAT and routing are the same thing

**Correction:** Routing determines where a packet should be forwarded. NAT modifies address information, often to enable communication between networks using different addressing arrangements. They can operate together, but they perform different functions.

---

# 9. Interview Questions and Answers

### Q1. What is routing?

Routing is the process of selecting a path or next hop for forwarding IP packets towards their destination.

### Q2. What is the main difference between a switch and a router?

A standard Layer 2 switch forwards frames using MAC addresses within a Layer 2 network. A router forwards IP packets between networks using routing information.

### Q3. What happens when two devices are on the same subnet?

The sender normally determines that the destination is directly reachable, resolves the destination's MAC address if necessary, and sends a frame across the local network.

### Q4. What happens when the destination is on a different subnet?

The sender selects an appropriate route, often the default route. It sends the frame to the next-hop router, whose MAC address is resolved if necessary. The router then forwards the IP packet towards the destination network.

### Q5. Why does a router need a MAC address?

When sending an IP packet over an Ethernet link, the router needs a Layer 2 frame with appropriate source and destination MAC addresses for that link.

### Q6. Do MAC addresses change when a packet crosses a router?

The incoming frame is replaced with a new frame for the outgoing link, using the appropriate MAC addresses. This happens at routed Layer 2 transitions, not at every ordinary Layer 2 switch.

### Q7. Do IP addresses change when a packet crosses a router?

Normally, the source and destination IP addresses remain the same across ordinary routing hops. NAT or another address-translation mechanism can modify them.

### Q8. What is NAT?

Network Address Translation modifies IP address information, and in common configurations may also modify transport-layer port information. Home routers often use source NAT so multiple private-addressed devices can share a public IPv4 address for outbound internet connections.

### Q9. What is a hop?

A hop is one step in the packet's journey through a network, commonly referring to forwarding by a router to the next network segment or router.

### Q10. Why might an EC2 instance be unreachable despite having a public IP?

Possible causes include an incorrect route, a missing internet gateway route, security-group restrictions, network ACL rules, host firewall configuration, an inactive service, or an incorrect connection target.

---

# 10. Quick Revision Cheat Sheet

| Concept | Remember |
|---|---|
| Routing | Selecting a path or next hop for an IP packet |
| Hop | A step along the network path |
| Layer 2 switch | Forwards frames using MAC addresses |
| Layer 3 router | Forwards packets using IP routing information |
| Same subnet | Usually direct local delivery |
| Different subnet | Send to an appropriate next hop, often the default gateway |
| ARP | Resolves a local IPv4 next-hop address to a MAC address |
| NAT | Modifies address information and, in common configurations, may modify ports |
| IP addresses | Normally preserved across ordinary routing hops |
| MAC addresses | Replaced in newly created frames when forwarding across routed links |
| Default route | Used when no more-specific applicable route is selected |
| EC2 reachability | Requires correct networking and security configuration |

## The entire lecture in one diagram

```text
                     SOURCE LAPTOP
                           |
                           v
                  Check routing information
                           |
               +-----------+-----------+
               |                       |
          Same subnet              Remote subnet
               |                       |
               v                       v
        Resolve target MAC       Resolve next-hop MAC
               |                       |
               v                       v
         Local switch                 Router
               |                       |
               v                       v
        Destination device      Route to next network
                                       |
                                       v
                               More routed hops
                                       |
                                       v
                              Destination network
                                       |
                                       v
                              Destination device
```

---

## Lecture 12 Complete

You've now connected local switching, IP routing, ARP, default gateways, NAT, and cloud connectivity into one model.

**The most important distinction to remember is this:**

- **Switches forward frames locally using MAC addresses.**
- **Routers forward IP packets between networks using routing information.**
- **ARP resolves local IPv4 next-hop addresses to MAC addresses.**
- **NAT may modify IP addresses, and sometimes ports.**
- **At each routed link transition, the router creates a new Layer 2 frame.**

These concepts will become particularly useful when troubleshooting Linux networking, Docker networks, AWS VPCs, and Kubernetes communication.
