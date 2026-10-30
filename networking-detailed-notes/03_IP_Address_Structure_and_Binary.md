# Networking for DevOps — Lecture 03
## IP Address Structure and Binary Representation

Let's revise Lecture 03 from the beginning, building up from the basics to the level where you can understand how IP addresses work in real networks.

**In this lecture, your main goal is to understand what an IPv4 address represents, why it has four numbers, what an octet is, and how binary relates to IP addressing.**

---

# 1. What Is an IP Address?

**IP stands for Internet Protocol.**

An IP address is a logical address used to identify a network interface so that data can be delivered to the correct destination across a network.

Think about sending a letter to someone.

For the letter to reach the right person, you need an address. Similarly, when your computer sends data over a network, it needs an IP address to identify the intended destination.

For example:

```text
192.168.1.10
```

This is an example of an IPv4 address.

Imagine that your laptop is communicating with another computer:

```text
Your Laptop                       Another Computer
192.168.1.10  ------------------> 192.168.1.20
```

Your laptop uses the destination IP address to determine where the data should go.

However, **an IP address alone does not guarantee delivery**. Routing, network configuration, firewalls, and other factors also affect whether the data reaches its destination.

### Why do we need IP addresses?

IP addresses help us:

1. Identify network interfaces.
2. Identify the network to which an address belongs, using the relevant subnet information.
3. Determine where packets should be routed.
4. Communicate between devices on the same network or across different networks.

### A practical example

Suppose your laptop has this configuration:

```text
IP address:  192.168.1.10
Subnet mask: 255.255.255.0
```

Your laptop wants to communicate with a server at:

```text
192.168.1.20
```

The IP address and subnet mask help the laptop determine whether the destination is on the same local subnet.

We'll explore subnet masks in a later lecture.

---

# 2. What Is IPv4?

There are different versions of the Internet Protocol, including IPv4 and IPv6.

For this lecture, we're focusing on IPv4.

**IPv4 uses a 32-bit address.**

Consider this example:

```text
192.168.1.10
```

At first glance, it looks like four ordinary decimal numbers separated by dots.

But internally, an IPv4 address is represented using **32 binary digits**.

For example:

```text
192.168.1.10

       ↓

11000000.10101000.00000001.00001010
```

The dots separate four groups of eight bits.

Let's understand why.

---

# 3. What Is Binary?

Computers represent digital information using bits.

A **bit** is the smallest unit of digital information. It can have one of two values:

```text
0 or 1
```

Our everyday number system is decimal, which uses ten digits:

```text
0 1 2 3 4 5 6 7 8 9
```

Binary uses only two:

```text
0 1
```

Computers use binary representations because digital electronic systems can encode information using two distinguishable states.

For example, we can represent a simplified pair of states as:

| Binary value | Simplified interpretation |
|---|---|
| `0` | Off |
| `1` | On |

This is a useful analogy, although actual computer hardware is more complex.

## 3.1 Decimal versus binary

In the decimal number system, each position represents a power of 10.

For example:

```text
345
```

means:

$$
345 = (3 \times 100) + (4 \times 10) + (5 \times 1)
$$

Or:

$$
345 = (3 \times 10^2) + (4 \times 10^1) + (5 \times 10^0)
$$

Binary works similarly, but each position represents a power of 2.

Consider:

```text
1011
```

Its value is:

$$
1011_2 = (1 \times 8) + (0 \times 4) + (1 \times 2) + (1 \times 1)
$$

$$
= 8 + 0 + 2 + 1
$$

$$
= 11_{10}
$$

Therefore:

$$
\boxed{1011_2 = 11_{10}}
$$

The subscripts indicate the number system: base 2 for binary and base 10 for decimal.

**Networking connection:** When you see an IP address written as `192.168.1.10`, you're looking at its human-friendly decimal representation. The underlying address is a 32-bit value.

---

# 4. What Is an Octet?

An IPv4 address contains 32 bits, divided into four groups.

Each group contains eight bits and is called an **octet**.

For example:

```text
192       .168       .1         .10
  ↓         ↓         ↓          ↓
Octet 1   Octet 2   Octet 3    Octet 4
```

Each octet contains eight binary digits.

The complete structure looks like this:

```text
IPv4 address: 192.168.1.10

Binary representation:

11000000 . 10101000 . 00000001 . 00001010
    8          8          8          8
   bits       bits       bits       bits
```

Let's calculate the total.

$$
4 \times 8 = 32 \text{ bits}
$$

Since one byte contains eight bits:

$$
32 \div 8 = 4 \text{ bytes}
$$

Therefore:

- Total length: **32 bits**
- Number of octets: **4**
- Bits per octet: **8**
- Total size: **4 bytes**

### Remember this

An octet is not a special networking device or protocol. It simply means a group of eight bits.

The term is commonly used when discussing IPv4 addresses.

---

# 5. Why Does an IPv4 Address Have Four Numbers?

An IPv4 address is commonly written in **dotted-decimal notation**.

For example:

```text
192.168.1.10
```

The four decimal numbers represent the four 8-bit octets.

The general format is:

```text
A.B.C.D
```

Each number represents one octet.

Since an octet contains eight bits, it can represent values from 0 to 255.

Why?

An eight-bit binary number has:

$$
2^8 = 256
$$

possible combinations.

Because the values start at zero, the range is:

$$
\boxed{0 \text{ to } 255}
$$

For example:

| Decimal value | Binary representation |
|---:|---|
| 0 | `00000000` |
| 1 | `00000001` |
| 2 | `00000010` |
| 10 | `00001010` |
| 127 | `01111111` |
| 128 | `10000000` |
| 192 | `11000000` |
| 255 | `11111111` |

Each of these binary values is exactly eight bits long.

Consequently, every octet in a conventionally written IPv4 address must represent a value from 0 through 255.

For example:

```text
192.168.1.10     Valid IPv4 format
10.0.0.1         Valid IPv4 format
256.1.2.3        Invalid: 256 exceeds the octet range
192.168.1.300    Invalid: 300 exceeds the octet range
```

These examples illustrate the format and range rules, not whether an address is assigned to a particular device.

---

# 6. Understanding Binary Place Values

This is one of the most important concepts for understanding IP addressing and subnetting.

Each position in an eight-bit octet has a specific value.

From left to right, the values are:

| Bit position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Place value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

Notice that the values double as we move from right to left.

These are the powers of 2:

$$
2^7,\;2^6,\;2^5,\;2^4,\;2^3,\;2^2,\;2^1,\;2^0
$$

So:

```text
Binary:       1  1  0  0  0  0  0  0
Place value: 128 64 32 16  8  4  2  1
```

To convert binary to decimal, add the place values wherever the binary digit is `1`.

For the example above:

$$
128 + 64 = 192
$$

Therefore:

$$
\boxed{11000000_2 = 192_{10}}
$$

Let's use this knowledge to convert a complete IP address.

---

# 7. Converting an IP Address from Decimal to Binary

Consider:

```text
192.168.1.10
```

We convert each octet separately.

## Octet 1: 192

The place values are:

```text
128  64  32  16  8  4  2  1
```

To make 192:

$$
192 = 128 + 64
$$

Therefore, the bits for 128 and 64 are `1`, and the remaining bits are `0`.

```text
Decimal: 192
Binary:  11000000
```

## Octet 2: 168

$$
168 = 128 + 32 + 8
$$

So:

```text
Decimal: 168
Binary:  10101000
```

Check the calculation:

$$
128 + 32 + 8 = 168
$$

## Octet 3: 1

Only the final bit is set:

```text
Decimal: 1
Binary:  00000001
```

The leading zeros are important because an octet must be represented using eight bits in this notation.

## Octet 4: 10

$$
10 = 8 + 2
$$

Therefore:

```text
Decimal: 10
Binary:  00001010
```

## Complete conversion

| Octet | Decimal | Binary |
|---|---:|---|
| 1 | 192 | `11000000` |
| 2 | 168 | `10101000` |
| 3 | 1 | `00000001` |
| 4 | 10 | `00001010` |

The complete address is:

```text
Decimal:
192.168.1.10

Binary:
11000000.10101000.00000001.00001010
```

Each group has eight bits, giving a total of 32 bits.

**DevOps connection:** You usually won't need to convert every IP address manually in your daily work. However, understanding binary makes subnet masks, CIDR notation, network ranges, and routing decisions much easier to understand.

---

# 8. Converting Binary to Decimal

Now let's reverse the process.

Suppose you encounter this binary octet:

```text
11000000
```

Write the place values underneath:

```text
Binary:       1  1  0  0  0  0  0  0
Place value: 128 64 32 16  8  4  2  1
```

Select the place values corresponding to `1`:

$$
128 + 64 = 192
$$

Therefore:

```text
11000000 = 192
```

Try another:

```text
Binary: 10101000
```

The `1` bits correspond to:

- 128
- 32
- 8

Adding them:

$$
128 + 32 + 8 = 168
$$

Therefore:

```text
10101000 = 168
```

### Quick reference

| Binary | Decimal |
|---|---:|
| `00000000` | 0 |
| `00000001` | 1 |
| `00001010` | 10 |
| `01111111` | 127 |
| `10000000` | 128 |
| `11000000` | 192 |
| `11111111` | 255 |

You don't need to memorize every possible conversion. Focus on understanding the place-value method.

---

# 9. How Many IPv4 Addresses Are Possible?

An IPv4 address has 32 bits.

Each bit has two possible values:

```text
0 or 1
```

Therefore, the total number of possible 32-bit patterns is:

$$
2^{32}
$$

Which equals:

$$
\boxed{4,294,967,296}
$$

That is approximately **4.29 billion possible IPv4 addresses**.

This number represents the total address space, not the number of public IP addresses available for ordinary assignment. Some addresses are reserved for special purposes, private networks, multicast, and other uses.

### Why does this matter?

IPv4 has a limited address space. As the number of connected devices grew, the world needed ways to use addresses more efficiently.

Technologies such as NAT help many devices share a public IPv4 address, while IPv6 provides a much larger address space.

We'll discuss these topics when they appear in your networking roadmap.

---

# 10. What Is `127.0.0.1`?

Your revision guide mentions:

```text
127.0.0.1
```

This is the IPv4 **loopback address** commonly used to refer to the local machine.

When an application connects to `127.0.0.1`, it communicates with a service on the same machine rather than sending traffic to another computer on the physical network.

For example, if a web server is listening on port 8000, you might access it through:

```text
http://127.0.0.1:8000
```

This works if the server is listening on that address or an appropriate local interface.

### Try it on your Linux system

Run:

```bash
ping -c 4 127.0.0.1
```

Possible output:

```text
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.05 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.04 ms
```

Your exact output will differ.

Let's break down the command:

| Component | Meaning |
|---|---|
| `ping` | Sends network diagnostic requests to test connectivity |
| `-c 4` | Sends four requests and then stops |
| `127.0.0.1` | The local IPv4 loopback address |

The loopback interface is generally named `lo` on Linux.

Check it with:

```bash
ip addr show lo
```

You should see an interface entry containing an address similar to:

```text
inet 127.0.0.1/8
```

The `/8` is subnet-prefix notation. We'll explore what it means in the CIDR and subnetting lectures.

### Important distinction

`127.0.0.1` does not identify your laptop to other computers on your Wi-Fi network.

It refers to the local machine itself. Other devices cannot use their own `127.0.0.1` address to reach your laptop; that address always refers to the device on which it is used.

---

# 11. Connecting This Lecture to DevOps

You might wonder why a future Cloud or DevOps Engineer needs to understand bits and IP addresses.

Consider a simple cloud environment:

```text
                  Internet
                     |
                     |
                  Router
                     |
               Cloud Network
                     |
              +------+------+
              |             |
          Web Server     App Server
          10.0.1.10      10.0.2.20
```

In a real environment, network configuration determines how these systems communicate.

For example:

- A cloud server receives traffic through its configured network interfaces.
- A routing table determines where packets should go next.
- A subnet mask or prefix helps determine which addresses belong to a particular subnet.
- Firewall rules can permit or block traffic.
- Services use ports to identify the destination application.

Understanding the structure of IPv4 addresses prepares you for these subjects.

### Where you'll use this knowledge

| DevOps topic | Why IPv4 knowledge matters |
|---|---|
| Linux networking | Inspecting and understanding interface addresses |
| AWS VPC | Understanding private IP ranges and subnet CIDRs |
| Docker | Understanding container network addresses |
| Kubernetes | Understanding Pod and Service networking |
| Troubleshooting | Identifying incorrect or unexpected IP configurations |
| Subnetting | Calculating network ranges and address capacity |
| Routing | Understanding how IP destinations influence packet forwarding |

For example, on Linux you can inspect your network interfaces with:

```bash
ip addr
```

Inspect routing information with:

```bash
ip route
```

These commands will become more meaningful as you learn subnetting, routing, and gateways.

---

# 12. Common Mistakes to Avoid

### Mistake 1: Thinking an IPv4 address has four bits

Incorrect:

```text
192.168.1.10 = 4 bits
```

Correct:

```text
4 octets × 8 bits = 32 bits
```

The four decimal numbers represent four groups of eight bits.

### Mistake 2: Thinking an octet can contain any decimal number

Incorrect:

```text
192.168.1.300
```

Correct:

Every octet must represent a value between `0` and `255`.

### Mistake 3: Confusing bits and bytes

Remember:

```text
1 byte = 8 bits
```

Therefore:

```text
IPv4 address = 32 bits = 4 bytes
```

### Mistake 4: Assuming every IP address is public

An IP address can be private, public, loopback, or reserved for another special purpose.

For example:

- `192.168.1.10` is within a private IPv4 range.
- `127.0.0.1` is a loopback address.

An address's decimal format alone does not tell you whether it is publicly routable.

### Mistake 5: Thinking the IP address is a physical address

An IP address is a logical network-layer address. A MAC address serves a different purpose at the data-link layer.

You'll explore their differences in your later lectures on MAC addresses and ARP.

---

# 13. Quick Revision Cheat Sheet

| Concept | Key fact |
|---|---|
| IP | Internet Protocol |
| IPv4 address length | 32 bits |
| Number of IPv4 octets | 4 |
| Bits per octet | 8 |
| Size of one octet | 1 byte |
| Total IPv4 size | 4 bytes |
| Minimum octet value | 0 |
| Maximum octet value | 255 |
| Number of possible IPv4 bit patterns | \(2^{32}\) |
| Total possible patterns | 4,294,967,296 |
| Loopback IPv4 address | `127.0.0.1` |
| Binary digits | `0` and `1` |
| Decimal number system | Base 10 |
| Binary number system | Base 2 |

## The three facts you must remember

$$
1. **IPv4 = 32 bits = 4 octets = 4 bytes.**
$$
2. **Each octet contains 8 bits and represents a decimal value from 0 to 255.**
3. **Binary place values are 128, 64, 32, 16, 8, 4, 2, and 1.**

---

# 14. Interview Questions and Answers

### Q1. What is an IP address?

An IP address is a logical address used to identify a network interface and support packet delivery across IP networks.

### Q2. What is IPv4?

IPv4 is version 4 of the Internet Protocol. It uses 32-bit addresses, conventionally written as four decimal octets separated by dots.

### Q3. Why does an IPv4 address have four octets?

A 32-bit IPv4 address is divided into four groups of eight bits. Each group is called an octet.

### Q4. Why does an octet have a maximum value of 255?

$$
An octet contains eight bits, giving it \(2^8 = 256\) possible combinations. Since the range starts at zero, the maximum value is 255.
$$

### Q5. How many bits are in an IPv4 address?

An IPv4 address contains 32 bits.

### Q6. What is the difference between a bit and a byte?

A bit is a single binary digit. A byte contains eight bits.

### Q7. Convert `11000000` from binary to decimal.

The `1` bits correspond to 128 and 64.

$$
128 + 64 = 192
$$

Answer: **192**.

### Q8. What is `127.0.0.1`?

It is the IPv4 loopback address, used to communicate with the local machine.

### Q9. How many possible 32-bit IPv4 address patterns exist?

$$
2^{32} = 4,294,967,296
$$

### Q10. Why should a DevOps Engineer understand IP addressing?

It is foundational to configuring Linux networking, cloud networks, routing, container networking, subnetting, and troubleshooting connectivity.

---

# 15. Practical Exercises

Try these exercises on paper or in your Linux terminal.

### Exercise 1: Identify the structure

For the IPv4 address:

```text
10.20.30.40
```

Identify:

1. Number of octets.
2. Bits per octet.
3. Total number of bits.
4. Total number of bytes.

### Exercise 2: Convert decimal to binary

Convert each value into an eight-bit binary number:

```text
A. 10
B. 20
C. 64
D. 128
E. 255
```

### Exercise 3: Convert binary to decimal

Convert the following eight-bit values:

```text
A. 00000001
B. 00001010
C. 01000000
D. 10000000
E. 11111111
```

### Exercise 4: Inspect your Linux system

Run:

```bash
ip addr
```

Find the following:

- Your loopback interface.
- The IPv4 address assigned to your Wi-Fi interface.
- The subnet prefix shown beside that address.

Don't share your public IP address or other network information publicly unless you understand the privacy implications.

### Exercise 5: Test loopback connectivity

Run:

```bash
ping -c 4 127.0.0.1
```

Then answer:

1. What does `ping` test?
2. Why does `127.0.0.1` refer to your own machine?
3. Does a successful loopback test prove that your Wi-Fi or internet connection works?

The answer to the third question is **no**. Loopback testing checks local networking; it does not prove external connectivity.

---

## Final takeaway

Lecture 03 establishes the mathematical foundation of IPv4 addressing. Once you understand how a 32-bit address is divided into four octets and how binary values map to decimal numbers, subnet masks and CIDR notation become much easier to understand.

**Next in your roadmap:** Lecture 04 builds on this foundation with network and host portions, CIDR notation, and address capacity.
