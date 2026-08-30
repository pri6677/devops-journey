# Networking Lesson 03 — Packets, Frames & How Data Travels

## 1. Core idea

Network data does not travel as one giant message. It is prepared and packaged so networking systems can deliver it across networks.

```text
Application Data
       ↓
      Data
       ↓
     Packet
       ↓
     Frame
       ↓
Physical / Radio Signals
```

## 2. Real-world analogy

Think of sending a parcel:

```text
Gift
 ↓
Put it in a box
 ↓
Write destination information
 ↓
Give it to delivery company
 ↓
It travels through multiple locations
 ↓
Recipient receives it
```

Networking is similar:

```text
Your Data
   ↓
Networking information added
   ↓
Packet
   ↓
Frame
   ↓
Network
   ↓
Frame removed
   ↓
Packet processed
   ↓
Data reaches application
```

## 3. What is a packet?

A packet is a unit of network-layer data.

For IPv4 networking, an IP packet contains information such as:

- Source IP
- Destination IP
- Protocol
- TTL
- Data / payload

```text
┌─────────────────────────────┐
│ Source IP                   │
├─────────────────────────────┤
│ Destination IP              │
├─────────────────────────────┤
│ Other IP information        │
├─────────────────────────────┤
│ Payload / Data              │
└─────────────────────────────┘
```

## 4. What is a frame?

A frame is a data-link-layer unit used to carry data across a particular local network link.

For Ethernet, a frame contains information such as:

- Source MAC
- Destination MAC
- Payload
- Frame information

```text
┌─────────────────────────────┐
│ Destination MAC             │
├─────────────────────────────┤
│ Source MAC                  │
├─────────────────────────────┤
│ Payload                     │
├─────────────────────────────┤
│ Frame information           │
└─────────────────────────────┘
```

Important mental model:

```text
IP → Packet
MAC → Frame
```

## 5. Packet vs Frame

```text
Frame
┌───────────────────────────────┐
│ MAC information               │
│                               │
│   Packet                      │
│   ┌───────────────────────┐   │
│   │ IP information        │   │
│   │                       │   │
│   │       Data            │   │
│   └───────────────────────┘   │
└───────────────────────────────┘
```

Think:

- Packet → Network layer
- Frame → Data Link layer

## 6. What happens when you ping 8.8.8.8?

Command:

```bash
ping -c 4 8.8.8.8
```

`ping` uses ICMP.

Simplified journey:

```text
Your ping command
       ↓
      ICMP
       ↓
       IP
       ↓
Network interface
       ↓
      Wi-Fi
       ↓
     Router
       ↓
    Internet
       ↓
    8.8.8.8
```

## 7. Your actual network journey

Your latest machine had:

```text
Your laptop:
192.168.0.152

Default gateway:
192.168.0.1
```

Simplified:

```text
                  INTERNET
                      │
                  8.8.8.8
                      ▲
                      │
                   Router
                      │
                192.168.0.1
                      ▲
                      │
                   Wi-Fi
                      ▲
                      │
               192.168.0.152
                  Your PC
```

## 8. Local frame destination

Your laptop does NOT send a local Wi-Fi/Ethernet frame directly to the MAC address of 8.8.8.8.

Because 8.8.8.8 is not on your local network, the local frame is sent toward the next-hop device: the router.

```text
IP destination:
8.8.8.8

Local frame destination:
Router's MAC address
```

This becomes clearer when studying routing and ARP.

## 9. Why do we need packets?

Large data can be divided into manageable pieces.

```text
Large Data
     ↓
┌────┬────┬────┬────┬────┐
│ P1 │ P2 │ P3 │ P4 │ P5 │
└────┴────┴────┴────┴────┘
```

## 10. Encapsulation

Encapsulation is the process where networking layers add their own information around data.

Simplified:

```text
Application Data
       ↓
     + TCP
       ↓
   TCP Segment
       ↓
     + IP
       ↓
    IP Packet
       ↓
   + Ethernet
       ↓
 Ethernet Frame
       ↓
 Physical transmission
```

Later we will learn:

- TCP produces a segment
- UDP produces a datagram
- IP produces a packet
- Ethernet produces a frame

Main idea:

> Each layer wraps the data with information needed by that layer.

## 11. Decapsulation

The destination performs the reverse process.

```text
Ethernet Frame
       ↓
Remove frame information
       ↓
IP Packet
       ↓
Remove IP information
       ↓
TCP Segment
       ↓
Remove TCP information
       ↓
Application Data
```

Sender:

```text
Data
 ↓
Segment
 ↓
Packet
 ↓
Frame
 ↓
Network
```

Receiver:

```text
Network
 ↓
Frame
 ↓
Packet
 ↓
Segment
 ↓
Data
```

## 12. Why networking uses layers

Different layers have different responsibilities. This separation makes networking systems easier to design, understand, troubleshoot, and evolve.

This becomes the foundation of:

- OSI model
- TCP/IP model

## 13. Frames can change between network links

The IP packet can travel across multiple routers, while the link-layer frame is specific to the current network link.

```text
Laptop
  │
  │ Frame A
  ↓
Router 1
  │
  │ Frame B
  ↓
Router 2
  │
  │ Frame C
  ↓
Router 3
  │
  ↓
Destination
```

Do not think that one frame travels unchanged across the entire Internet.

## 14. Routers process packets

A router receives traffic and determines where it should go next.

```text
             Router
          ┌──────────┐
Packet →  │ Routing  │
          │ Decision │
          └────┬─────┘
               │
               ↓
          Next Network
```

The router uses the destination IP and routing information to determine the next direction.

## 15. What happens on your local network?

Your latest machine had:

```text
192.168.0.152
```

and wanted to reach:

```text
8.8.8.8
```

Because 8.8.8.8 is outside the local network, the laptop uses its default gateway:

```text
192.168.0.1
```

```text
Destination
8.8.8.8
   ↓
Not local
   ↓
Use default gateway
   ↓
192.168.0.1
   ↓
Router forwards traffic
```

## 16. Linux observations

Check interfaces:

```bash
ip addr
```

Check a specific interface:

```bash
ip addr show wlp2s0
```

Your latest output showed:

```text
wlp2s0
inet 192.168.0.152/24
```

Check the route:

```bash
ip route
```

Your latest output showed:

```text
default via 192.168.0.1 dev wlp2s0
```

This means traffic for destinations outside known networks uses `192.168.0.1` through `wlp2s0`.

Check neighbors:

```bash
ip neigh
```

Your latest output included:

```text
192.168.0.1 dev wlp2s0 lladdr 50:0f:f5:76:59:d0 REACHABLE
```

So Linux knows:

```text
IP:
192.168.0.1

MAC:
50:0f:f5:76:59:d0
```

This is a preview of ARP.

## 17. Docker interface

Your machine also showed:

```text
docker0
172.17.0.1/16
```

This is a Docker virtual network interface. It will become useful later when studying Docker networking.

## 18. Practical lab completed

Commands:

```bash
ip link
ip addr show wlp2s0
ip route
ip neigh
ping -c 4 8.8.8.8
```

Your latest ping result:

```text
4 packets transmitted
4 received
0% packet loss
```

Average round-trip time:

```text
7.810 ms
```

This confirms successful ICMP connectivity to 8.8.8.8.

## 19. Your actual Linux network

```text
                    Internet
                       │
                    8.8.8.8
                       │
                  192.168.0.1
                    Router
                       │
                    Wi-Fi
                       │
                  wlp2s0
                       │
                192.168.0.152
                    Your PC
```

Your Ethernet interface:

```text
enp1s0
```

was not connected:

```text
NO-CARRIER
state DOWN
```

Your Wi-Fi interface:

```text
wlp2s0
```

was connected:

```text
UP
LOWER_UP
```

## 20. DevOps connection

Consider:

```text
Internet
   ↓
Load Balancer
   ↓
Web Server
   ↓
Application Server
   ↓
Database
```

If the application cannot communicate with the database, a DevOps engineer needs to reason about:

```text
Is the network reachable?
        ↓
Is routing correct?
        ↓
Is the destination IP correct?
        ↓
Is the correct port reachable?
        ↓
Is traffic blocked?
        ↓
Is the application listening?
```

Later, `tcpdump` will allow us to observe real network traffic.

## 21. Common mistakes

### Mistake 1: Packet and frame are the same

Incorrect.

```text
Packet → Network layer
Frame  → Data Link layer
```

### Mistake 2: MAC identifies the final Internet destination

Normally, MAC addresses are used for communication on the local link.

### Mistake 3: One frame travels unchanged across the Internet

Not normally. Frames are associated with individual network links and can change as traffic moves between routers.

### Mistake 4: The Internet is one network

No. The Internet is a collection of interconnected networks.

## 22. Lesson mental model

```text
                 YOUR DATA
                     │
                     ↓
              Transport Layer
                     │
                     ↓
                IP Packet
                     │
                     ↓
                  Frame
                     │
                     ↓
             Network Interface
                     │
                     ↓
                  Wi-Fi
                     │
                     ↓
                  Router
                     │
                     ↓
                Other Routers
                     │
                     ↓
                Destination
```

## 23. Key takeaways

1. Network data is packaged for transmission.
2. A packet is associated with the network layer.
3. A frame is associated with the data-link layer.
4. IP addresses are used for network-layer addressing.
5. MAC addresses are used on the local link.
6. Encapsulation adds layer-specific information.
7. Decapsulation removes that information at the receiver.
8. A frame does not normally remain unchanged across the entire Internet.
9. A router forwards traffic toward the destination.
10. A device uses its default gateway for destinations outside its local network.
11. Linux lets us observe networking with `ip addr`, `ip route`, and `ip neigh`.

## 24. Next lesson

### Networking Lesson 04 — OSI Model

We will learn:

```text
Layer 7 → Application
Layer 6 → Presentation
Layer 5 → Session
Layer 4 → Transport
Layer 3 → Network
Layer 2 → Data Link
Layer 1 → Physical
```

Instead of memorizing seven names, we will use real traffic to understand what happens from an application down to the physical network.
