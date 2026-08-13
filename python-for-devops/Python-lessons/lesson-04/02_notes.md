# Chapter 4 — Input and Output

## 1. Input

Python's `input()` function allows a program to receive information from the user.

```python
name = input("Enter your name: ")
```

The program displays the prompt and waits for the user to enter a value.

---

## 2. Important Rule

`input()` always returns a string.

```python
port = input("Enter port: ")
```

If the user enters:

```text
80
```

Python receives:

```python
"80"
```

not:

```python
80
```

---

## 3. Converting Input

Use `int()` when an integer is required:

```python
port = int(input("Enter port: "))
```

Use `float()` when a decimal number is required:

```python
cpu_usage = float(input("Enter CPU usage: "))
```

The general pattern is:

```text
input()
   ↓
string
   ↓
type conversion
   ↓
required type
```

---

## 4. Output

Python uses `print()` to display information.

```python
print("Hello")
```

Variables can also be printed:

```python
server = "web-01"

print(server)
```

Multiple values:

```python
server = "web-01"
port = 80

print(server, port)
```

---

## 5. Labels in Output

```python
print("Server:", server)
print("Port:", port)
```

This makes terminal output easier to understand.

---

## 6. f-Strings

An f-string is a formatted string.

Example:

```python
server = "web-01"

print(f"Server: {server}")
```

Output:

```text
Server: web-01
```

Variables can be inserted inside `{}`.

Multiple variables:

```python
server = "web-01"
port = 80

print(f"Server {server} is using port {port}")
```

---

## 7. Input and Output Pattern

A basic interactive Python program follows:

```text
Input
  ↓
Processing
  ↓
Output
```

Example:

```python
server = input("Enter server: ")

print(f"Server: {server}")
```

---

## 8. Type Conversion

Common conversions:

```python
int("80")
float("72.5")
str(80)
```

Examples:

```python
port = int("80")
cpu = float("72.5")
port_text = str(80)
```

---

## 9. Common Error

This can cause a `ValueError`:

```python
port = int(input("Enter port: "))
```

if the user enters:

```text
eighty
```

Python cannot convert `"eighty"` into an integer.

Error handling will be studied later.

---

## 10. DevOps Connection

Input and output are fundamental to automation.

Later, data will come from:

- Linux commands
- Environment variables
- Configuration files
- APIs
- AWS
- Docker
- Kubernetes
- CI/CD pipelines
- Monitoring systems

Instead of manually entering values, professional automation usually obtains data automatically.

---

## 11. Mini Project

Server Configuration Generator:

```python
server_name = input("Enter server name: ")
ip_address = input("Enter IP address: ")
port = int(input("Enter port: "))
environment = input("Enter environment: ")

print()
print("========== SERVER CONFIGURATION ==========")
print(f"Server: {server_name}")
print(f"IP Address: {ip_address}")
print(f"Port: {port}")
print(f"Environment: {environment}")
print("===========================================")
```

---

## 12. Key Takeaways

```text
input()
→ receives user input
→ always returns str

print()
→ displays output

int()
→ converts to integer

float()
→ converts to float

str()
→ converts to string

f"...{variable}..."
→ formatted string
```

---

## 13. Future DevOps Applications

```text
Input
 ↓
Linux automation
 ↓
APIs
 ↓
AWS
 ↓
Docker
 ↓
Kubernetes
 ↓
CI/CD
 ↓
Monitoring
```

The concepts learned here will be reused throughout the Python-for-DevOps course.