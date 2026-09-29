
# Lesson 08: Routing and Routing Tables

## 1. What Is Routing?

Routing is the process of selecting a path for network packets to travel from a source network to a destination network.

When a computer sends data to another device, it must determine where the packet should go.

If the destination is on the same local network, the computer can communicate directly.

If the destination is on another network, the packet is usually sent to a router or gateway.

### Real-World Analogy

Imagine sending a parcel:

- Your home is the source.
- The destination address is the target.
- The delivery route is the path.
- A local delivery center is similar to a gateway.
- The delivery system selects the appropriate route.

Routing works in a similar way, but it handles network packets instead of physical parcels.

---

## 2. What Is a Router?

A router is a networking device that connects different IP networks and forwards packets between them.

For example:

- Your laptop belongs to a Wi-Fi network.
- A web server belongs to a different network.
- Your router forwards packets between these networks.

A router examines the destination IP address and uses its routing table to decide where to forward the packet.

### Router Responsibilities

1. Receive packets.
2. Examine destination IP addresses.
3. Look up the destination in the routing table.
4. Select the appropriate next hop or outgoing interface.
5. Forward packets toward their destination.

---

## 3. What Is a Routing Table?

A routing table is a collection of rules that tells a computer or router where to send packets destined for different IP networks.

Linux maintains a routing table to determine how outgoing traffic should travel.

To display the routing table:

```bash
ip route
```

Alternative command:

```bash
ip -4 route
```

The second command displays IPv4 routes.

### Example Routing Table

```text
default via 10.189.112.89 dev wlp2s0 proto dhcp src 10.189.112.123 metric 600

10.189.112.0/24 dev wlp2s0 proto kernel scope link src 10.189.112.123 metric 600

172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
```

Let's understand each entry.

---

## 4. Understanding the Default Route

Example:

```text
default via 10.189.112.89 dev wlp2s0
```

This means:

- `default`: Use this route when no more specific route matches.
- `via 10.189.112.89`: Forward the packet to this gateway.
- `dev wlp2s0`: Send the packet through this network interface.

The default route is used for destinations that do not match a more specific route in the routing table.

### What Is 0.0.0.0/0?

The default route can also be represented as:

```text
0.0.0.0/0
```

It matches all IPv4 destinations.

However, more specific routes take priority over the default route.

### Example

Suppose your laptop wants to reach:

```text
8.8.8.8
```

If no more specific route exists, the packet is forwarded to your default gateway.

Your laptop does not need to know the complete path to the destination. It sends the packet to the next hop, and routers along the way continue forwarding it.

---

## 5. What Is a Gateway?

A gateway is a device or network node that provides a path from one network to another.

In a typical home or office network, the router acts as the default gateway.

Example:

```text
Laptop
IP: 10.189.112.123
       |
       | Wi-Fi
       |
Router / Default Gateway
IP: 10.189.112.89
       |
       |
Internet
```

When your laptop communicates with a remote network, it sends packets to the gateway.

### Important

A gateway is not necessarily the final destination.

It is often just the next hop on the path toward the destination.

---

## 6. Understanding a Directly Connected Route

Example:

```text
10.189.112.0/24 dev wlp2s0 proto kernel scope link src 10.189.112.123
```

This entry tells Linux that the network `10.189.112.0/24` is directly connected through the Wi-Fi interface.

Let's break it down:

| Field | Meaning |
|---|---|
| `10.189.112.0/24` | Destination network |
| `dev wlp2s0` | Outgoing interface |
| `proto kernel` | Route installed by the kernel |
| `scope link` | Destination is directly reachable on the link |
| `src 10.189.112.123` | Preferred source IP address |

### Example

Your laptop:

```text
10.189.112.123/24
```

Another device:

```text
10.189.112.50/24
```

Both addresses belong to:

```text
10.189.112.0/24
```

Therefore, your laptop can communicate with that device directly over the local network, without sending the packet to the default gateway.

---

## 7. Docker Networking and Routing

Your routing table also contains:

```text
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
```

This route is associated with Docker's default bridge network.

### Understanding the Entry

- `172.17.0.0/16`: Docker network.
- `docker0`: Docker bridge interface.
- `172.17.0.1`: IP address assigned to the bridge.
- `linkdown`: The interface is currently reported as down.

Docker uses bridge networking to connect containers to a virtual network.

### Simplified Diagram

```text
Host Machine
     |
     | docker0 bridge
     |
     +------ Container 1
     |
     +------ Container 2
     |
     +------ Container 3
```

The Docker bridge provides connectivity between containers and the host, subject to the network configuration and firewall rules.

---

## 8. How Linux Selects a Route

Linux does not simply select the first route in the routing table.

It uses a process called **Longest Prefix Match**.

The system selects the matching route with the most specific network prefix.

### Example

Suppose the routing table contains:

```text
10.0.0.0/8
10.10.0.0/16
10.10.20.0/24
default
```

Now consider the destination:

```text
10.10.20.50
```

This destination matches all four routes.

However, Linux selects:

```text
10.10.20.0/24
```

Because `/24` is more specific than `/16`, `/8`, or `/0`.

### Prefix Comparison

| Route | Specificity |
|---|---|
| `0.0.0.0/0` | Least specific |
| `10.0.0.0/8` | More specific |
| `10.10.0.0/16` | More specific |
| `10.10.20.0/24` | Most specific |

### Why Is This Important?

Longest Prefix Match is important in:

- Cloud networking
- AWS VPC route tables
- Kubernetes networking
- Docker networking
- Linux troubleshooting
- Enterprise networks

It allows networks to define broad routes and then override them with more specific routes.

---

## 9. What Is a Metric?

A metric is a value used to compare routes when multiple routes are otherwise comparable.

Example:

```text
default via 10.189.112.89 dev wlp2s0 metric 600
```

Here:

```text
metric 600
```

is the route metric.

Generally, a lower metric is preferred when the relevant routes have the same destination prefix and are otherwise eligible alternatives.

### Example

Suppose two default routes exist:

```text
default via 192.168.1.1 dev wlan0 metric 100
default via 192.168.1.254 dev eth0 metric 200
```

The first route has a lower metric and is generally preferred.

**Remember:** Route selection is based first on the most specific matching prefix. Metrics help compare routes of equal prefix specificity; they do not normally make a less-specific route override a more-specific one.

---

## 10. Routing vs Switching

Routing and switching are related but different networking functions.

| Routing | Switching |
|---|---|
| Connects different IP networks | Connects devices within a local network |
| Uses IP addresses | Traditional Ethernet switching uses MAC addresses |
| Operates primarily at Layer 3 | Traditional switching operates at Layer 2 |
| Uses routing tables | Uses MAC address tables |
| Example: Sending traffic to the internet | Example: Forwarding frames between devices on a LAN |

### Simple Example

When your laptop sends data to another device on the same LAN, Ethernet switching is involved.

When your laptop sends data to a remote internet server, routing is involved.

Modern network devices may combine both functions.

---

## 11. Linux Commands for Routing

### 11.1 Display the Routing Table

```bash
ip route
```

Displays the IPv4 routing table.

### 11.2 Display IPv4 Routes

```bash
ip -4 route
```

### 11.3 Display IPv6 Routes

```bash
ip -6 route
```

### 11.4 Check the Route to a Specific IP

```bash
ip route get 8.8.8.8
```

This command asks the kernel which route it would use to reach the specified destination.

Example output:

```text
8.8.8.8 via 10.189.112.89 dev wlp2s0 src 10.189.112.123 uid 1000
```

Interpretation:

- Destination: `8.8.8.8`
- Gateway: `10.189.112.89`
- Interface: `wlp2s0`
- Source IP: `10.189.112.123`

**Important:** `ip route get` shows the selected route. It does not prove that the destination is reachable.

### 11.5 Check the Route to Your Gateway

```bash
ip route get 10.189.112.89
```

### 11.6 Check the Route to a Local Device

```bash
ip route get 10.189.112.50
```

If the address belongs to your directly connected subnet, the output should normally show the local interface without a `via` gateway.

### 11.7 Display Neighbor Information

```bash
ip neigh
```

Displays the Linux neighbor table, which contains information used to map local IP addresses to link-layer addresses.

For IPv4 Ethernet networks, this is commonly associated with ARP.

---

## 12. What Happens When There Is No Route?

Suppose Linux tries to reach a destination but has no matching route.

It may return an error such as:

```text
Network is unreachable
```

This indicates that the system cannot find a usable route for the destination.

### Common Causes

1. No default gateway is configured.
2. The required interface is down.
3. The routing table is missing a route.
4. The network configuration is incorrect.
5. IPv6 routing is unavailable for an IPv6 destination.

### Troubleshooting Commands

```bash
ip addr
ip route
ip link
ip route get <destination-IP>
```

These commands help inspect interfaces, addresses, routes, and the kernel's route decision.

---

## 13. Practical Lab: Inspect Your Linux Routing Table

### Step 1: Display Routes

```bash
ip route
```

Identify:

- Default route
- Local network route
- Docker route

### Step 2: Check an Internet Destination

```bash
ip route get 8.8.8.8
```

Observe the selected gateway and interface.

### Step 3: Check a Local Destination

```bash
ip route get 10.189.112.50
```

Compare the output with the previous command.

### Step 4: Check Another Remote Destination

```bash
ip route get 1.1.1.1
```

Observe whether Linux uses the same default gateway.

### Step 5: Check the Docker Network

```bash
ip route get 172.17.0.2
```

Inspect which route Linux selects for this destination.

The route may be associated with `docker0`, depending on the current routing configuration.

### Step 6: Inspect Neighbor Information

```bash
ip neigh
```

Observe the local IP-to-MAC mappings learned by the system.

---

## 14. Routing in Cloud and DevOps

Routing is a fundamental concept in cloud infrastructure.

### AWS VPC

In AWS, route tables determine where network traffic from a subnet is directed.

A route may direct traffic toward:

- A local VPC network
- An Internet Gateway
- A NAT Gateway
- A peering connection
- A Transit Gateway

The actual destination depends on the configured route and the available network resources.

### Docker

Docker uses virtual networks and bridge interfaces to connect containers.

Understanding Linux routing helps troubleshoot container connectivity.

### Kubernetes

Kubernetes networking depends on communication between pods, nodes, and services.

Routing knowledge helps diagnose connectivity problems across these components.

### CI/CD and Production Infrastructure

DevOps engineers may need routing knowledge when:

- Deploying services on cloud instances.
- Troubleshooting inaccessible servers.
- Debugging container networking.
- Investigating connectivity between subnets.
- Configuring private and public networks.
- Diagnosing network-related deployment failures.

---

## 15. Interview Questions and Answers

### Q1. What is routing?

Routing is the process of selecting a path for packets to travel from a source network to a destination network.

### Q2. What is a routing table?

A routing table is a collection of routes that tells a system where to forward packets for different destinations.

### Q3. What is a default route?

A default route is used when no more specific route matches the destination.

In IPv4, it is represented as `0.0.0.0/0`.

### Q4. What is a gateway?

A gateway is a network node that provides a path to another network. A home router commonly acts as the default gateway.

### Q5. What is the difference between a gateway and a destination?

The destination is the IP address the packet is ultimately trying to reach. The gateway is a next hop that forwards the packet toward that destination.

### Q6. What is Longest Prefix Match?

It is the route-selection rule in which the most specific matching network prefix is preferred.

### Q7. What is a route metric?

A metric is a value used to compare otherwise comparable routes. A lower metric is generally preferred.

### Q8. What does `ip route get` do?

It displays the route the Linux kernel would select for a specified destination.

### Q9. What is the difference between routing and switching?

Routing forwards packets between IP networks, while traditional Layer 2 switching forwards Ethernet frames within a local network.

### Q10. What happens if there is no matching route?

The system may return a `Network is unreachable` error because it cannot find a usable path to the destination.

### Q11. Why is routing important in DevOps?

It helps engineers troubleshoot connectivity between servers, containers, cloud networks, and infrastructure components.

### Q12. What is the purpose of the Docker bridge interface?

It provides a virtual Layer 2 network for connecting containers and the host through Docker's bridge networking.

---

## 16. Key Takeaways

- Routing determines where network packets should go.
- Routers connect different IP networks.
- Routing tables contain rules for forwarding packets.
- The default route handles destinations without a more specific match.
- A gateway is commonly the next hop for remote networks.
- Directly connected networks can be reached through a local interface.
- Linux uses Longest Prefix Match to select the most specific matching route.
- Metrics help compare otherwise comparable routes.
- `ip route` displays the routing table.
- `ip route get` reveals the kernel's route decision.
- Routing knowledge is essential for Linux, AWS, Docker, Kubernetes, and production troubleshooting.

**Lesson 08 completed: Routing and Routing Tables.**
