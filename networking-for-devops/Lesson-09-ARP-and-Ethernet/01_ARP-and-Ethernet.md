# Networking Lesson 09 --- ARP and Ethernet

## 1. What is ARP?

**ARP (Address Resolution Protocol)** is used in IPv4 networks to find
the **MAC address** associated with an IP address on the local network.

``` text
IPv4 Address
     ↓
   ARP
     ↓
MAC Address
```

## 2. Why Do We Need ARP?

Suppose your computer wants to communicate with:

``` text
10.189.112.89
```

The computer knows the destination IP, but local Ethernet/Wi-Fi delivery
requires a MAC address.

``` text
Destination IP
      ↓
ARP Request
      ↓
ARP Reply
      ↓
Destination MAC
```

## 3. Local vs Remote Destination

### Local destination

If the destination is on the same subnet, ARP resolves the destination
device's MAC address.

``` text
10.189.112.123
      |
      | local network
      |
10.189.112.50
```

### Remote destination

For a remote destination, ARP resolves the MAC address of the **next
hop**, normally the default gateway.

``` text
Destination: 8.8.8.8
Next hop:    10.189.112.89

10.189.112.89
      ↓
ARP
      ↓
Gateway MAC
```

> ARP resolves the MAC address of the next device on the local link.

## 4. ARP Request

An ARP request asks:

> Who has this IP address?

Example:

``` text
Who has 10.189.112.89?
Tell 10.189.112.123
```

The request is normally sent as a broadcast.

Broadcast MAC:

``` text
ff:ff:ff:ff:ff:ff
```

## 5. ARP Reply

The device that owns the requested IP responds with its MAC address.

``` text
ARP Request:
Who has 10.189.112.89?
        ↓
Broadcast
        ↓
Gateway receives it
        ↓
ARP Reply:
10.189.112.89 is at AA:BB:CC:DD:EE:FF
```

The sender can now send the Ethernet/Wi-Fi frame to that MAC.

## 6. ARP Process

``` text
Computer A
10.189.112.123
      |
      | Need MAC for 10.189.112.89
      |
      v
ARP Request
Broadcast
ff:ff:ff:ff:ff:ff
      |
      v
Gateway
10.189.112.89
      |
      | ARP Reply
      |
      v
MAC Address
      |
      v
Neighbor Table
      |
      v
Ethernet/Wi-Fi Frame
```

## 7. Linux Neighbor Table

Linux keeps information about nearby devices in a **neighbor table**.

``` bash
ip neigh
```

Example:

``` text
10.189.112.89 dev wlp2s0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
```

This means:

-   IP: `10.189.112.89`
-   Interface: `wlp2s0`
-   MAC: `aa:bb:cc:dd:ee:ff`
-   State: `REACHABLE`

## 8. `ip neigh`

Useful commands:

``` bash
ip neigh
```

``` bash
ip neigh show 10.189.112.89
```

``` bash
ip neigh show dev wlp2s0
```

## 9. Neighbor States

  State          Meaning
  -------------- --------------------------------------------------
  `REACHABLE`    Neighbor is known and recently reachable
  `STALE`        Entry exists but has not been recently confirmed
  `DELAY`        Waiting before probing
  `PROBE`        Linux is actively checking the neighbor
  `INCOMPLETE`   Address resolution is still in progress
  `FAILED`       Neighbor resolution failed

## 10. ARP Cache / Neighbor Cache

Once a MAC address has been learned, Linux can temporarily keep it:

``` text
IP Address              MAC Address
-----------------------------------------
10.189.112.89      →    aa:bb:cc:dd:ee:ff
```

This avoids performing ARP for every packet.

## 11. What is Ethernet?

**Ethernet** is a common Layer 2 networking technology.

It uses MAC addresses for local frame delivery.

``` text
IP Packet
   ↓
Ethernet Frame
   ↓
Network Interface
   ↓
Physical Network
```

## 12. Ethernet Frame

Simplified Ethernet frame:

``` text
+-------------------+
| Destination MAC   |
+-------------------+
| Source MAC        |
+-------------------+
| EtherType         |
+-------------------+
| Payload           |
+-------------------+
| FCS               |
+-------------------+
```

## 13. Destination MAC

The destination MAC identifies the device that should receive the frame
on the local link.

For an ARP request, it is normally:

``` text
ff:ff:ff:ff:ff:ff
```

## 14. Source MAC

The source MAC identifies the interface sending the frame.

``` text
Source MAC
      ↓
Destination MAC
```

## 15. EtherType

EtherType identifies the protocol carried inside the Ethernet frame.

Examples:

``` text
IPv4
IPv6
ARP
```

## 16. Payload

The payload contains the data carried by the Ethernet frame.

For example:

``` text
Ethernet Frame
      |
      +-- Header
      |
      +-- Payload
             |
             +-- IP packet
                    |
                    +-- TCP/UDP
                           |
                           +-- Application data
```

## 17. FCS

FCS means **Frame Check Sequence**.

It is used to detect errors in the Ethernet frame.

## 18. MAC Address

A MAC address is a Layer 2 interface address.

Example:

``` text
aa:bb:cc:dd:ee:ff
```

## 19. IP Address vs MAC Address

  IP Address                  MAC Address
  --------------------------- ------------------------------
  Layer 3 concept             Layer 2 concept
  Logical addressing          Local frame delivery
  Example: `10.189.112.123`   Example: `aa:bb:cc:dd:ee:ff`
  Used by routers             Used by switches/NICs

Simple mental model:

``` text
IP  = Where?
MAC = Which local interface?
```

## 20. ARP + Routing

Suppose:

``` text
Your PC: 10.189.112.123/24
Gateway: 10.189.112.89
Destination: 8.8.8.8
```

The routing table determines that `8.8.8.8` is remote, so the next hop
is:

``` text
10.189.112.89
```

ARP then resolves:

``` text
10.189.112.89
       ↓
Gateway MAC
```

Complete flow:

``` text
8.8.8.8
   |
   v
Routing table
   |
   v
Next hop = 10.189.112.89
   |
   v
ARP
   |
   v
Gateway MAC
   |
   v
Ethernet/Wi-Fi frame
   |
   v
Gateway
```

## 21. Router vs Switch

### Switch

Primarily operates at Layer 2 and forwards frames using MAC addresses.

``` text
MAC Address
    ↓
Ethernet Frame
```

### Router

Operates at Layer 3 and forwards packets using IP addresses and routing
tables.

``` text
Destination IP
    ↓
Routing Table
    ↓
Next Hop / Interface
```

Simple distinction:

``` text
Switch → MAC
Router → IP
```

## 22. ARP vs DNS

### DNS

``` text
Hostname
    ↓
IP Address
```

Example:

``` text
google.com
    ↓
142.250.x.x
```

### ARP

``` text
Local IPv4 Address
    ↓
MAC Address
```

Example:

``` text
10.189.112.89
    ↓
aa:bb:cc:dd:ee:ff
```

Remember:

``` text
DNS = Name → IP
ARP = IPv4 → MAC
```

## 23. Practical Linux Commands

Show interfaces:

``` bash
ip link
```

Show IPv4 addresses:

``` bash
ip -4 addr
```

Show routing table:

``` bash
ip route
```

Show neighbor table:

``` bash
ip neigh
```

Show neighbors on Wi-Fi:

``` bash
ip neigh show dev wlp2s0
```

Check a specific neighbor:

``` bash
ip neigh show 10.189.112.89
```

Test the gateway:

``` bash
ping -c 4 10.189.112.89
```

## 24. Practical ARP Lab

### Step 1 --- Check Wi-Fi interface

``` bash
ip link show wlp2s0
```

### Step 2 --- Check neighbor table

``` bash
ip neigh
```

### Step 3 --- Ping the gateway

``` bash
ping -c 4 10.189.112.89
```

### Step 4 --- Check neighbors again

``` bash
ip neigh
```

The gateway should have a neighbor entry if ARP resolution succeeded.

## 25. Why ARP Matters in DevOps

ARP is useful when troubleshooting:

-   Linux servers
-   Virtual machines
-   Containers
-   Local network connectivity
-   Gateway problems
-   Duplicate IP problems
-   Neighbor resolution failures
-   Cloud and infrastructure networking

A server can have a correct IP and route but still have a problem
communicating with the local next hop.

## 26. ARP Troubleshooting

If a local device cannot be reached:

``` bash
ip link
```

``` bash
ip -4 addr
```

``` bash
ip route
```

``` bash
ip neigh
```

``` bash
ping -c 4 <gateway-ip>
```

Check for states such as:

``` text
REACHABLE
STALE
INCOMPLETE
FAILED
```

`INCOMPLETE` or `FAILED` can indicate that neighbor resolution is not
succeeding.

## 27. Complete Networking Flow

Suppose we access:

``` text
google.com
```

Simplified process:

``` text
1. Application
       |
       v
2. DNS
       |
       v
3. google.com → IP address
       |
       v
4. Routing table
       |
       v
5. Determine next hop
       |
       v
6. ARP
       |
       v
7. Find next-hop MAC
       |
       v
8. Ethernet/Wi-Fi frame
       |
       v
9. Router
       |
       v
10. Internet
       |
       v
11. Destination
```

## 28. ARP Request vs ARP Reply

  ARP Request                              ARP Reply
  ---------------------------------------- ---------------------------
  Asks for a MAC address                   Provides the MAC address
  Normally broadcast                       Normally unicast
  Destination MAC is `ff:ff:ff:ff:ff:ff`   Sent back to requester
  "Who has this IP?"                       "This IP is at this MAC."

## 29. Important ARP Facts

1.  ARP is used with IPv4.
2.  ARP resolves an IPv4 address to a MAC address on the local link.
3.  ARP requests are normally broadcast.
4.  The broadcast MAC is `ff:ff:ff:ff:ff:ff`.
5.  ARP replies are normally unicast.
6.  For a remote destination, ARP resolves the MAC of the next hop,
    usually the gateway.
7.  Linux stores neighbor information in the neighbor table.
8.  `ip neigh` is the main Linux command for viewing neighbor
    information.
9.  Ethernet uses MAC addresses for local frame delivery.
10. Switches primarily use MAC addresses.
11. Routers use IP addresses and routing tables.

## 30. Key Commands Cheat Sheet

  Command                      Purpose
  ---------------------------- -------------------------------
  `ip link`                    Show network interfaces
  `ip addr`                    Show IP addresses
  `ip -4 addr`                 Show IPv4 addresses
  `ip route`                   Show routing table
  `ip neigh`                   Show neighbor/ARP information
  `ip neigh show dev wlp2s0`   Show neighbors on Wi-Fi
  `ip neigh show <IP>`         Show a specific neighbor
  `ping -c 4 <IP>`             Test connectivity

## 31. Key Differences

  Technology   Main Job
  ------------ ------------------------------------
  DNS          Name → IP
  Routing      Select path to destination
  ARP          IPv4 → MAC on local network
  Ethernet     Local Layer 2 frame delivery
  Switch       Forward frames using MAC addresses
  Router       Forward packets using IP/routing

## 32. Final Mental Model

``` text
                 DNS
                  |
           "What IP is this?"
                  |
                  v
             Domain Name
                  |
                  v
              IP Address
                  |
                  v
               ROUTING
                  |
           "How do I reach it?"
                  |
                  v
              Next Hop
                  |
                  v
                 ARP
                  |
           "What MAC is it?"
                  |
                  v
            MAC Address
                  |
                  v
        Ethernet / Wi-Fi Frame
                  |
                  v
               Router
                  |
                  v
              Internet
                  |
                  v
             Destination
```

### Most important rule

``` text
DNS      = Name → IP
Routing  = Path to IP
ARP      = IPv4 → MAC
Ethernet = Local frame delivery
```

These technologies work together constantly in Linux, Cloud, and DevOps
environments.
