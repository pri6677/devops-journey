# Personal File Server

A simple personal file server built with Python and Flask that turns a Linux laptop into a private file storage server.

Files can be uploaded, downloaded, viewed, and deleted from another device connected to the same local network through a web browser.

---

## Project Overview

The idea behind this project is simple:

Instead of using a separate cloud storage service, a laptop can act as a personal server for storing and managing files.

Any device connected to the same Wi-Fi network can access the server through its web browser.

### Basic Architecture

```text
                 Wi-Fi / Local Network
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       Phone / PC               Other Device
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Linux Laptop  │
                │                 │
                │  Flask Server   │
                │       │         │
                │       ▼         │
                │  server-files/  │
                └─────────────────┘
```

---

## Objectives

- Learn how a server works in a practical environment.
- Use a laptop as a local file server.
- Allow other devices to access the server through a web browser.
- Upload files to the laptop remotely.
- Download files from the laptop.
- Delete files remotely.
- Implement basic authentication.
- Understand how Python and Flask can be used to build a web server.

---

## Features

### Authentication

- Username and password authentication
- Password verification using password hashing
- Login session
- Logout functionality

### File Management

Authenticated users can:

- Upload files
- View uploaded files
- Download files
- Delete files

### Network Access

The Flask server listens on the laptop's network interface, allowing other devices connected to the same local network to access it.

Example:

```text
http://10.147.135.123:8000
```

The IP address may be different depending on the network.

### Secure File Names

Uploaded filenames are processed using Werkzeug's `secure_filename()` before being stored.

### Environment Variables

Sensitive configuration such as:

- Secret key
- Username
- Password hash

is stored in a `.env` file instead of directly inside the Python source code.

The `.env` file is excluded from Git using `.gitignore`.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Flask | Web server and application framework |
| HTML | Web page structure |
| CSS | Web interface styling |
| Werkzeug | Password hashing and secure filenames |
| python-dotenv | Environment variable management |
| Linux | Server operating system |
| Git | Version control |

---

## Project Structure

```text
personal-file-server/
│
├── server.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── templates/
│   ├── login.html
│   └── index.html
│
├── static/
│   └── style.css
│
├── server-files/
│   └── uploaded files
│
└── .venv/
```

### Important

The following should not be uploaded to GitHub:

```text
.env
.venv/
__pycache__/
```

They are excluded using `.gitignore`.

---

# How the System Works

## 1. Start the Server

```bash
python server.py
```

Flask starts listening on port `8000`.

```text
Laptop
   │
   └── Flask
        │
        └── Port 8000
```

---

## 2. Find the Laptop's IP Address

Run:

```bash
ip addr
```

Find the active Wi-Fi interface.

Example:

```text
wlp2s0

inet 10.147.135.123/24
```

The laptop's local IP address is:

```text
10.147.135.123
```

---

## 3. Connect From Another Device

Connect the second device to the same Wi-Fi network.

Open a browser and enter:

```text
http://10.147.135.123:8000
```

The login page will appear.

---

## 4. Login

The user enters the username and password.

Flask verifies the credentials.

```text
Login
  │
  ▼
Credentials verified
  │
  ▼
Session created
  │
  ▼
Dashboard
```

---

## 5. Upload a File

The user selects a file from the other device.

```text
Phone
  │
  │ Upload
  ▼
Flask Server
  │
  ▼
secure_filename()
  │
  ▼
server-files/
```

The file is stored on the laptop.

---

## 6. Download a File

The user selects the Download option.

The Flask server sends the selected file back to the client device.

```text
server-files/
     │
     ▼
Flask
     │
     ▼
Phone / PC
```

---

## 7. Delete a File

The user selects Delete.

The Flask application removes the selected file from:

```text
server-files/
```

---

# Flask Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | File dashboard |
| `/login` | GET/POST | Login |
| `/logout` | GET | Logout |
| `/upload` | POST | Upload file |
| `/download/<filename>` | GET | Download file |
| `/delete/<filename>` | POST | Delete file |

---

# Security Features

## Password Hashing

The application does not need to store the user's plain-text password.

Instead, a password hash is stored and verified using Werkzeug.

```python
check_password_hash()
```

---

## Session Authentication

After successful login:

```python
session["logged_in"] = True
```

Protected routes check the session before allowing access.

```python
if not session.get("logged_in"):
    return redirect(url_for("login"))
```

---

## Environment Variables

Sensitive configuration is stored in:

```text
.env
```

Example:

```text
SECRET_KEY=your-secret-key
USERNAME=admin
PASSWORD_HASH=your-password-hash
```

Do not upload `.env` to GitHub.

---

## Secure Filenames

Uploaded filenames are processed with:

```python
secure_filename(file.filename)
```

before being saved.

This helps prevent unsafe filenames from being directly used as filesystem paths.

---

# Installation

## Requirements

You need:

- Linux, macOS, or Windows
- Python 3
- Git
- A local network/Wi-Fi connection

---

## Clone the Project

```bash
git clone <your-github-repository-url>
cd personal-file-server
```

---

## Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```text
SECRET_KEY=your-secret-key
USERNAME=admin
PASSWORD_HASH=your-password-hash
```

Do not upload `.env` to GitHub.

---

# Running the Server

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the server:

```bash
python server.py
```

The server will be available locally at:

```text
http://127.0.0.1:8000
```

And on the laptop's local network IP:

```text
http://<laptop-ip>:8000
```

Example:

```text
http://10.147.135.123:8000
```

---

# Local Network Requirement

The client device and server laptop must normally be connected to the same local network.

```text
                 Wi-Fi Router
                 /          \
                /            \
               ▼              ▼
        Laptop Server       Phone
        10.147.135.123      Client
                │
                │
                └────── HTTP ──────►
                     Port 8000
```

---

# Limitations

This project is intentionally designed as a simple local file server.

Current limitations include:

- Designed primarily for a local network.
- Uses a single login account.
- No database is used.
- No HTTPS is configured.
- No advanced user permissions.
- No cloud deployment.
- No automatic backup system.
- File-size restrictions are not currently implemented.

These limitations can be addressed in future versions if required.

---

# Future Improvements

Possible future improvements include:

- Multiple user accounts
- File-size limits
- File type restrictions
- HTTPS
- Database integration
- User-specific storage
- File search
- Folder support
- File previews
- Docker deployment
- Remote access over the Internet
- Cloud backup
- Storage monitoring

---

# Advantages

- Simple architecture
- Easy to understand
- Uses an existing laptop as the server
- No external cloud service required
- Files remain on the local machine
- Accessible from multiple devices on the same network
- Demonstrates practical server and networking concepts

---

# What I Learned

This project helped demonstrate practical concepts including:

- Python programming
- Flask web applications
- HTTP requests and responses
- Client-server architecture
- Local networking
- IP addresses
- Ports
- Authentication
- Sessions
- Password hashing
- File handling
- Environment variables
- Basic application security
- Linux server usage
- Git and GitHub

---

# Project Demonstration

A simple demonstration can follow these steps:

1. Start the Flask server on the laptop.
2. Find the laptop's IP address.
3. Connect a phone or another computer to the same Wi-Fi.
4. Open the server address in a browser.
5. Login.
6. Upload a file.
7. Show the file appearing on the laptop.
8. Download the file from another device.
9. Delete the file.
10. Logout.

---

# Conclusion

The Personal File Server demonstrates how a normal Linux laptop can be used as a local server for storing and managing files.

Instead of depending on an external cloud storage service, the laptop provides the storage while Flask provides the web-based interface for accessing it.

The project demonstrates the basic relationship between:

```text
Client
   │
   │ HTTP
   ▼
Server
   │
   ▼
Storage
```

This project provides a practical introduction to server-side programming, networking, authentication, file management, and Linux-based infrastructure.

---

## Author

**Pri**

BCA Student

**Personal File Server — University Project**
