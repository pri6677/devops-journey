# Lecture 08: What Is a MAC Address? Understanding Its Structure and Purpose

**Course:** Networking for DevOps  
**Lecture:** 08  
**Topic:** Network Interfaces, MAC Addresses, Structure, Hexadecimal Representation, OUI, and Device Identification

This lesson follows the topics you shared from your lecture. I'll explain each one in detail, including how it works, Linux commands for practical learning, examples, and connections to DevOps.

---

# 1. What Is a Network Interface?

Before understanding MAC addresses, you need to understand **network interfaces**.

A network interface is a point through which a device connects to a network and sends or receives data.

For example, your laptop might connect to the internet using Wi-Fi, while a desktop computer might use an Ethernet cable.

Both connections use network interfaces.

## Types of network interfaces

### A. Ethernet interface

An Ethernet interface allows a device to communicate over a wired Ethernet network.

It typically connects to a router or switch using an Ethernet cable.

```text
Laptop
  |
  | Ethernet cable
  |
  v
Network Switch
  |
  v
Router
  |
  v
Internet
```

The network interface hardware processes Ethernet frames and sends or receives network traffic over the wired connection.

**Example:** A server in a data centre may use one or more Ethernet interfaces to communicate with other servers and network devices.

### B. Wi-Fi interface

A Wi-Fi interface allows a device to communicate wirelessly with a Wi-Fi access point or wireless router.

```text
Laptop
  |
  | Wi-Fi signals
  |
  v
Wi-Fi Router / Access Point
  |
  v
Internet
```

Wi-Fi interfaces typically contain radio hardware and associated circuitry that allows them to send and receive wireless signals.

Your laptop's Wi-Fi interface is an example.

### C. Bluetooth interface

Bluetooth provides short-range wireless communication between devices.

Examples include:
- Wireless headphones
- Keyboards and mice
- Smartphones
- Other nearby Bluetooth-enabled devices

Bluetooth is a networking technology, but it does not use Ethernet in the same way as a conventional wired LAN.

**Important distinction:** A network interface is not the same thing as a network cable. The interface is the connection point and associated hardware or software; a cable is one possible medium used to carry signals.

---

# 2. What Is a MAC Address?

**MAC stands for Media Access Control.**

A MAC address is a link-layer address used to identify a network interface within a local network communication system.

A typical MAC address looks like this:

```text
A4:5E:60:C2:10:9B
```

It contains six hexadecimal pairs.

A MAC address is associated with a network interface rather than being the same thing as a device's IP address.

For example, your laptop might have:
- One MAC address for its Wi-Fi interface.
- A different MAC address for its Ethernet interface.
- Other addresses associated with virtual interfaces.

A MAC address is commonly used by Ethernet switches to determine where to forward Ethernet frames within a local network.

## Why do we need MAC addresses?

To understand this, let's compare IP addresses and MAC addresses.

### IP address example

Suppose your laptop connects to a home network.

```text
Laptop IP: 192.168.1.10
```

When it connects to another network, it might receive a different IP address:

```text
Laptop IP: 10.0.0.25
```

The IP address can change because IP addressing depends on the network configuration.

For example, a DHCP server may assign a different IP address when a device connects to a different network.

### MAC address example

The same Wi-Fi interface might have a hardware-assigned MAC address such as:

```text
A4:5E:60:C2:10:9B
```

That address may remain the same when the device changes IP networks.

This helps distinguish the network interface's link-layer identity from its current IP address.

### Important clarification about permanence

Your lecture describes MAC addresses as permanent, hardcoded physical addresses. That is a useful introduction to factory-assigned MAC addresses, but there is an important technical distinction:

**A MAC address is not guaranteed to be permanent or impossible to change.**

- Network interfaces commonly have a factory-assigned address.
- Operating systems can use MAC address randomization, especially for Wi-Fi privacy.
- Administrators can sometimes configure a different MAC address.
- Virtual machines and software-defined interfaces can have configured MAC addresses.

Therefore, a MAC address is **not a guaranteed permanent identifier of a physical device**.

For this lesson, remember that a factory-assigned MAC address is usually associated with a particular network interface, while its active MAC address can sometimes be changed or randomized.

---

# 3. MAC Address Structure: Understanding the 48 Bits

A conventional MAC address used by Ethernet is **48 bits long**, equivalent to six bytes.

Let's calculate that.

We know:

```text
1 byte = 8 bits
```

A MAC address contains six bytes:

```text
6 bytes × 8 bits per byte = 48 bits
```

Therefore:

**A conventional 48-bit MAC address contains 48 bits.**

## Example MAC address

Consider:

```text
A4:5E:60:C2:10:9B
```

Each pair represents one byte.

| Position | Hexadecimal pair | Size |
|---|---|---:|
| Byte 1 | `A4` | 8 bits |
| Byte 2 | `5E` | 8 bits |
| Byte 3 | `60` | 8 bits |
| Byte 4 | `C2` | 8 bits |
| Byte 5 | `10` | 8 bits |
| Byte 6 | `9B` | 8 bits |
| **Total** | **6 pairs** | **48 bits** |

The colons separate the bytes to make the address easier to read.

Without separators, the address would be:

```text
A45E60C2109B
```

This representation contains 12 hexadecimal digits.

## Why are there 12 hexadecimal digits?

One hexadecimal digit represents four binary bits.

For example:

```text
Hexadecimal F = Binary 1111
```

Each hexadecimal pair contains two hexadecimal digits:

```text
A4 = 8 bits
```

A MAC address contains six pairs:

```text
6 pairs × 2 hexadecimal digits = 12 hexadecimal digits
12 hexadecimal digits × 4 bits = 48 bits
```

That is why a 48-bit MAC address is normally represented using 12 hexadecimal digits.

---

# 4. Understanding Hexadecimal Notation

Your lecture introduces hexadecimal because MAC addresses are written using base 16.

Let's understand what that means.

We normally count in decimal, which uses ten symbols:

```text
0 1 2 3 4 5 6 7 8 9
```

Hexadecimal uses 16 symbols:

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

The letters represent decimal values greater than nine.

| Hexadecimal | Decimal |
|---|---:|
| `0` | 0 |
| `1` | 1 |
| `2` | 2 |
| `3` | 3 |
| `4` | 4 |
| `5` | 5 |
| `6` | 6 |
| `7` | 7 |
| `8` | 8 |
| `9` | 9 |
| `A` | 10 |
| `B` | 11 |
| `C` | 12 |
| `D` | 13 |
| `E` | 14 |
| `F` | 15 |

After `9`, hexadecimal continues with `A`, `B`, `C`, `D`, `E`, and `F`.

After `F`, the next value is `10` in hexadecimal, which equals decimal 16.

## Example: Convert a hexadecimal pair into binary

Consider:

```text
A4
```

Convert each hexadecimal digit separately:

```text
A = 1010
4 = 0100
```

Combine them:

```text
A4 = 10100100
```

That is eight binary bits, or one byte.

Let's try another example:

```text
5E
```

Convert each digit:

```text
5 = 0101
E = 1110
```

Combine them:

```text
5E = 01011110
```

Again, the result is eight bits.

### Visualizing a complete MAC address

Consider:

```text
A4:5E:60:C2:10:9B
```

Its binary representation is:

```text
A4 = 10100100
5E = 01011110
60 = 01100000
C2 = 11000010
10 = 00010000
9B = 10011011
```

The full binary address is:

```text
10100100 01011110 01100000
11000010 00010000 10011011
```

There are six groups of eight bits, giving 48 bits in total.

**For now, you do not need to convert every MAC address manually.** Focus on understanding why hexadecimal is used and how each pair represents one byte.

---

# 5. MAC Address Format on Linux, macOS, and Windows

MAC addresses can be displayed using different separators.

### Linux and macOS

A common representation is:

```text
A4:5E:60:C2:10:9B
```

### Windows

Windows commonly displays the address using hyphens:

```text
A4-5E-60-C2-10-9B
```

These are two display formats for the same hexadecimal value.

The separators do not change the underlying address.

---

# 6. OUI: The Organizationally Unique Identifier

Now let's understand the division of a conventional 48-bit MAC address.

Consider this example:

```text
A4:5E:60:C2:10:9B
```

For a conventional globally administered unicast MAC address, the first three bytes are commonly associated with the **OUI (Organizationally Unique Identifier)**.

The last three bytes are the remaining portion of the address.

```text
A4:5E:60 | C2:10:9B
     OUI | Remaining address bits
```

Each section contains three bytes, or 24 bits.

| Section | Size | Purpose |
|---|---:|---|
| First three bytes | 24 bits | Identifies an assigned address block associated with an organization |
| Last three bytes | 24 bits | Distinguishes addresses within that block |
| **Total** | **48 bits** | Complete MAC address |

## 6.1 What does the OUI tell us?

Organizations receive assigned address blocks that can be used to construct MAC addresses.

The organization may be a network hardware manufacturer, such as a company producing network adapters or networking equipment.

For example, a company might receive an address block and allocate addresses from that block to its network interfaces.

When a MAC address uses a globally assigned OUI, looking up the prefix may identify the organization associated with that assignment.

However, **the OUI does not guarantee the identity of the device's current owner or manufacturer**. Virtual interfaces, locally administered addresses, and MAC spoofing can complicate identification.

## 6.2 What is the purpose of the remaining three bytes?

The remaining 24 bits can be used to distinguish individual addresses within the assigned block.

A simplified illustration:

```text
Organization's assigned block
             |
             v
     A4:5E:60:XX:XX:XX
             |
             +---- Interface 1: A4:5E:60:00:00:01
             |
             +---- Interface 2: A4:5E:60:00:00:02
             |
             +---- Interface 3: A4:5E:60:00:00:03
```

These addresses are illustrative, not claims about a real manufacturer's allocation.

Also, the final 24 bits are not always a simple sequential device number. Allocation methods vary, and not every MAC address follows this simplified manufacturer-assignment model.

### Key takeaway

The OUI identifies an assigned address block, while the remaining bits distinguish addresses within that block.

---

# 7. How Does a MAC Address Help Devices Communicate?

Let's connect this lesson to your previous lectures.

Suppose two computers are connected to the same Ethernet network.

```text
Computer A                     Computer B
IP: 192.168.1.10                IP: 192.168.1.20
MAC: AA:AA:AA:AA:AA:AA          MAC: BB:BB:BB:BB:BB:BB
        |                              |
        +----------- Switch -----------+
```

Computer A wants to send data to Computer B.

### Step 1: Computer A determines the destination IP

Computer A checks its routing information and determines that Computer B is on the same subnet.

### Step 2: Computer A obtains the destination MAC address

If Computer A does not already know Computer B's MAC address, it uses ARP for IPv4 to discover it.

### Step 3: Computer A constructs an Ethernet frame

The frame includes:

```text
Source MAC:      AA:AA:AA:AA:AA:AA
Destination MAC: BB:BB:BB:BB:BB:BB
Source IP:       192.168.1.10
Destination IP:  192.168.1.20
```

### Step 4: The switch forwards the frame

An Ethernet switch learns MAC addresses from received frames and uses its MAC address table to decide which port should receive a frame.

Computer B receives the frame and processes the encapsulated IP packet.

This illustrates the different roles of IP and MAC addresses:

- **IP address:** Identifies the IP-layer source and destination.
- **MAC address:** Identifies the link-layer source and destination on the local link.

We'll explore the ARP process in more detail in Lecture 10, according to your supplied lecture summary.

---

# 8. Practical Lab: Find MAC Addresses on Linux

Let's inspect the network interfaces on your Zorin OS laptop.

## Step 1: List network interfaces

Run:

```bash
ip link show
```

You may see interfaces such as:

```text
lo
wlp2s0
docker0
```

Their meanings:

| Interface | Meaning |
|---|---|
| `lo` | Loopback interface used for communication within the same host |
| `wlp2s0` | An example of a wireless network interface name |
| `docker0` | A virtual bridge commonly created by Docker |

Your exact interface names may differ.

## Step 2: Display MAC addresses

Run:

```bash
ip link show
```

Example output:

```text
2: wlp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    link/ether a4:5e:60:c2:10:9b brd ff:ff:ff:ff:ff:ff
```

The important part is:

```text
link/ether a4:5e:60:c2:10:9b
```

This shows the interface's Ethernet-style link-layer address.

The example MAC address is illustrative; your actual address will be different.

### Understanding `link/ether`

- `link` indicates link-layer information.
- `ether` identifies the Ethernet-style link-layer address type.
- The hexadecimal pairs represent the address.

### What is `brd ff:ff:ff:ff:ff:ff`?

This is the Ethernet broadcast MAC address.

A broadcast frame is intended for all devices on the relevant Layer 2 broadcast domain.

Don't confuse the broadcast address with the interface's own MAC address.

## Step 3: Inspect one interface

For your Wi-Fi interface, run:

```bash
ip link show wlp2s0
```

If your Wi-Fi interface has another name, replace `wlp2s0` with the actual name shown by `ip link show`.

You can also inspect its address directly:

```bash
cat /sys/class/net/wlp2s0/address
```

This reads the address exposed by the Linux network interface.

**Privacy note:** Your MAC address is not generally a password or authentication secret, but avoid unnecessarily posting it publicly because it can be used as a network identifier in some contexts.

---

# 9. Physical and Virtual Network Interfaces

This distinction is especially important for your Cloud and DevOps roadmap.

A network interface does not always correspond to a physical network card.

## Physical interface

Examples include:

- A laptop's Wi-Fi adapter.
- A physical Ethernet network card.
- A server's Ethernet interface.

These interfaces connect the operating system to physical networking hardware.

## Virtual interface

Virtual interfaces are created or managed by software.

Examples include:

- Virtual machine network adapters.
- Docker bridge interfaces.
- Virtual Ethernet pairs.
- Some VPN interfaces.

A virtual interface can have its own MAC address, depending on the interface type.

For example, Docker may create a virtual bridge called `docker0` and connect containers to networking infrastructure through virtual interfaces.

This allows software-defined networks to connect workloads without requiring a separate physical network card for every container.

### DevOps connection

As you learn Docker, virtual machines, and Kubernetes, you'll encounter virtual networking frequently.

Understanding MAC addresses helps you understand how network interfaces participate in Layer 2 communication. However, container and cloud networking can also involve routing, overlays, virtual switches, and other mechanisms beyond basic Ethernet.

---

# 10. Important Corrections to Remember

Your lecture uses simplified explanations to introduce MAC addresses. Keep these technical details in mind as your knowledge develops.

| Lecture simplification | More precise explanation |
|---|---|
| A MAC address never changes | Factory-assigned addresses often remain stable, but addresses can be randomized or changed. |
| Every MAC address identifies a physical device | Virtual interfaces can also have MAC addresses. |
| The first three bytes always identify the manufacturer | The OUI model applies to relevant globally assigned address blocks; locally administered addresses may not identify a manufacturer. |
| The last three bytes uniquely identify a physical network card worldwide | They distinguish addresses within an assigned block, but a MAC address is not a guaranteed permanent hardware identity. |
| IP addresses identify hardware | IP addresses identify network-layer endpoints or interfaces in a network configuration; they can change. |

These distinctions matter when troubleshooting Linux networking and cloud infrastructure.

---

# 11. Interview Questions and Answers

### Q1. What is a MAC address?

A MAC address is a link-layer address used by network technologies such as Ethernet to identify an interface for local network communication.

### Q2. What is the full form of MAC?

Media Access Control.

### Q3. How many bits are in a conventional Ethernet MAC address?

48 bits, or six bytes.

### Q4. Why are MAC addresses written in hexadecimal?

Hexadecimal provides a compact representation of binary data. Each hexadecimal digit represents four bits, so 12 hexadecimal digits represent 48 bits.

### Q5. What is an OUI?

An Organizationally Unique Identifier is an assigned identifier associated with an organization's address block. It commonly occupies the first 24 bits of a conventional globally administered MAC address.

### Q6. What is the difference between an IP address and a MAC address?

An IP address is used at the network layer to identify IP endpoints and support routing. A MAC address is used at the link layer for delivery over a local network link.

### Q7. Can a MAC address change?

Yes. A network interface may use a factory-assigned address, but software can sometimes configure another address, and operating systems may randomize MAC addresses for privacy.

### Q8. What is the difference between a physical and a virtual network interface?

A physical interface uses networking hardware, such as a Wi-Fi or Ethernet adapter. A virtual interface is implemented or managed through software and is used by technologies such as virtual machines and containers.

### Q9. What does this Linux command show?

```bash
ip link show
```

It displays network interfaces and their link-layer information, including MAC addresses where applicable.

### Q10. Does a router use MAC addresses to route traffic between IP networks?

A router uses IP routing information to select the next hop. It also uses link-layer addressing to transmit frames over the relevant local link.

---

# 12. Quick Revision Sheet

| Topic | Remember |
|---|---|
| Network interface | A connection point for network communication |
| MAC full form | Media Access Control |
| MAC address size | 48 bits for a conventional Ethernet MAC address |
| Number of bytes | 6 |
| Hexadecimal digits | 12 |
| Hexadecimal symbols | `0–9` and `A–F` |
| Common Linux format | `AA:BB:CC:DD:EE:FF` |
| OUI | Commonly the first 24 bits of a globally assigned MAC address |
| Remaining address bits | Distinguish addresses within the assigned block |
| Linux command | `ip link show` |
| IP address | Network-layer addressing |
| MAC address | Link-layer addressing |
| Virtual interfaces | Can also have MAC addresses |

## Practical commands to remember

```bash
# List network interfaces
ip link show

# Inspect the Wi-Fi interface
ip link show wlp2s0

# Read its current link-layer address
cat /sys/class/net/wlp2s0/address

# Display IPv4 addresses and interface details
ip -4 addr show
```

---

## Lecture 08 Completed

You have now covered the topics in your supplied Lecture 08 breakdown:

1. Network interfaces.
2. Why IP addresses and MAC addresses serve different purposes.
3. MAC address structure and 48-bit length.
4. Hexadecimal notation.
5. OUI and the remaining address bits.
6. MAC addresses in local network communication.
7. Linux commands for inspecting interfaces.
8. Physical and virtual interfaces.