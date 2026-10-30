# Networking for DevOps — Lecture 06
## Default Gateway and Router Roles

**Roadmap position:** Networking — Lecture 06  
**Previous lecture:** Subnet Masks and Local vs. External Traffic  
**Today's goal:** Understand how your computer sends packets to other networks, what a default gateway does, and how routers forward packets toward their destinations.

These concepts are essential for Linux networking, AWS VPCs, cloud servers, and troubleshooting connectivity.

---

# 1. Why Do We Need a Router?

Imagine your laptop is connected to your home Wi-Fi.

Your network contains:

- Your laptop
- Your mobile phone
- Your printer
- Your Wi-Fi router

Suppose your laptop wants to communicate with your printer.

If both devices are on the same subnet, your laptop can communicate with the printer directly over the local network.

But what happens when you want to access a website hosted on a server somewhere else in the world?

Your laptop cannot communicate directly with every network on the internet. It needs a device that can forward packets toward other networks.

That device is a **router**.

A router connects networks and forwards IP packets between them based on its routing information.

### Example

```text
                 Internet
                    |
                    |
              +-------------+
              |   Router    |
              +-------------+
                    |
                 Home LAN
                    |
          +---------+---------+
          |                   |
       Laptop               Mobile
    192.168.1.10         192.168.1.20
```

The router connects the home network to another network, such as an internet service provider's network.

It can forward traffic between networks when its routing configuration and security rules allow it.

---

# 2. What Is a Default Gateway?

A **default gateway** is the next-hop router a device uses for destinations when no more-specific matching route takes precedence over the default route.

Think of your local network as a building.

- Your laptop is a room inside the building.
- Your local network is the building.
- The default gateway is an exit that leads toward other networks.

When your laptop wants to reach a destination outside its local subnet, it checks its routing table.

If no more-specific route matches and a default route is configured, the packet can be sent to the default gateway.

### Example

Suppose your laptop has this configuration:

```text
IP address:      192.168.1.10
Subnet mask:     255.255.255.0
Default gateway: 192.168.1.1
```

The default gateway is:

```text
192.168.1.1
```

Your laptop might use this address to reach destinations outside its local subnet.

**Important:** The default gateway is usually a router interface on the local network. It is not necessarily the router's only IP address.

---

# 3. How Does a Laptop Know Where to Send a Packet?

Your laptop does not simply send every packet to the router.

Instead, it uses its **routing table** to decide where the packet should go.

Consider this example:

```text
Laptop IP:       192.168.1.10/24
Default gateway: 192.168.1.1
```

The laptop wants to reach two destinations.

### Destination A: `192.168.1.20`

The destination belongs to the laptop's local subnet:

```text
Laptop network:      192.168.1.0/24
Destination network: 192.168.1.0/24
```

The laptop can send traffic directly over the local network.

It does not need to send the packet to the default gateway as its next hop.

### Destination B: `8.8.8.8`

The destination is outside `192.168.1.0/24`.

If the routing table contains a default route through `192.168.1.1`, the laptop can forward the packet toward that gateway.

```text
Local destination:
Laptop ──────────────────> Destination

Remote destination:
Laptop ─────> Gateway ────> Other networks ────> Destination
```

The router then consults its own routing table to determine the next step.

The packet may pass through several routers before reaching its destination.

---

# 4. What Happens When You Open a Website?

Let's follow a simplified example.

Suppose you open a website hosted at a public IP address.

Your laptop has:

```text
Laptop IP:       192.168.1.10
Default gateway: 192.168.1.1
```

The website's server has a different IP address.

## Step 1: Your browser initiates a connection

Your browser needs to communicate with the website's server.

Before making the connection, your system may need to resolve the website's domain name using DNS.

For example:

```text
example.com → Destination IP address
```

The actual address depends on DNS responses and the site's configuration.

## Step 2: Your computer checks the destination route

Your laptop examines its routing table.

It determines that the destination is not on the local subnet and selects an appropriate route, such as the default route.

## Step 3: Your laptop identifies the gateway's MAC address

On a typical IPv4 Ethernet or Wi-Fi network, your laptop needs the MAC address of the next hop.

If it does not already have the mapping cached, it can use ARP to discover the MAC address associated with the gateway's local IP address.

For example:

```text
Gateway IP: 192.168.1.1
Gateway MAC:  AA:BB:CC:DD:EE:FF
```

This MAC address is illustrative.

## Step 4: Your laptop sends the frame to the gateway

The packet contains the destination IP address of the website's server.

However, the local Ethernet or Wi-Fi frame is addressed to the gateway's MAC address.

```text
IP packet:
Source IP:      192.168.1.10
Destination IP: Website server IP

Local frame:
Source MAC:      Laptop MAC
Destination MAC: Gateway MAC
```

This distinction is crucial.

**The IP packet is addressed to the final destination, while the local frame is addressed to the next hop.**

## Step 5: The router receives the packet

The router removes the incoming link-layer frame and examines the IP packet.

It checks the destination IP and consults its routing table.

If a suitable route exists and forwarding is permitted, the router forwards the packet toward the next hop.

## Step 6: The packet travels through other networks

The packet may travel through multiple routers before reaching the website's server.

The router on each hop makes a forwarding decision based on its own routing information.

## Step 7: The response returns

The server's response travels back through the network toward your laptop.

The return path may differ from the outgoing path.

---

# 5. Does the Default Gateway Change the Destination IP?

Usually, no.

Suppose your laptop is communicating with a remote server.

```text
Laptop IP:       192.168.1.10
Gateway IP:      192.168.1.1
Remote server:   203.0.113.50
```

The server address above is an example from a range reserved for documentation.

Your laptop sends a packet toward the gateway.

Before network address translation (NAT), the packet's IP header may look like this:

```text
Source IP:      192.168.1.10
Destination IP: 203.0.113.50
```

The gateway forwards the packet toward the destination.

In ordinary routing, the source and destination IP addresses remain the same as the packet passes through routers, although the TTL is reduced and the IP header checksum is updated in IPv4.

However, **NAT can modify IP addresses**. For example, a home router may translate a private source address into a public source address when forwarding traffic to the internet.

We will study NAT separately in your roadmap.

---

# 6. Why Do MAC Addresses Change at Each Router Hop?

This connects directly to your previous networking lectures.

Suppose a packet travels through three networks:

```text
Laptop
   |
   v
Router A
   |
   v
Router B
   |
   v
Destination Server
```

Each router forwards the IP packet using a new link-layer frame appropriate for the next network.

For example:

| Network segment | Frame source MAC | Frame destination MAC |
|---|---|---|
| Laptop → Router A | Laptop MAC | Router A's LAN MAC |
| Router A → Router B | Router A's outgoing MAC | Router B's next-hop MAC |
| Router B → Server | Router B's outgoing MAC | Server MAC, if directly connected |

The exact addresses depend on the topology and link-layer technology.

The key idea is:

- **IP addresses** identify the source and destination at the network layer.
- **MAC addresses** identify link-layer endpoints on a local link.

Routers remove the incoming frame and construct a new frame for the outgoing link.

That is why the MAC addresses usually change from one routed link to the next.

---

# 7. Practical Linux Lab

Now let's inspect the actual routing configuration on your Zorin OS system.

## Step 1: Display your IP address

Run:

```bash
ip addr
```

Look for your Wi-Fi interface, previously identified as:

```text
wlp2s0
```

You might see an entry similar to:

```text
inet 192.168.1.10/24
```

Your actual IP address and prefix may differ.

## Step 2: Display your routing table

Run:

```bash
ip route
```

Example output:

```text
default via 192.168.1.1 dev wlp2s0
192.168.1.0/24 dev wlp2s0 proto kernel scope link
```

Let's understand the first line:

```text
default via 192.168.1.1 dev wlp2s0
```

| Component | Meaning |
|---|---|
| `default` | Default route |
| `via 192.168.1.1` | Next-hop gateway |
| `dev wlp2s0` | Interface used to reach the gateway |

The second line describes the directly connected subnet.

```text
192.168.1.0/24 dev wlp2s0
```

It indicates that the subnet is directly reachable through that interface.

Your actual output may contain additional routes, including routes for Docker or VPN interfaces.

## Step 3: Find the route to an external destination

Run:

```bash
ip route get 8.8.8.8
```

Example output:

```text
8.8.8.8 via 192.168.1.1 dev wlp2s0 src 192.168.1.10
```

This indicates that Linux selected the route through `192.168.1.1`, using `wlp2s0` and the specified source address.

The output depends on your routing configuration.

**Remember:** `ip route get` shows the route Linux would select. It does not prove that the destination is reachable.

## Step 4: Inspect the gateway's MAC address

Run:

```bash
ip neigh
```

This displays the Linux neighbor table, which commonly contains IPv4-to-MAC mappings learned through ARP.

Example:

```text
192.168.1.1 dev wlp2s0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
```

Your output may differ, and the gateway entry might not appear until your computer has attempted to communicate with it.

---

# 8. Default Gateway vs. Router

These terms are related, but they are not identical.

| Router | Default gateway |
|---|---|
| A device or system that forwards packets between networks | The next-hop gateway used by a host's default route |
| Can have multiple interfaces and routes | Refers to the gateway selected by the host's default route |
| May route traffic between several networks | Provides a route toward destinations without a more-specific matching route |
| Example: a home Wi-Fi router | Example: `192.168.1.1` |

A router can serve as the default gateway for devices on one network while also routing traffic between other networks.

---

# 9. DevOps Connection: AWS and Cloud Networking

Suppose you create a virtual machine in AWS.

The VM has a private IPv4 address and belongs to a subnet in a VPC.

Its traffic is governed by several components:

- The subnet's route table.
- The VPC's networking configuration.
- Security groups and network ACLs.
- The available route to the intended destination.
- Any additional firewall or network configuration.

For example:

```text
EC2 Instance
10.0.1.10
     |
     v
VPC Subnet
10.0.1.0/24
     |
     v
Route Table
     |
     v
Configured Next Hop
```

The next hop depends on the route. It might be a local VPC route, an internet gateway, a NAT gateway, a transit gateway, or another supported target.

A default route does not automatically guarantee internet connectivity. The necessary routing, addressing, and security configuration must also be in place.

This is why understanding default gateways and routing is important before you go deeper into AWS networking.

---

# 10. Common Mistakes

### Mistake 1: Sending all traffic to the gateway

A computer can send traffic directly to an on-link destination. It does not need to send every packet to the default gateway.

### Mistake 2: Assuming a default gateway guarantees internet access

A gateway alone is insufficient. The route beyond it, connectivity, firewall rules, and other network configuration must permit communication.

### Mistake 3: Confusing the gateway's IP with the remote server's IP

The gateway is the next hop, not necessarily the final destination.

### Mistake 4: Assuming routers never change packet headers

Routers normally reduce the IPv4 TTL and update the IPv4 header checksum. NAT can also modify IP addresses and related fields.

### Mistake 5: Assuming the outgoing and return paths are identical

Routing can be asymmetric. The return packet may travel through a different set of routers.

---

# 11. Interview Questions and Answers

**Q1. What is a default gateway?**

A default gateway is the next-hop router used by a host's default route when no more-specific matching route takes precedence.

**Q2. Why do we need a router?**

A router forwards IP packets between networks using its routing table.

**Q3. How does a laptop determine where to send a packet?**

It consults its routing table and selects the most specific matching route, subject to routing policy and configuration.

**Q4. Does a laptop send local traffic through its default gateway?**

Normally, no. If the destination is on-link, the laptop sends the traffic directly over the local network.

**Q5. What happens to the destination IP when a packet passes through a router?**

Normally, it remains unchanged during routing, unless a function such as NAT modifies it.

**Q6. Why do MAC addresses change across router hops?**

Each router constructs a new link-layer frame for the next network segment.

**Q7. How can you find the default gateway on Linux?**

Run:

```bash
ip route
```

Look for the route beginning with `default`.

**Q8. Does a default route guarantee that the internet will work?**

No. The route, next-hop connectivity, network configuration, and security rules must all permit communication.

---

# 12. Quick Revision

Remember these key points:

1. A **router** forwards packets between networks.
2. A **default gateway** is the next hop used by a host's default route.
3. A computer consults its routing table to decide where to send traffic.
4. Local destinations can be reached directly over the local network.
5. Remote destinations are reached through a suitable route, often via a gateway.
6. IP addresses normally remain unchanged during routing, while link-layer addresses change at each routed hop.
7. On Linux, use `ip route` to inspect routing information.

## Practice Exercises

Try these on your Zorin OS system:

**Exercise 1**

```bash
ip route
```

Identify the default route and gateway, if one is configured.

**Exercise 2**

```bash
ip route get 8.8.8.8
```

Identify the selected route, outgoing interface, and source IP.

**Exercise 3**

Explain in your own words why a packet sent to a remote server has the server's IP address as its destination but the gateway's MAC address as its local Ethernet destination.

**Exercise 4**

A laptop has the IP address `192.168.1.10/24` and gateway `192.168.1.1`.

Does it normally need the gateway to communicate with `192.168.1.20`? What about `192.168.2.20`?

---

## Next: Lecture 07

Your supplied revision guide moves from Lecture 06 to Lecture 09 for the IP-versus-MAC topic. To avoid inventing lesson numbers or skipping material, we'll keep the next lesson aligned with your actual lecture sequence when you provide the corresponding topic.