# Linux Laptop as a Local Server

## Goal

Use my Linux laptop as a simple web server and access it from my phone over the same local network.

This experiment helped me understand how a computer can provide a network service that another device can access.

---

## Architecture

```text
             Same Wi-Fi Network
        ┌─────────────────────────┐
        │                         │
        ▼                         ▼
   Linux Laptop                Phone
   192.168.0.152                  │
        │                         │
        │ Port 8000               │
        └────────── HTTP ─────────┘
                   │
                   ▼
          Python HTTP Server
```

---

## Step 1 — Find the Laptop's IP Address

First, find the IP addresses assigned to the Linux laptop:

```bash
hostname -I
```

Example output:

```text
192.168.0.152 172.17.0.1
```

The important address for this experiment was:

```text
192.168.0.152
```

This was the laptop's address on the local Wi-Fi network.

The `172.17.0.1` address was related to Docker/container networking and was not the address used by the phone.

---

## Step 2 — Start the HTTP Server

Move into the directory containing the files you want to serve:

```bash
cd ~/path/to/directory
```

Start Python's built-in HTTP server:

```bash
python3 -m http.server 8000
```

The server listens on port `8000`.

The terminal remains occupied by the running server and displays requests received from clients.

---

## Step 3 — Access the Server From the Phone

Make sure:

- The laptop is connected to the Wi-Fi network.
- The phone is connected to the same Wi-Fi network.
- The Python HTTP server is running.

On the phone, open a browser and enter:

```text
http://192.168.0.152:8000
```

The phone can now access the directory being served by the laptop.

---

## How It Works

```text
Phone
  │
  │ HTTP request
  │
  ▼
192.168.0.152:8000
  │
  │
  ▼
Linux Laptop
  │
  ▼
Python HTTP Server
  │
  ▼
Files in the server directory
```

The phone acts as the **client**.

The laptop acts as the **server**.

Python provides the HTTP service.

---

## Understanding the URL

The address:

```text
http://192.168.0.152:8000
```

has three important parts:

```text
http://       → Protocol
192.168.0.152 → Laptop's local IP address
:8000         → Port number
```

### HTTP

HTTP is the protocol used by the browser to communicate with the web server.

### IP Address

`192.168.0.152` identifies the laptop on the local network.

### Port

`8000` identifies the network service running on the laptop.

A single computer can run many network services on different ports.

For example:

```text
22   → SSH
80   → HTTP
443  → HTTPS
8000 → Our Python test server
```

---

## Localhost vs LAN IP

### Localhost

```text
http://127.0.0.1:8000
```

or:

```text
http://localhost:8000
```

`localhost` refers to the same computer.

If the browser on the laptop opens this address, it connects back to the laptop itself.

### LAN IP

```text
http://192.168.0.152:8000
```

This identifies the laptop on the local network.

Another device, such as the phone, can use this address to connect to the laptop.

---

## Useful Commands

### Find IP addresses

```bash
hostname -I
```

### Start the HTTP server

```bash
python3 -m http.server 8000
```

### Stop the server

Press:

```text
Ctrl + C
```

---

## Troubleshooting

If the phone cannot connect, check the following.

### 1. Check the IP address

```bash
hostname -I
```

Make sure you are using the current LAN IP address.

### 2. Check that both devices use the same network

The laptop and phone should normally be connected to the same Wi-Fi/LAN.

### 3. Check that the server is running

The terminal should still have:

```bash
python3 -m http.server 8000
```

running.

### 4. Check the port

Make sure the phone uses the same port:

```text
:8000
```

### 5. Check the firewall

A firewall can prevent incoming connections even when the server is running.

Check the firewall status with:

```bash
sudo ufw status
```

If UFW is active, its rules may need to allow the required connection.

Do not blindly disable the firewall.

---

## Important Security Note

Python's built-in HTTP server is useful for learning and quick local file sharing.

It is **not intended to be a production web server**.

Be careful about the directory from which you start it.

For example:

```bash
cd ~/Documents
python3 -m http.server 8000
```

can make files inside that directory accessible to devices that can reach the server.

Never assume that a simple test server is automatically secure.

---

## What I Learned

This experiment connected several Linux and networking concepts together:

```text
Linux
  │
  ├── IP address
  │
  ├── Network interface
  │
  ├── Port
  │
  ├── Service
  │
  ├── HTTP
  │
  └── Client ↔ Server communication
```

The most important lesson was:

> A server is not necessarily a special computer. A normal Linux laptop can provide a network service that other devices connect to.

This experiment gave me practical experience with:

- Finding a machine's IP address
- Running a network service
- Understanding ports
- Understanding localhost
- Understanding LAN addresses
- Connecting two devices over a network
- Using Python to provide an HTTP service
- Basic network troubleshooting
- Basic firewall awareness

---

## Reproduce the Experiment

The basic workflow is:

```bash
# 1. Find the laptop's IP
hostname -I

# 2. Go to the directory you want to serve
cd ~/path/to/directory

# 3. Start the server
python3 -m http.server 8000
```

Then open this from another device on the same network:

```text
http://<LAPTOP-IP>:8000
```

Example:

```text
http://192.168.0.152:8000
```

Stop the server with:

```text
Ctrl + C
```

---

## Status

**Completed**

This was a hands-on Linux + networking experiment using my Linux laptop as a local HTTP server and accessing it from my phone.
