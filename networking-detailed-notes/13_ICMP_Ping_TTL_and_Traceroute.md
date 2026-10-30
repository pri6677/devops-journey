# Networking for DevOps — Lecture 13
# ICMP, Ping, TTL, and Traceroute

**Roadmap position:** Networking → Lecture 13  
**Previous lecture:** Lecture 12 — Routing, Switches vs. Routers, and How Packets Travel

In this lesson, we'll learn how computers test network connectivity, how routers report certain network problems, and how to discover the route packets take through a network.

We'll cover five main concepts:

1. **ICMP** — how network devices report errors and diagnostic information.
2. **Ping** — how to test connectivity and measure round-trip time.
3. **TTL** — how IP packets avoid circulating indefinitely.
4. **Traceroute** — how to discover intermediate network hops.
5. **Traceroute asterisks (`* * *`)** — why some routers don't appear in the results.

These are particularly useful for DevOps engineers troubleshooting Linux servers, cloud instances, Docker networking, and connectivity problems.

---

# 1. What Is ICMP?

**ICMP stands for Internet Control Message Protocol.**

It is a network-layer protocol used to communicate diagnostic information and report certain problems encountered during IP packet delivery.

Think of IP as the system responsible for addressing and forwarding packets. Sometimes, however, a packet cannot be delivered as expected. Network devices may need a way to report what happened.

That's one of ICMP's purposes.

## What can ICMP report?

Examples include:

| ICMP message | Meaning |
|---|---|
| Echo Request | A device is being asked to respond to a connectivity test |
| Echo Reply | A response to an Echo Request |
| Destination Unreachable | A destination or part of the delivery path is unreachable for a particular reason |
| Time Exceeded | A packet's TTL expired before it reached its destination |
| Parameter Problem | A problem was found in an IP header |

An ICMP message is carried inside an IP packet.

For example:

```text
IP Packet
┌───────────────────────────────┐
│ IP Header                     │
│ Source IP                     │
│ Destination IP                │
├───────────────────────────────┤
│ ICMP Message                  │
│ Type                          │
│ Code                          │
│ Additional information        │
└───────────────────────────────┘
```

This is a simplified representation. Actual ICMP messages have protocol-specific fields.

## Does ICMP use port numbers?

**No. ICMP does not use TCP or UDP port numbers.**

Compare the protocols:

| Protocol | Uses port numbers? | Main purpose |
|---|---|---|
| TCP | Yes | Reliable, ordered transport |
| UDP | Yes | Datagram transport |
| ICMP | No | Network diagnostics and error reporting |

TCP and UDP use port numbers to identify transport endpoints. ICMP instead uses fields such as its **Type** and **Code** to identify the kind of message.

For example, ICMPv4 Echo Request uses Type 8, and Echo Reply uses Type 0.

### Important distinction

ICMP is associated with OSI Layer 3 because it supports IP-level diagnostics and error reporting. However, it is not a replacement for IP; ICMP messages are carried inside IP packets.

**Remember:** ICMP helps network devices report certain conditions and supports tools such as `ping` and `traceroute`.

---

# 2. How Does `ping` Work Internally?

The `ping` utility tests whether a destination responds to ICMP Echo Requests and measures the time taken for replies to return.

For example, on your Zorin OS terminal:

```bash
ping google.com
```

You might see output resembling:

```text
PING google.com (142.250.x.x) 56(84) bytes of data.
64 bytes from ...: icmp_seq=1 ttl=117 time=18.4 ms
64 bytes from ...: icmp_seq=2 ttl=117 time=17.9 ms
64 bytes from ...: icmp_seq=3 ttl=117 time=18.1 ms
```

These addresses and values are illustrative; your actual results will differ.

Let's understand what happens internally.

## Step 1: DNS resolves the hostname

You typed:

```bash
ping google.com
```

But the network needs an IP address to send the packet to.

Your computer therefore uses DNS resolution to obtain an IP address for `google.com`.

For example:

```text
google.com
    |
    | DNS resolution
    v
142.250.x.x
```

The actual address depends on DNS responses and your network.

**Important:** DNS and ICMP are different. DNS helps resolve the name; ICMP carries the Echo Request and Echo Reply used by `ping`.

## Step 2: Your computer sends an ICMP Echo Request

Your computer creates an ICMP Echo Request and sends it inside an IP packet towards the destination.

Conceptually:

```text
Your Laptop
    |
    | ICMP Echo Request
    v
Home Router
    |
    v
Internet Routers
    |
    v
Destination
```

The IP packet includes source and destination IP addresses. Its payload contains the ICMP message.

## Step 3: The destination responds

If the destination receives the Echo Request and is configured to respond, it sends an ICMP Echo Reply.

```text
Your Laptop                         Destination
     |                                    |
     |------- Echo Request -------------->|
     |                                    |
     |<------ Echo Reply -----------------|
     |                                    |
```

The reply travels back through a suitable return path. That path does not necessarily follow exactly the same routers as the outbound path.

## Step 4: Ping calculates Round-Trip Time

**RTT stands for Round-Trip Time.**

It measures the elapsed time between sending a request and receiving its reply.

For example:

```text
time=18.4 ms
```

This means the measured round trip took approximately 18.4 milliseconds.

RTT can be affected by:
- Distance between endpoints.
- Network congestion.
- Router processing and queuing.
- Wi-Fi conditions.
- The destination's response behavior.
- The return path.

### Does ping measure only network latency?

Not perfectly. It measures the round-trip time for that particular probe and response, which can include network delays and processing delays.

It is not a direct measurement of the time a typical HTTP request takes to complete.

## Step 5: Ping reports packet statistics

Run:

```bash
ping -c 4 google.com
```

The `-c 4` option tells `ping` to send four requests and then stop.

At the end, you might see statistics such as:

```text
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = ...
```

This reports the number of packets transmitted and received, packet loss, and timing statistics.

### What if ping fails?

For example:

```text
100% packet loss
```

This does **not** automatically prove that the server is down.

Possible explanations include:

- The destination is offline.
- The route to the destination is unavailable.
- A firewall blocks ICMP Echo Requests or Replies.
- The destination deliberately ignores ping.
- A network device filters ICMP traffic.
- A return-path problem prevents the reply from reaching you.

**DevOps lesson:** Ping is useful for diagnosing connectivity, but it is not a complete test of whether an application is working.

For example, a server may block ping while continuing to serve HTTPS requests.

---

# 3. TTL — Time to Live

TTL is one of the most important concepts in this lecture because it explains how routers prevent packets from circulating indefinitely.

**TTL stands for Time to Live**, although for IPv4 it functions as a hop-count limit in practice.

An IPv4 packet contains a TTL field in its IP header.

## Why does TTL exist?

Imagine a routing problem causes two routers to forward a packet to each other repeatedly.

```text
Router A ──────> Router B
    ^                |
    |                |
    +----------------+
```

Without a mechanism to limit the packet's lifetime, that packet could keep circulating in a routing loop, consuming network resources.

TTL helps prevent this.

## How does TTL work?

When an IPv4 packet is forwarded by a router, the router decreases its TTL by at least one.

For ordinary forwarding, it is decreased by one.

Suppose a packet starts with:

```text
TTL = 5
```

As it travels through routers:

| Stage | TTL |
|---|---:|
| Sent by source | 5 |
| After Router 1 | 4 |
| After Router 2 | 3 |
| After Router 3 | 2 |
| After Router 4 | 1 |
| Next router attempts forwarding | Expires |

When a router cannot forward the packet because its TTL would expire, it discards the packet and will ordinarily send an ICMP Time Exceeded message, subject to ICMP error-generation rules and network policy.

This prevents the packet from continuing indefinitely.

### Does TTL measure time in seconds?

No—not in the way its name might suggest.

For IPv4, TTL is effectively a **hop limit**. Routers decrease it during forwarding.

IPv6 uses a similar field called **Hop Limit**.

---

# 4. Practical Lab — Set TTL to 1

Your lecture describes forcing a packet's TTL to expire at the first router.

On Linux, use the `-t` option with `ping` to set the IPv4 TTL.

Run:

```bash
ping -4 -t 1 -c 4 8.8.8.8
```

Let's understand each part:

| Option | Meaning |
|---|---|
| `ping` | Sends ICMP Echo Requests |
| `-4` | Uses IPv4 |
| `-t 1` | Sets the outgoing IPv4 TTL to 1 |
| `-c 4` | Sends four requests |

If the destination is reached through a router, that router will normally decrement the TTL to zero and discard the packet, potentially returning an ICMP Time Exceeded message.

Your output may resemble:

```text
From 192.168.1.1 icmp_seq=1 Time to live exceeded
```

The address is an illustrative example. Your actual gateway address may differ, and your router may not send an ICMP response.

## Important correction about the command in the lecture

Your lecture mentions:

```bash
ping -m 1 google.com
```

On typical Linux versions of `ping`, **`-m` sets a packet mark, not the TTL**.

Therefore, to test IPv4 TTL expiration on your Zorin OS machine, use:

```bash
ping -4 -t 1 -c 4 google.com
```

If you want to use Google's hostname rather than a numeric IP, DNS resolution must still work before the destination can be contacted.

### Why might you not see a TTL Exceeded response?

Possible reasons include:

- Your router filters ICMP error messages.
- The network drops the packet without sending a response.
- A firewall or network policy prevents the message from reaching you.
- The selected route or network environment behaves differently than expected.

The absence of an ICMP response does not necessarily mean the TTL mechanism failed.

---

# 5. What Is Traceroute?

`traceroute` is a diagnostic utility that attempts to discover the routers, or hops, along a path towards a destination.

For example:

```bash
traceroute google.com
```

The output may resemble:

```text
traceroute to google.com (...), 30 hops max
 1  192.168.1.1       2.1 ms   1.8 ms   2.0 ms
 2  10.20.0.1         8.3 ms   7.9 ms   8.1 ms
 3  203.0.113.10     14.4 ms  14.1 ms  14.7 ms
 4  ...
```

These are illustrative addresses and times. Actual output will differ.

Each numbered line represents a hop discovered by the probe method used by `traceroute`.

The utility typically sends multiple probes for each hop and measures their round-trip times.

## How does traceroute discover the hops?

It exploits the TTL mechanism you just learned.

Instead of sending every probe with the same TTL, traceroute increases the TTL gradually.

### Probe 1: TTL = 1

```text
Your Laptop
    |
    | Probe with TTL 1
    v
Router 1
    |
    X TTL expires
```

The first router cannot forward the packet because its TTL expires.

It may send an ICMP Time Exceeded response to your laptop.

Your laptop learns the source address of the responding router.

That becomes the first discovered hop.

### Probe 2: TTL = 2

```text
Your Laptop
    |
    v
Router 1
    |
    | TTL now 1
    v
Router 2
    |
    X TTL expires
```

The second router may send an ICMP Time Exceeded response.

Traceroute records the responding router as the second hop.

### Probe 3: TTL = 3

```text
Your Laptop
    |
    v
Router 1
    |
    v
Router 2
    |
    v
Router 3
    |
    X TTL expires
```

The third router may respond, allowing traceroute to discover another hop.

The process continues until the destination responds, a stopping condition is reached, or the configured hop limit is exhausted.

## Traceroute in one diagram



```text
TTL = 1  → Router 1 responds
TTL = 2  → Router 2 responds
TTL = 3  → Router 3 responds
TTL = 4  → Router 4 responds
TTL = 5  → Destination may be reached
```

This is the basic idea behind traditional TTL-based traceroute.

---

# 6. How Traceroute Works Internally

There is an important technical detail: **not every traceroute implementation sends the same type of probe**.

On Linux, the traditional `traceroute` command commonly uses UDP probes by default. Other modes can use ICMP Echo Requests or TCP probes.

Regardless of the probe method, the classic TTL-based technique works by increasing the TTL and observing the responses.

## Traditional Linux traceroute

With the default UDP method, the process is broadly:

1. Send a UDP probe with TTL 1.
2. A router lets the TTL expire and may return ICMP Time Exceeded.
3. Increase TTL to 2 and send another probe.
4. Repeat for successive hops.
5. When the probe reaches the destination, the destination may return an ICMP Destination Unreachable message indicating that the UDP destination port is unreachable. Traceroute interprets this as reaching the destination.

The exact response depends on the probe method and destination behavior.

## ICMP-based traceroute

Some implementations send ICMP Echo Request probes instead.

A command commonly supported by Linux's `traceroute` is:

```bash
traceroute -I google.com
```

The `-I` option selects ICMP Echo probes.

The destination may respond with an ICMP Echo Reply when the probe reaches it, assuming the destination and network permit the response.

## TCP-based traceroute

A TCP-based method sends TCP probes, often directed at a selected destination port.

This can be useful when UDP or ICMP probes are filtered but TCP traffic is permitted.

Availability and command options depend on the installed implementation.

### Check which traceroute command you have

On Zorin OS, run:

```bash
command -v traceroute
```

If it is installed, you can inspect its supported options:

```bash
traceroute --help
```

If the command is missing, you may use:

```bash
tracepath google.com
```

`tracepath` is another Linux diagnostic tool that can reveal information about the path to a destination.

**Key takeaway:** Traceroute does not simply ask every router for its identity. It sends carefully constructed probes and infers the path from the responses it receives.

---

# 7. Understanding `* * *` in Traceroute

This is one of the most useful things to understand when troubleshooting real networks.

Consider this output:

```text
traceroute to example.com, 30 hops max
 1  192.168.1.1      2.0 ms   1.8 ms   2.1 ms
 2  10.20.0.1        8.4 ms   8.2 ms   8.7 ms
 3  * * *
 4  203.0.113.20     15.1 ms  15.4 ms  15.2 ms
```

The third hop shows:

```text
* * *
```

What does it mean?

**It means traceroute did not receive a response for those probes within its timeout.**

It does not automatically mean that the router is broken.

## Why might a hop show asterisks?

### Reason 1: The router does not send ICMP responses

Some routers are configured not to generate ICMP Time Exceeded messages for these probes.

They may still forward ordinary traffic correctly.

### Reason 2: A firewall filters the probes or responses

A firewall may discard the traceroute probes or the corresponding ICMP replies.

### Reason 3: Rate limiting

Some routers limit the rate at which they generate diagnostic responses.

If too many probes arrive, some responses may be suppressed.

### Reason 4: The response takes too long

Traceroute waits for a configured period. If a response arrives after that period, the tool may display an asterisk for that probe.

### Reason 5: The return path is blocked

A router may generate a response, but the response might not successfully reach your laptop.

## What if later hops respond?

Suppose you see:

```text
1  192.168.1.1
2  10.20.0.1
3  * * *
4  203.0.113.20
5  destination.example
```

This tells you that traceroute received no responses for the third-hop probes, but it received responses from later hops.

That is strong evidence that the missing response at hop 3 **does not, by itself, prove the forwarding path is broken**.

The router may be forwarding traffic normally while declining to respond to the diagnostic probes.

## What if every hop after a point shows asterisks?

For example:

```text
1  192.168.1.1
2  10.20.0.1
3  * * *
4  * * *
5  * * *
```

This gives you less information.

Possible explanations include:
- A routing problem.
- A firewall blocking traffic.
- A network segment that filters traceroute probes.
- A destination that cannot be reached.
- A return-path problem.
- Diagnostic response filtering.

You need additional tests before deciding which explanation is correct.

**DevOps lesson:** Asterisks indicate missing traceroute responses, not necessarily missing packet forwarding.

---

# 8. Hands-On Lab: Ping and Traceroute on Zorin OS

Let's practise the commands.

## Lab 1: Ping a public IP address

```bash
ping -c 4 8.8.8.8
```

This sends four ICMP Echo Requests to Google's public DNS address.

Observe:
- Whether replies arrive.
- The round-trip time.
- Packet loss.

If it fails, remember that ICMP may be blocked even when other traffic works.

## Lab 2: Ping a hostname

```bash
ping -c 4 google.com
```

Compare the output with Lab 1.

The hostname test also depends on name resolution. If it fails while the numeric-IP test succeeds, DNS is one area worth investigating.

## Lab 3: Test a TTL of 1

```bash
ping -4 -t 1 -c 4 8.8.8.8
```

Observe whether your gateway or another network device responds with a TTL-expired message.

Your router may not send one.

## Lab 4: Trace the route

If `traceroute` is installed:

```bash
traceroute google.com
```

Observe:
- Hop numbers.
- Responding IP addresses or hostnames.
- Round-trip times.
- Asterisks.

If the command is not available, check:

```bash
command -v tracepath
```

Then try:

```bash
tracepath google.com
```

## Lab 5: Try ICMP-based traceroute

If your installed `traceroute` supports it:

```bash
traceroute -I google.com
```

Compare the output with the default method.

Different probe types may produce different results because networks handle UDP, ICMP, and TCP traffic differently.

## Lab 6: Compare network reachability and application reachability

Run:

```bash
ping -c 4 example.com
```

Then:

```bash
curl -I --connect-timeout 10 https://example.com
```

The first command tests ICMP Echo communication.

The second attempts an HTTPS request and may test DNS, TCP connectivity, TLS negotiation, and HTTP response behavior.

If ping fails but curl succeeds, ICMP may be filtered while HTTPS is allowed.

If ping succeeds but curl fails, investigate the application connection path, TLS, DNS behavior, and service availability rather than assuming the whole network is broken.

---

# 9. DevOps Troubleshooting Scenarios

Let's apply the lesson to realistic situations.

## Scenario A: Your EC2 instance does not respond to ping

You run:

```bash
ping -c 4 <EC2_PUBLIC_IP>
```

But receive no replies.

Does that prove the EC2 instance is down?

**No.**

Investigate:
1. Is the instance running?
2. Does it have the expected public IPv4 address?
3. Is the route to the instance configured correctly?
4. Do the security group and network ACL permit the relevant traffic?
5. Is the operating system configured to respond to ICMP Echo Requests?
6. Can you connect using the actual application protocol, such as SSH?

For example, if you are testing SSH, check the connection directly:

```bash
ssh -v -i aws-demo.pem ec2-user@<EC2_PUBLIC_IP>
```

Use the correct key, username, and destination for your instance.

The `-v` option enables verbose output, which helps show where the SSH connection is failing.

An EC2 instance may be reachable over SSH even if ICMP Echo Requests are blocked.

## Scenario B: Traceroute stops at the first router

Suppose:

```text
1  192.168.1.1
2  * * *
3  * * *
4  * * *
```

Possible explanations include filtering, rate limiting, or a routing problem.

Next, try an application-level test:

```bash
curl -I --connect-timeout 10 https://example.com
```

If HTTPS succeeds, the missing traceroute responses may be a diagnostic filtering issue rather than a general connectivity failure.

## Scenario C: Ping works, but the application does not

Suppose:

```bash
ping -c 4 10.0.1.10
```

succeeds, but connecting to the application fails.

This can happen because ICMP reachability does not prove that a particular TCP port is open or that an application is healthy.

Check whether the destination service is listening and whether its security rules permit the connection.

On a server you control:

```bash
ss -tuln
```

For an HTTPS endpoint:

```bash
curl -v --connect-timeout 10 https://example.com
```

The verbose output can help distinguish connection, TLS, and HTTP errors.

---

# 10. Interview Questions and Answers

### Q1. What is ICMP?

ICMP is a network-layer protocol used for reporting certain IP delivery errors and supporting diagnostic operations.

### Q2. Does ICMP use port numbers?

No. ICMP does not use TCP or UDP ports. It uses fields such as Type and Code to identify messages.

### Q3. How does ping work?

Ping sends ICMP Echo Requests and waits for Echo Replies. It calculates the round-trip time for responses and reports packet statistics.

### Q4. What is RTT?

Round-Trip Time is the elapsed time for a probe to travel to a destination and for the corresponding response to return.

### Q5. What is TTL?

TTL is an IPv4 header field that limits how many router-forwarding hops a packet can survive. Each router decreases it, normally by one.

### Q6. Why is TTL important?

It prevents packets from circulating indefinitely when routing loops occur.

### Q7. What happens when TTL expires?

The router discards the packet. It will ordinarily send an ICMP Time Exceeded message, subject to protocol rules and network policy.

### Q8. How does traceroute work?

Traditional TTL-based traceroute sends probes with progressively increasing TTL values. Routers whose forwarding operation causes the TTL to expire may respond with ICMP Time Exceeded messages, revealing successive hops.

### Q9. Why does traceroute show `* * *`?

The probes did not receive responses within the timeout. Possible causes include filtering, rate limiting, a blocked return path, or a routing problem.

### Q10. Does a failed ping mean the server is down?

No. ICMP may be blocked even when the server is operational and its application services are reachable.

### Q11. What is the difference between ping and traceroute?

Ping primarily tests ICMP Echo communication and measures round-trip times. Traceroute attempts to identify intermediate hops along the path towards a destination.

### Q12. Why might ping work while HTTPS fails?

The host may respond to ICMP while the HTTPS service is unavailable, listening on a different address, blocked by a firewall, or experiencing a TLS or application problem.

---

# 11. Quick Revision Cheat Sheet

| Concept | Remember |
|---|---|
| ICMP | Network diagnostics and error reporting |
| ICMP ports | No TCP/UDP port numbers |
| Echo Request | Probe sent by ping |
| Echo Reply | Response to an Echo Request |
| RTT | Time for a request and its response to complete the round trip |
| IPv4 TTL | Limits packet forwarding hops |
| TTL expiration | Packet is discarded; an ICMP Time Exceeded response may be sent |
| `ping -c 4` | Sends four ping requests |
| `ping -4 -t 1` | Sends IPv4 probes with TTL 1 on typical Linux `ping` |
| `traceroute` | Attempts to discover intermediate hops |
| `traceroute -I` | Selects ICMP Echo probes in common Linux implementations |
| `* * *` | No response received before timeout for those probes |
| Failed ping | Does not prove that the destination is down |
| Successful ping | Does not prove that a particular application is healthy |

### The three commands to remember

```bash
# Test connectivity and measure RTT
ping -c 4 google.com

# Test IPv4 TTL expiration
ping -4 -t 1 -c 4 8.8.8.8

# Discover intermediate hops
traceroute google.com
```

---

# 12. Practice Questions

Try answering these without looking at the notes.

1. What is ICMP, and why does it not need TCP or UDP port numbers?
2. What is the difference between an ICMP Echo Request and an Echo Reply?
3. What does `time=20 ms` mean in ping output?
4. Why can a server be reachable through HTTPS even when ping fails?
5. What does TTL do when a packet travels through routers?
6. What happens when an IPv4 packet's TTL expires?
7. How does traceroute use TTL to identify intermediate routers?
8. Why might traceroute show `* * *` for one hop but display later hops successfully?
9. What is the difference between `ping` and `traceroute`?
10. On Linux, which option sets the IPv4 TTL for `ping`: `-m` or `-t`?

## Solutions

**1.** ICMP supports network diagnostics and error reporting. It uses ICMP-specific message fields rather than TCP or UDP port numbers.

**2.** An Echo Request asks the destination to respond; an Echo Reply is the corresponding response.

**3.** It indicates that the measured round trip took approximately 20 milliseconds.

**4.** A firewall may block ICMP while permitting TCP traffic to the HTTPS service.

**5.** Each router decreases the IPv4 TTL during forwarding, limiting how many router hops a packet can traverse.

**6.** The router discards the packet and may send an ICMP Time Exceeded message.

**7.** Traceroute sends probes with increasing TTL values and observes responses from routers where the TTL expires.

**8.** The router may filter diagnostic responses or rate-limit them while continuing to forward traffic.

**9.** Ping measures round-trip times for ICMP Echo communication. Traceroute attempts to identify the intermediate hops towards a destination.

**10.** On typical Linux `ping`, `-t` sets the IPv4 TTL. `-m` sets a packet mark.

---

## Lecture 13 Complete

You've now learned how ICMP, ping, TTL, and traceroute help diagnose network behavior.

For your Cloud/DevOps journey, remember this practical troubleshooting approach:

1. **Check basic connectivity** with `ping`, while remembering that ICMP may be blocked.
2. **Inspect the route** with `ip route` and `ip route get <destination>`.
3. **Investigate the path** with `traceroute` or `tracepath`.
4. **Test the actual application** with tools such as `curl` or `ssh`.
5. **Use the results as evidence**, rather than assuming one failed command proves the entire server or network is down.
