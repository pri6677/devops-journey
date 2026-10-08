# Networking Lesson 10 — DNS (Domain Name System)

## 1. What is DNS?

**DNS (Domain Name System)** is the system that translates human-readable domain names into IP addresses.

Humans prefer:

```text
google.com
github.com
amazon.com
```

Computers communicate using IP addresses:

```text
142.250.195.14
140.82.112.3
```

DNS connects the two.

### Simple flow

```text
User
  |
  v
google.com
  |
  v
DNS Resolution
  |
  v
IP Address
  |
  v
Server
```

For example:

```text
google.com
     ↓
DNS
     ↓
142.250.x.x
     ↓
Internet connection
     ↓
Google server
```

---

# 2. Why Do We Need DNS?

Without DNS, users would need to remember IP addresses for every website.

Instead of:

```text
https://google.com
```

we would have to use something like:

```text
https://142.250.x.x
```

DNS makes network communication easier by providing a naming system.

---

# 3. Domain Name vs IP Address

### Domain name

A human-readable name:

```text
google.com
github.com
example.com
```

### IP address

An address used by the network:

```text
142.250.x.x
140.82.x.x
93.184.x.x
```

DNS performs the lookup:

```text
Domain Name → IP Address
```

---

# 4. DNS Resolution

DNS resolution is the process of finding the IP address associated with a domain name.

Example:

```text
google.com
     |
     v
DNS Resolver
     |
     v
IP Address
     |
     v
Connection to Google
```

When an application needs to connect to:

```text
google.com
```

the system first needs to determine the IP address.

---

# 5. DNS in Linux

Linux systems have several tools and configuration files related to DNS.

Important commands:

```bash
cat /etc/resolv.conf
```

```bash
resolvectl status
```

```bash
getent hosts google.com
```

```bash
nslookup google.com
```

```bash
dig google.com
```

---

# 6. /etc/resolv.conf

The traditional Linux DNS configuration file is:

```text
/etc/resolv.conf
```

Check it using:

```bash
cat /etc/resolv.conf
```

Our system showed:

```text
nameserver 127.0.0.53
options edns0 trust-ad
search .
```

An important point:

```text
127.0.0.53
```

is the local **systemd-resolved DNS stub resolver**.

It is not the actual upstream DNS server.

---

# 7. systemd-resolved

Our system uses:

```text
systemd-resolved
```

as the local DNS resolver service.

The local application can send DNS queries to:

```text
127.0.0.53
```

Then `systemd-resolved` communicates with the configured upstream DNS server.

Our DNS flow was:

```text
Application
     |
     v
127.0.0.53
(systemd-resolved stub)
     |
     v
192.168.0.1
(upstream DNS server)
     |
     v
DNS response
```

---

# 8. Our Actual DNS Configuration

We checked:

```bash
resolvectl status
```

Our Wi-Fi interface was:

```text
wlp2s0
```

The important DNS information was:

```text
Link 3 (wlp2s0):
    Current Scopes: DNS
    +DefaultRoute
    Current DNS Server: 192.168.0.1
    DNS Servers: 192.168.0.1
```

This means our Wi-Fi connection uses:

```text
192.168.0.1
```

as the upstream DNS server.

The local DNS stub is:

```text
127.0.0.53
```

Therefore:

```text
Application
    ↓
127.0.0.53
    ↓
systemd-resolved
    ↓
192.168.0.1
    ↓
DNS response
```

---

# 9. DNS Resolver

A DNS resolver is responsible for obtaining DNS answers for clients.

There are different roles involved in DNS.

### Client

The application or system requesting a DNS lookup.

Example:

```text
Your browser
```

### Recursive Resolver

The resolver that performs DNS lookups on behalf of the client.

Example in our system:

```text
systemd-resolved
```

which uses the configured upstream DNS server.

### Authoritative DNS Server

A server that has authoritative information about a domain.

For example, Google's authoritative DNS servers include:

```text
ns1.google.com
ns2.google.com
ns3.google.com
ns4.google.com
```

---

# 10. DNS Hierarchy

DNS is hierarchical.

A simplified structure is:

```text
                         .
                         |
                  Root DNS Servers
                         |
             +-----------+-----------+
             |                       |
            .com                    .org
             |                       |
          google.com             example.org
             |
      Authoritative DNS
```

The hierarchy contains:

```text
Root
  ↓
TLD
  ↓
Authoritative DNS
  ↓
Domain
```

---

# 11. Root DNS Servers

At the top of the DNS hierarchy is:

```text
.
```

This is called the **root**.

Root DNS servers help direct queries toward the appropriate Top-Level Domain servers.

Examples of TLDs:

```text
.com
.org
.net
.in
```

---

# 12. TLD Servers

TLD means:

**Top-Level Domain**

Examples:

```text
.com
.org
.net
.in
.edu
```

For:

```text
google.com
```

the TLD is:

```text
.com
```

The DNS hierarchy can therefore be represented as:

```text
Root
 |
 +-- .com
       |
       +-- google.com
```

---

# 13. Authoritative DNS Server

An authoritative DNS server contains DNS information for a domain.

For Google, our `dig google.com MX` output showed authoritative name servers such as:

```text
ns1.google.com
ns2.google.com
ns3.google.com
ns4.google.com
```

These servers are authoritative for Google's DNS information.

---

# 14. Recursive DNS Lookup

A simplified recursive lookup looks like this:

```text
Client
  |
  v
Recursive Resolver
  |
  v
Root DNS
  |
  v
TLD DNS
  |
  v
Authoritative DNS
  |
  v
IP / DNS Record
  |
  v
Recursive Resolver
  |
  v
Client
```

The client normally does not communicate directly with every DNS server in the hierarchy.

The resolver performs the lookup.

---

# 15. DNS Record Types

DNS stores different types of information called **DNS records**.

Important record types:

```text
A
AAAA
CNAME
MX
NS
TXT
PTR
SRV
SOA
```

---

# 16. A Record

An **A record** maps a domain name to an IPv4 address.

Example:

```text
google.com → IPv4 address
```

Query:

```bash
dig google.com A
```

Example structure:

```text
google.com.    IN    A    142.250.x.x
```

Meaning:

```text
A = IPv4 address
```

---

# 17. AAAA Record

An **AAAA record** maps a domain name to an IPv6 address.

Example:

```text
google.com → IPv6 address
```

Query:

```bash
dig google.com AAAA
```

Example IPv6 address:

```text
2404:6800:4013:807::8b
```

Important:

DNS resolution succeeding does **not** automatically mean that IPv6 connectivity is working.

A system may successfully resolve an IPv6 address but still have no usable IPv6 route.

---

# 18. CNAME Record

CNAME means:

**Canonical Name**

It creates an alias for another domain name.

Conceptually:

```text
www.example.com
       |
       v
example.com
```

A CNAME points to another hostname rather than directly providing an IP address.

---

# 19. MX Record

MX means:

**Mail Exchange**

MX records specify mail servers responsible for receiving email for a domain.

We tested:

```bash
dig google.com MX
```

Our result included:

```text
google.com. 1800 IN MX 10 smtp.google.com.
```

This means the domain has a mail-exchange record pointing to:

```text
smtp.google.com
```

The number:

```text
10
```

is the mail server priority.

Lower values generally have higher priority.

---

# 20. NS Record

NS means:

**Name Server**

NS records identify authoritative DNS servers for a domain.

We saw:

```text
ns1.google.com
ns2.google.com
ns3.google.com
ns4.google.com
```

Query:

```bash
dig google.com NS
```

---

# 21. TXT Record

TXT records store text information associated with a domain.

They are commonly used for things such as:

```text
Domain verification
Email authentication
SPF information
Other domain-related metadata
```

Query:

```bash
dig google.com TXT
```

---

# 22. PTR Record

PTR means:

**Pointer Record**

PTR records are commonly used for reverse DNS.

Normal DNS:

```text
Domain → IP
```

Reverse DNS:

```text
IP → Domain
```

Example:

```bash
dig -x 8.8.8.8
```

Our result returned:

```text
dns.google.
```

Therefore:

```text
8.8.8.8
   ↓
dns.google
```

---

# 23. Reverse DNS

Reverse DNS uses special DNS zones.

For IPv4, reverse DNS uses:

```text
in-addr.arpa
```

For example:

```text
8.8.8.8
```

becomes:

```text
8.8.8.8.in-addr.arpa
```

Command:

```bash
dig -x 8.8.8.8
```

---

# 24. SOA Record

SOA means:

**Start of Authority**

It contains important administrative information about a DNS zone.

A SOA record can contain information such as:

```text
Primary name server
Responsible administrator
Serial number
Refresh
Retry
Expire
Minimum TTL
```

Query:

```bash
dig google.com SOA
```

---

# 25. SRV Record

SRV records are used to describe services.

They can provide information such as:

```text
Service
Protocol
Port
Target server
Priority
Weight
```

Example:

```text
_service._tcp.example.com
```

SRV records are useful for service discovery.

---

# 26. TTL

TTL means:

**Time To Live**

DNS records have a TTL value.

Example:

```text
1800
```

means the record can be cached for a specified period, measured in seconds.

Caching reduces repeated DNS queries.

General idea:

```text
First lookup
     ↓
DNS server
     ↓
Answer
     ↓
Cache
     ↓
Future lookup may use cached answer
```

---

# 27. DNS Caching

DNS responses can be cached by:

```text
Operating system
Browser
Local DNS resolver
Network DNS server
```

Caching improves:

* Performance
* Response time
* DNS server efficiency
* Network efficiency

But cached records remain valid only according to their TTL.

---

# 28. UDP and TCP Port 53

DNS commonly uses:

```text
UDP port 53
```

DNS can also use:

```text
TCP port 53
```

Traditional/simple DNS queries commonly use UDP.

TCP may be used when required, such as for larger DNS responses or certain DNS operations.

---

# 29. `getent hosts`

Command:

```bash
getent hosts google.com
```

This asks the system's configured name-service mechanism to resolve the hostname.

Our system returned IPv6 addresses such as:

```text
2404:6800:4013:807::8b
2404:6800:4013:802::66
2404:6800:4013:807::65
```

This demonstrated that DNS resolution can return IPv6 addresses.

Important:

```text
DNS resolution ≠ network connectivity
```

A hostname can resolve successfully even if the machine cannot currently reach the returned address.

---

# 30. `dig`

`dig` is one of the most useful DNS troubleshooting tools on Linux.

Basic command:

```bash
dig google.com
```

It provides detailed DNS information.

Our query showed:

```text
status: NOERROR
```

This means the DNS query completed successfully.

It also showed:

```text
SERVER: 127.0.0.53#53
```

This confirms that the query was sent to the local systemd-resolved stub.

---

# 31. `dig +short`

For a cleaner answer:

```bash
dig +short google.com
```

This returns only the useful DNS answer.

Our system returned multiple IPv4 addresses.

Example format:

```text
142.250.x.x
142.250.x.x
142.250.x.x
```

This is useful when you only want the resolved IP addresses.

---

# 32. Query Specific DNS Records

### A record

```bash
dig google.com A
```

### AAAA record

```bash
dig google.com AAAA
```

### MX record

```bash
dig google.com MX
```

### NS record

```bash
dig google.com NS
```

### TXT record

```bash
dig google.com TXT
```

### SOA record

```bash
dig google.com SOA
```

### Reverse lookup

```bash
dig -x 8.8.8.8
```

---

# 33. `nslookup`

Another DNS troubleshooting command:

```bash
nslookup google.com
```

It can be used to perform basic DNS lookups.

However, for detailed DNS troubleshooting, `dig` generally provides more useful information.

---

# 34. `resolvectl`

`resolvectl` is useful when working with `systemd-resolved`.

Check DNS configuration:

```bash
resolvectl status
```

Query a hostname:

```bash
resolvectl query google.com
```

This can help determine which DNS server/interface is being used.

---

# 35. DNS Troubleshooting

When a website or service cannot be reached, DNS should be checked separately from network connectivity.

A useful troubleshooting sequence is:

```text
1. Check DNS configuration
        ↓
2. Test DNS resolution
        ↓
3. Check routing
        ↓
4. Check connectivity
        ↓
5. Check application/service
```

---

# 36. Useful DNS Troubleshooting Commands

### Check resolver configuration

```bash
cat /etc/resolv.conf
```

### Check systemd-resolved

```bash
resolvectl status
```

### Resolve using system configuration

```bash
getent hosts google.com
```

### Basic DNS lookup

```bash
nslookup google.com
```

### Detailed DNS lookup

```bash
dig google.com
```

### Only IP addresses

```bash
dig +short google.com
```

### Check IPv4

```bash
dig google.com A
```

### Check IPv6

```bash
dig google.com AAAA
```

### Reverse lookup

```bash
dig -x 8.8.8.8
```

---

# 37. DNS Failure vs Network Failure

This distinction is extremely important for DevOps troubleshooting.

### Case 1 — DNS works, network fails

```text
google.com
     ↓
DNS
     ↓
IP address
     ↓
Connection fails
```

DNS is working.

The problem may be:

```text
Routing
Firewall
Gateway
Network interface
Internet connectivity
```

---

### Case 2 — DNS fails

```text
google.com
     ↓
DNS lookup fails
     ↓
No IP address
```

The problem may involve:

```text
DNS server
/etc/resolv.conf
systemd-resolved
Network configuration
Upstream DNS
```

---

# 38. Important DevOps Concept

DNS is involved in many DevOps systems.

Examples:

```text
Browser
   ↓
DNS
   ↓
Load Balancer
   ↓
Application
```

Cloud architecture:

```text
User
 ↓
DNS
 ↓
Load Balancer
 ↓
Web Server
 ↓
Application
 ↓
Database
```

Containers and Kubernetes also depend heavily on DNS for service discovery.

---

# 39. DNS + Routing

DNS and routing perform different jobs.

### DNS

Answers:

> "What IP address belongs to this hostname?"

```text
google.com
     ↓
IP address
```

### Routing

Answers:

> "How should I reach that IP address?"

```text
Destination IP
     ↓
Routing table
     ↓
Interface / Gateway
```

Together:

```text
google.com
    ↓
DNS
    ↓
142.250.x.x
    ↓
Routing table
    ↓
Gateway
    ↓
Network
    ↓
Destination
```

---

# 40. DNS + ARP

For a local IPv4 network, the complete process can involve DNS and ARP.

Example:

```text
google.com
    |
    v
DNS resolution
    |
    v
Google IP
    |
    v
Routing table
    |
    v
Default gateway
    |
    v
ARP
    |
    v
Gateway MAC address
    |
    v
Ethernet/Wi-Fi frame
    |
    v
Router
    |
    v
Internet
```

This shows how the networking concepts learned so far connect together.

---

# 41. Our DNS Lab

## Step 1 — Check `/etc/resolv.conf`

```bash
cat /etc/resolv.conf
```

Important output:

```text
nameserver 127.0.0.53
```

Conclusion:

```text
Local DNS stub = 127.0.0.53
```

---

## Step 2 — Check DNS configuration

```bash
resolvectl status
```

Our Wi-Fi interface:

```text
wlp2s0
```

Upstream DNS:

```text
192.168.0.1
```

Therefore:

```text
Application
     ↓
127.0.0.53
     ↓
192.168.0.1
```

---

## Step 3 — Resolve hostname

```bash
getent hosts google.com
```

The system returned multiple IPv6 addresses.

Conclusion:

```text
DNS resolution is working.
```

---

## Step 4 — Use `dig`

```bash
dig google.com
```

Result:

```text
status: NOERROR
```

The DNS server shown was:

```text
127.0.0.53#53
```

Conclusion:

```text
The local DNS resolver successfully handled the query.
```

---

## Step 5 — Get only addresses

```bash
dig +short google.com
```

This returned multiple IPv4 addresses.

---

## Step 6 — Check MX

```bash
dig google.com MX
```

We found:

```text
google.com. 1800 IN MX 10 smtp.google.com.
```

This demonstrated how DNS can store email-server information.

---

## Step 7 — Reverse DNS

```bash
dig -x 8.8.8.8
```

Result included:

```text
dns.google.
```

Therefore:

```text
8.8.8.8 → dns.google
```

---

# 42. DNS Troubleshooting Flow for DevOps

When a service hostname is not working:

```text
                 Application
                      |
                      v
              Does hostname resolve?
                    /   \
                  NO     YES
                  |       |
                  v       v
             Check DNS   Check route
                  |       |
                  |       v
                  |   Check gateway
                  |       |
                  |       v
                  |   Check connectivity
                  |       |
                  +-------+
                          |
                          v
                    Check service
```

Useful commands:

```bash
getent hosts example.com
```

```bash
dig example.com
```

```bash
resolvectl status
```

```bash
ip route
```

```bash
ip route get <IP>
```

```bash
ping <IP>
```

---

# 43. Common DNS Mistakes

### Mistake 1 — Assuming `/etc/resolv.conf` shows the real DNS server

If you see:

```text
nameserver 127.0.0.53
```

that is the local systemd-resolved stub.

Check:

```bash
resolvectl status
```

to find the upstream DNS server.

---

### Mistake 2 — Assuming DNS success means Internet connectivity

This is wrong:

```text
DNS works
    ≠
Internet works
```

DNS and network connectivity are separate layers of troubleshooting.

---

### Mistake 3 — Confusing DNS with routing

DNS determines:

```text
Hostname → IP
```

Routing determines:

```text
How to reach IP
```

---

### Mistake 4 — Using only `ping` to troubleshoot DNS

`ping` tests connectivity to an IP/hostname, but it is not a complete DNS troubleshooting tool.

Use:

```bash
dig
resolvectl
getent
```

for DNS-specific investigation.

---

# 44. Important Commands Cheat Sheet

| Command                       | Purpose                                     |
| ----------------------------- | ------------------------------------------- |
| `cat /etc/resolv.conf`        | View resolver configuration                 |
| `resolvectl status`           | View DNS configuration                      |
| `resolvectl query google.com` | Query hostname                              |
| `getent hosts google.com`     | Resolve hostname using system configuration |
| `nslookup google.com`         | Basic DNS lookup                            |
| `dig google.com`              | Detailed DNS lookup                         |
| `dig +short google.com`       | Show concise DNS answer                     |
| `dig google.com A`            | Query IPv4                                  |
| `dig google.com AAAA`         | Query IPv6                                  |
| `dig google.com MX`           | Query mail servers                          |
| `dig google.com NS`           | Query name servers                          |
| `dig google.com TXT`          | Query TXT records                           |
| `dig google.com SOA`          | Query SOA record                            |
| `dig -x 8.8.8.8`              | Reverse DNS lookup                          |

---

# 45. Key Differences

| Concept    | Purpose                                      |
| ---------- | -------------------------------------------- |
| DNS        | Name → IP                                    |
| Routing    | Selects path to destination                  |
| ARP        | IPv4 → MAC on local network                  |
| Ethernet   | Local network frame delivery                 |
| DHCP       | Automatically provides network configuration |
| TCP        | Reliable transport                           |
| UDP        | Connectionless transport                     |
| HTTP/HTTPS | Web communication                            |
| ICMP       | Network diagnostics/control                  |

---

# 46. Complete Networking Flow

The concepts we have learned can now connect together.

Suppose we run:

```bash
curl https://example.com
```

A simplified process is:

```text
1. Application
       |
       v
2. DNS
       |
       v
3. Domain → IP address
       |
       v
4. Routing table
       |
       v
5. Determine next hop
       |
       v
6. ARP resolves gateway MAC
       |
       v
7. Ethernet/Wi-Fi frame
       |
       v
8. Router
       |
       v
9. Internet
       |
       v
10. Destination server
```

This is one of the most important mental models for Cloud and DevOps troubleshooting.

---

# 47. What I Learned in This Lesson

After completing this lesson, I should understand:

* What DNS is
* Why DNS is needed
* Domain names vs IP addresses
* DNS resolution
* Recursive DNS
* Authoritative DNS
* DNS hierarchy
* Root DNS
* TLD DNS
* DNS records
* A records
* AAAA records
* CNAME records
* MX records
* NS records
* TXT records
* PTR records
* SOA records
* SRV records
* TTL
* DNS caching
* UDP/TCP port 53
* `/etc/resolv.conf`
* `systemd-resolved`
* `resolvectl`
* `getent`
* `nslookup`
* `dig`
* Reverse DNS
* DNS troubleshooting
* DNS vs routing
* DNS vs network connectivity
* How DNS connects with routing and ARP

---

# 48. Final Mental Model

Remember this:

```text
              DNS
               |
       "What IP is this?"
               |
               v
        google.com
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
       Ethernet / Wi-Fi
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

### Most important rule:

```text
DNS = Name → IP
Routing = Path to IP
ARP = IP → MAC (local IPv4 network)
```

These three concepts work together constantly in Linux, Cloud, and DevOps environments.
