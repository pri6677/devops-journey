# Networking Lesson 07: Subnetting & CIDR

## 1. What is Subnetting?

Subnetting is the process of dividing one large IP network into smaller networks called **subnets**.

Example:

    10.0.0.0/24

can be divided into smaller networks:

    10.0.0.0/25
    10.0.0.128/25

Subnetting helps organize networks, control traffic, and efficiently use IP addresses.

---

# 2. Why Subnetting Matters in DevOps

Subnetting is important in:

- AWS VPCs
- Docker networking
- Kubernetes networking
- Linux servers
- Cloud infrastructure
- Network security
- Routing
- Load balancing
- Private/public network design

Example AWS-style design:

    VPC: 10.0.0.0/16

             VPC
        10.0.0.0/16
              |
       +------+------+
       |             |
    Public         Private
    Subnet         Subnet
    10.0.1.0/24    10.0.2.0/24
       |             |
     Web/LB        App/DB

Subnetting allows infrastructure to be separated into logical networks.

---

# 3. IPv4 and CIDR

IPv4 addresses contain:

    32 bits

Example:

    192.168.1.10

Binary representation:

    11000000.10101000.00000001.00001010

CIDR notation tells us how many bits belong to the network portion.

Example:

    192.168.1.10/24

means:

    24 bits = Network portion
     8 bits = Host portion

Because:

    32 - 24 = 8

---

# 4. CIDR Notation

CIDR means:

    Classless Inter-Domain Routing

Example:

    192.168.1.0/24

The `/24` is the CIDR prefix length.

It means that the first 24 bits identify the network.

Binary:

    11111111.11111111.11111111.00000000

Therefore:

    Network bits = 24
    Host bits    = 8

---

# 5. Subnet Mask

Every CIDR prefix corresponds to a subnet mask.

Common examples:

| CIDR | Subnet Mask |
|------|-------------|
| /24 | 255.255.255.0 |
| /25 | 255.255.255.128 |
| /26 | 255.255.255.192 |
| /27 | 255.255.255.224 |
| /28 | 255.255.255.240 |
| /29 | 255.255.255.248 |
| /30 | 255.255.255.252 |

---

# 6. Number of Addresses

Formula:

    Total addresses = 2^(host bits)

Traditional usable host calculation:

    Usable hosts = 2^(host bits) - 2

The two traditionally reserved addresses are:

1. Network address
2. Broadcast address

Example:

    /24

Host bits:

    32 - 24 = 8

Total:

    2^8 = 256

Traditional usable hosts:

    256 - 2 = 254

---

# 7. Common CIDR Sizes

| CIDR | Total Addresses | Traditional Usable Hosts |
|------|----------------:|-------------------------:|
| /24 | 256 | 254 |
| /25 | 128 | 126 |
| /26 | 64 | 62 |
| /27 | 32 | 30 |
| /28 | 16 | 14 |
| /29 | 8 | 6 |
| /30 | 4 | 2 |

---

# 8. /24 Network

Example:

    192.168.1.0/24

Subnet mask:

    255.255.255.0

Network:

    192.168.1.0

Host range:

    192.168.1.1 - 192.168.1.254

Broadcast:

    192.168.1.255

Therefore:

    Network     = 192.168.1.0
    Hosts       = 192.168.1.1 - 192.168.1.254
    Broadcast   = 192.168.1.255

Traditional usable hosts:

    254

---

# 9. /25 Network

A `/24` can be divided into two `/25` subnets.

Original:

    192.168.1.0/24

After subnetting:

    192.168.1.0/25
    192.168.1.128/25

## First subnet

    Network:    192.168.1.0
    Hosts:      192.168.1.1 - 192.168.1.126
    Broadcast:  192.168.1.127

## Second subnet

    Network:    192.168.1.128
    Hosts:      192.168.1.129 - 192.168.1.254
    Broadcast:  192.168.1.255

Each subnet contains:

    128 total addresses
    126 traditional usable hosts

---

# 10. /26 Network

A `/24` can be divided into four `/26` subnets.

Subnet mask:

    255.255.255.192

The subnets are:

    192.168.1.0/26
    192.168.1.64/26
    192.168.1.128/26
    192.168.1.192/26

Each subnet contains:

    64 addresses
    62 traditional usable hosts

## Subnet 1

    Network:    192.168.1.0
    Hosts:      192.168.1.1 - 192.168.1.62
    Broadcast:  192.168.1.63

## Subnet 2

    Network:    192.168.1.64
    Hosts:      192.168.1.65 - 192.168.1.126
    Broadcast:  192.168.1.127

## Subnet 3

    Network:    192.168.1.128
    Hosts:      192.168.1.129 - 192.168.1.190
    Broadcast:  192.168.1.191

## Subnet 4

    Network:    192.168.1.192
    Hosts:      192.168.1.193 - 192.168.1.254
    Broadcast:  192.168.1.255

---

# 11. Block Size Method

The block-size method provides a quick way to calculate subnet ranges.

The main formula is:

    Block Size = 256 - Interesting Octet

The **interesting octet** is the octet in the subnet mask that is neither `255` nor `0`.

---

# 12. Block Size Example: /26

CIDR:

    /26

Subnet mask:

    255.255.255.192

Interesting octet:

    192

Calculate:

    Block Size = 256 - 192
               = 64

Therefore the subnet boundaries increase by 64:

    0
    64
    128
    192
    256

So the `/26` subnets are:

    192.168.10.0/26
    192.168.10.64/26
    192.168.10.128/26
    192.168.10.192/26

---

# 13. /26 Subnet Ranges Using Block Size

## Subnet 1

    Network:    192.168.10.0
    Broadcast:  192.168.10.63
    Hosts:      192.168.10.1 - 192.168.10.62

## Subnet 2

    Network:    192.168.10.64
    Broadcast:  192.168.10.127
    Hosts:      192.168.10.65 - 192.168.10.126

## Subnet 3

    Network:    192.168.10.128
    Broadcast:  192.168.10.191
    Hosts:      192.168.10.129 - 192.168.10.190

## Subnet 4

    Network:    192.168.10.192
    Broadcast:  192.168.10.255
    Hosts:      192.168.10.193 - 192.168.10.254

---

# 14. /27 Block Size

CIDR:

    /27

Subnet mask:

    255.255.255.224

Interesting octet:

    224

Block size:

    256 - 224 = 32

Subnet boundaries:

    0
    32
    64
    96
    128
    160
    192
    224
    256

Therefore:

    192.168.10.0/27
    192.168.10.32/27
    192.168.10.64/27
    192.168.10.96/27
    192.168.10.128/27
    192.168.10.160/27
    192.168.10.192/27
    192.168.10.224/27

Each subnet has:

    32 total addresses
    30 traditional usable hosts

---

# 15. /28 Block Size

CIDR:

    /28

Subnet mask:

    255.255.255.240

Interesting octet:

    240

Block size:

    256 - 240 = 16

Boundaries:

    0
    16
    32
    48
    64
    80
    96
    112
    128
    144
    160
    176
    192
    208
    224
    240
    256

Each `/28` subnet contains:

    16 total addresses
    14 traditional usable hosts

Example:

    Network:    192.168.10.64
    Broadcast:  192.168.10.79
    Hosts:      192.168.10.65 - 192.168.10.78

---

# 16. Important CIDR Cheat Sheet

| CIDR | Subnet Mask | Block Size | Total Addresses | Traditional Usable |
|------|-------------|-----------:|----------------:|-------------------:|
| /24 | 255.255.255.0 | 256 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 4 | 2 |

---

# 17. Finding Which Subnet an IP Belongs To

Example:

    IP = 192.168.10.75/26

First find the block size.

`/26`:

    Mask = 255.255.255.192

Therefore:

    Block Size = 256 - 192
               = 64

Boundaries:

    0
    64
    128
    192

The host value is:

    75

75 falls between:

    64 and 128

Therefore:

    Network = 192.168.10.64/26

The next boundary is:

    128

Therefore:

    Broadcast = 128 - 1
              = 127

Final result:

    Network:    192.168.10.64/26
    Hosts:      192.168.10.65 - 192.168.10.126
    Broadcast:  192.168.10.127

---

# 18. Another Example

Given:

    IP = 192.168.10.150/27

For `/27`:

    Mask = 255.255.255.224

Block size:

    256 - 224 = 32

Boundaries:

    0
    32
    64
    96
    128
    160
    192
    224

The host value is:

    150

150 falls between:

    128 and 160

Therefore:

    Network = 192.168.10.128/27

Broadcast:

    160 - 1 = 159

Host range:

    192.168.10.129 - 192.168.10.158

Final:

    Network:    192.168.10.128/27
    Hosts:      192.168.10.129 - 192.168.10.158
    Broadcast:  192.168.10.159

---

# 19. CIDR Prefixes That Affect Different Octets

Not every subnet uses the fourth octet.

Example:

    172.16.50.20/20

`/20` means:

    Subnet mask = 255.255.240.0

The interesting octet is:

    240

Therefore:

    Block Size = 256 - 240
               = 16

The boundaries are in the **third octet**:

    0
    16
    32
    48
    64
    80
    ...

The third octet of our IP is:

    50

50 falls between:

    48 and 64

Therefore:

    Network = 172.16.48.0/20

Broadcast:

    172.16.63.255

So:

    Network:    172.16.48.0/20
    Broadcast:  172.16.63.255

---

# 20. The Block Size Algorithm

When given an IP with CIDR:

    192.168.20.75/26

Follow these steps:

### Step 1 — Identify CIDR

    /26

### Step 2 — Find subnet mask

    255.255.255.192

### Step 3 — Find interesting octet

    192

### Step 4 — Calculate block size

    256 - 192 = 64

### Step 5 — Find boundaries

    0, 64, 128, 192

### Step 6 — Find where the IP falls

    75 is between 64 and 128

### Step 7 — Network address

    192.168.20.64

### Step 8 — Broadcast

    192.168.20.127

### Step 9 — Host range

    192.168.20.65 - 192.168.20.126

Final:

    Network:    192.168.20.64/26
    Host range: 192.168.20.65 - 192.168.20.126
    Broadcast:  192.168.20.127

---

# 21. Same Subnet vs Different Subnet

Example:

    192.168.1.10/24
    192.168.1.50/24

Both belong to:

    192.168.1.0/24

Therefore:

    Same subnet

Example:

    192.168.1.10/24
    192.168.2.10/24

They belong to:

    192.168.1.0/24
    192.168.2.0/24

Therefore:

    Different subnets

Traffic between different IP networks generally needs routing through a router/default gateway.

---

# 22. Linux Practical Commands

Install `ipcalc`:

    sudo apt install ipcalc

Calculate a network:

    ipcalc 10.189.112.123/24

Example result:

    Address:   10.189.112.123
    Netmask:   255.255.255.0 = 24
    Network:   10.189.112.0/24
    HostMin:   10.189.112.1
    HostMax:   10.189.112.254
    Broadcast: 10.189.112.255
    Hosts/Net: 254

---

# 23. Checking the Current Linux Network

Show IPv4 addresses:

    ip -4 addr

Show routing table:

    ip route

Example:

    10.189.112.0/24 dev wlp2s0

This means the Linux system knows that:

    10.189.112.0/24

is directly connected through:

    wlp2s0

---

# 24. Your Current Network Example

Your machine currently has:

    IP:       10.189.112.123/24
    Network:  10.189.112.0/24
    Gateway:  10.189.112.89
    Broadcast: 10.189.112.255

Traditional host range:

    10.189.112.1 - 10.189.112.254

Your laptop:

    10.189.112.123

belongs to:

    10.189.112.0/24

---

# 25. Important Formulas

### Host bits

    Host bits = 32 - CIDR

Example:

    /26

    32 - 26 = 6 host bits

### Total addresses

    2^(host bits)

Example:

    2^6 = 64

### Traditional usable hosts

    2^(host bits) - 2

Example:

    64 - 2 = 62

### Block size

    Block Size = 256 - Interesting Octet

Example:

    /26
    Mask = 255.255.255.192

    256 - 192 = 64

---

# 26. Key Concepts to Remember

```text
IPv4 = 32 bits

CIDR tells us how many bits are network bits.

More CIDR bits
      ↓
More network bits
      ↓
Fewer host bits
      ↓
Smaller subnet

Example:

/24 → 254 traditional usable hosts
/25 → 126
/26 → 62
/27 → 30
/28 → 14
````

The most important block-size formula:

```
BLOCK SIZE = 256 - SUBNET MASK OCTET
```

Then:

```
Network = nearest boundary below the IP

Broadcast = next boundary - 1

Host range = Network + 1 through Broadcast - 1
```

---

# 27. DevOps Relevance

Subnetting is directly connected to:

* AWS VPC subnet design
* Public and private subnets
* Route tables
* Security groups
* Network ACLs
* Docker networks
* Kubernetes networking
* Load balancers
* Database isolation
* Network troubleshooting
* Infrastructure as Code

Example cloud architecture:

```
VPC
10.0.0.0/16
    |
    +---------------------+
    |                     |
Public Subnets       Private Subnets
    |                     |
Load Balancer         Application
Web Servers           Servers
                          |
                      Database
```

```

---

# 28. Summary

Subnetting divides a large network into smaller networks.

CIDR notation defines the network prefix:

    192.168.1.0/24

IPv4 contains:

    32 bits

Host bits:

    32 - CIDR

Total addresses:

    2^(host bits)

Traditional usable hosts:

    2^(host bits) - 2

The block-size method:

    1. Find subnet mask
    2. Find interesting octet
    3. Calculate 256 - mask octet
    4. Create subnet boundaries
    5. Find where the IP falls
    6. Identify network
    7. Find broadcast
    8. Determine host range

Most important examples:

    /24 → block size 256
    /25 → block size 128
    /26 → block size 64
    /27 → block size 32
    /28 → block size 16
    /29 → block size 8
    /30 → block size 4

Subnetting is a foundational networking skill for Cloud and DevOps because cloud networks such as AWS VPCs are built around IP ranges, subnets, routing, and network security.
```
