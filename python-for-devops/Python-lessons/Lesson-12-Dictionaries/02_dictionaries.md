# Lesson 12 — Dictionaries

> Python for Cloud & DevOps Engineering

---

## 1. Where I Am in the Python Roadmap

We are currently in **Phase 1 — Python Foundations**.

```text
Phase 1 — Python Foundations

Lesson 01 — Running Python        ✅
Lesson 02 — Variables             ✅
Lesson 03 — Data Types            ✅
Lesson 04 — Input / Output        ✅
Lesson 05 — Operators             ✅
Lesson 06 — Conditions            ✅
Lesson 07 — Loops                 ✅
Lesson 08 — Functions              ✅
Lesson 09 — Error Handling         ✅
Lesson 10 — Lists                  ✅
Lesson 11 — Tuples & Sets          ✅
Lesson 12 — Dictionaries           ✅ CURRENT
```

Dictionaries are one of the most important Python fundamentals for DevOps because they are heavily used when working with:

- JSON
- REST APIs
- AWS SDK (`boto3`)
- Kubernetes APIs
- Configuration data
- Monitoring data

---

# 2. Previous Lesson Recap

In Lesson 11, we learned about:

### Tuples

```python
ports = (22, 80, 443)
```

Tuples are:

- Ordered
- Immutable
- Allow duplicates

### Sets

```python
servers = {"web-01", "web-02", "web-03"}
```

Sets:

- Store unique values
- Do not provide reliable ordering
- Are useful for membership checks
- Are useful for comparing collections

For example:

```python
missing = expected_servers - running_servers
```

This allowed us to compare expected infrastructure with actual infrastructure.

---

# 3. Practical Problem

Suppose we have information about a server.

We could create separate variables:

```python
server_name = "web-01"
server_ip = "10.0.0.10"
server_port = 80
server_status = "running"
```

This works for one server.

But imagine managing:

```text
100 servers
500 servers
1000 servers
```

Creating separate variables for everything would become difficult to manage.

We need a way to group related information together.

A dictionary solves this problem:

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80,
    "status": "running"
}
```

Now all the information about the server is stored together.

---

# 4. What Is a Dictionary?

A dictionary is a Python data structure that stores information as **key-value pairs**.

Example:

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80
}
```

Conceptually:

```text
KEY             VALUE

"name"    →     "web-01"
"ip"      →     "10.0.0.10"
"port"    →     80
```

The **key** identifies the piece of information.

The **value** contains the actual information.

---

# 5. Real-World Analogy

Think about a server information card.

```text
Server Information
------------------
Name       → web-01
IP         → 10.0.0.10
Port       → 80
Status     → running
```

A Python dictionary represents the same idea:

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80,
    "status": "running"
}
```

Instead of remembering that the third value represents the port, we can directly ask for:

```python
server["port"]
```

This makes structured information much easier to work with.

---

# 6. Dictionary Syntax

A dictionary uses curly braces:

```python
{
    "key": value,
    "key": value
}
```

Example:

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10"
}
```

Important symbols:

```text
{ }   → dictionary boundaries

:     → separates key and value

,     → separates key-value pairs
```

For example:

```python
"name": "web-01"
```

means:

```text
key     → "name"
value   → "web-01"
```

---

# 7. Accessing Dictionary Values

We access a dictionary value using its key.

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80
}

print(server["name"])
print(server["ip"])
print(server["port"])
```

Output:

```text
web-01
10.0.0.10
80
```

Unlike a list, we don't use a numeric index.

### List

```python
servers[0]
```

### Dictionary

```python
server["name"]
```

Mental model:

```text
List
 ↓
Find by position

Dictionary
 ↓
Find by key
```

---

# 8. Dictionaries Are Mutable

Dictionaries can be changed after they are created.

Example:

```python
server = {
    "name": "web-01",
    "status": "running"
}

server["status"] = "stopped"

print(server["status"])
```

Output:

```text
stopped
```

The existing value was changed.

---

# 9. Adding a New Key

A new key can be added using assignment.

```python
server = {
    "name": "web-01"
}

server["ip"] = "10.0.0.10"
server["port"] = 80
```

The dictionary now contains:

```text
name → web-01
ip   → 10.0.0.10
port → 80
```

Python uses the same syntax for:

- Updating an existing key
- Creating a new key

Example:

```python
server["status"] = "running"
```

If `"status"` already exists, it is updated.

If it doesn't exist, it is created.

---

# 10. Removing a Key

The `del` keyword can remove a key.

```python
server = {
    "name": "web-01",
    "port": 80
}

del server["port"]
```

Now `"port"` no longer exists.

`del` means **delete**.

---

# 11. Checking Whether a Key Exists

We can use the `in` operator.

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10"
}

if "ip" in server:
    print("IP address exists")
```

Output:

```text
IP address exists
```

This is useful in automation because data received from APIs or configuration files may not always contain every possible field.

---

# 12. The `get()` Method

Consider:

```python
server = {
    "name": "web-01"
}

print(server["ip"])
```

The `"ip"` key doesn't exist.

Python raises:

```text
KeyError
```

Instead, we can use:

```python
print(server.get("ip"))
```

The result is:

```text
None
```

`None` represents the absence of a value.

---

# 13. Providing a Default with `get()`

We can provide a default value:

```python
server = {
    "name": "web-01"
}

print(server.get("ip", "Unknown"))
```

Output:

```text
Unknown
```

The structure is:

```python
dictionary.get(key, default_value)
```

This is particularly useful when processing data where a key may or may not exist.

---

# 14. Getting Dictionary Keys

The `keys()` method returns the dictionary's keys.

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80
}

print(server.keys())
```

We can also loop through them:

```python
for key in server.keys():
    print(key)
```

Output:

```text
name
ip
port
```

---

# 15. Getting Dictionary Values

The `values()` method gives us the values.

```python
for value in server.values():
    print(value)
```

Output:

```text
web-01
10.0.0.10
80
```

---

# 16. Getting Keys and Values Together

The `items()` method gives us both the key and value.

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80
}

for key, value in server.items():
    print(key, value)
```

Output:

```text
name web-01
ip 10.0.0.10
port 80
```

The important pattern is:

```python
for key, value in dictionary.items():
```

This will be used frequently in automation.

---

# 17. Nested Dictionaries

Real-world infrastructure data is often nested.

Example:

```python
server = {
    "name": "web-01",
    "network": {
        "ip": "10.0.0.10",
        "port": 80
    }
}
```

The `network` value is itself another dictionary.

To access the IP:

```python
print(server["network"]["ip"])
```

Output:

```text
10.0.0.10
```

Think of it as:

```text
server
│
├── name
│
└── network
     │
     ├── ip
     └── port
```

Nested dictionaries are extremely common when processing API responses.

---

# 18. Dictionaries and JSON

One of the biggest reasons dictionaries matter for DevOps is JSON.

JSON commonly looks like:

```json
{
    "name": "web-01",
    "ip": "10.0.0.10",
    "status": "running"
}
```

When Python processes JSON, the resulting structure commonly uses Python dictionaries and lists.

Conceptually:

```text
JSON
 ↓
Python
 ↓
Dictionary / List
 ↓
Process the data
```

We will study JSON properly later in the automation phase.

---

# 19. Dictionaries and APIs

Suppose an API returns information about a server.

Conceptually:

```python
response = {
    "name": "web-01",
    "status": "running",
    "ip": "10.0.0.10"
}
```

We can access:

```python
print(response["name"])
print(response["status"])
print(response["ip"])
```

This is the basic pattern behind a lot of API automation.

---

# 20. DevOps Example — Server Configuration

Our project stores server information in a dictionary:

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80,
    "environment": "production",
    "status": "running"
}
```

We can display individual values:

```python
print(server["name"])
print(server["ip"])
print(server["status"])
```

We can also process the complete dictionary:

```python
for key, value in server.items():
    print(f"{key}: {value}")
```

This allows a script to work with structured server information.

---

# 21. Complete Project Code

The project file is:

```text
03_server_config.py
```

Code:

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80,
    "environment": "production",
    "status": "running"
}

print("========== SERVER CONFIGURATION ==========")

print(f"Name: {server['name']}")
print(f"IP: {server['ip']}")
print(f"Port: {server['port']}")
print(f"Environment: {server['environment']}")
print(f"Status: {server['status']}")

print("\nConfiguration:")

for key, value in server.items():
    print(f"{key}: {value}")

print("===========================================")
```

---

# 22. What This Project Combines

This small project combines several concepts we've already learned:

```text
Variables
    ↓
Dictionary
    ↓
Dictionary keys
    ↓
Dictionary values
    ↓
f-strings
    ↓
for loop
    ↓
.items()
    ↓
Terminal output
```

This is closer to real automation than isolated syntax examples.

---

# 23. Common Mistakes

## Mistake 1 — Using a list index

Wrong:

```python
server[0]
```

A dictionary is accessed using keys:

```python
server["name"]
```

---

## Mistake 2 — Missing key

This can raise:

```python
server["hostname"]
```

If `"hostname"` doesn't exist:

```text
KeyError
```

Use:

```python
server.get("hostname")
```

when the key may be missing.

---

## Mistake 3 — Forgetting quotation marks

Wrong:

```python
server[name]
```

Correct:

```python
server["name"]
```

---

## Mistake 4 — Using `=` instead of `:`

Inside a dictionary:

```python
"name": "web-01"
```

Not:

```python
"name" = "web-01"
```

The colon separates the key and value.

---

# 24. Industry Note

Dictionaries are one of the most important Python data structures for DevOps.

Professional DevOps engineers frequently process structured data from:

- REST APIs
- AWS APIs
- Kubernetes APIs
- JSON files
- YAML configuration
- Monitoring systems
- CI/CD systems

A response may contain nested information such as:

```text
API response
│
├── status
├── server
│    ├── name
│    ├── ip
│    └── region
│
└── metadata
     ├── environment
     └── owner
```

Python dictionaries allow us to navigate and process this information.

---

# 25. How This Helps in DevOps

Dictionaries connect directly to your future roadmap:

```text
Python Dictionaries
        ↓
JSON
        ↓
REST APIs
        ↓
AWS boto3
        ↓
Kubernetes APIs
        ↓
Monitoring data
        ↓
Automation
```

For example, later:

```text
AWS API
   ↓
boto3
   ↓
Python dictionary
   ↓
Extract EC2 information
   ↓
Check instance status
   ↓
Take action
```

This is why mastering dictionaries is important before we move into API and cloud automation.

---

# 26. Connection to Future Technologies

### Linux Automation

Python can collect system information and organize it into dictionaries:

```python
system = {
    "hostname": "server01",
    "uptime": "5 days",
    "disk_usage": 72
}
```

### AWS

AWS SDK responses contain structured data that Python processes using dictionaries and lists.

### Docker

Container information can be represented as structured data.

### Kubernetes

Kubernetes resources contain deeply nested structured information.

### Terraform

Terraform configuration and state involve structured data concepts.

### CI/CD

Pipeline APIs often return JSON that Python processes as dictionaries.

### Monitoring

Metrics, alerts, and system information can be organized into dictionaries for processing.

---

# 27. Dictionary vs Other Collections

| Feature | List | Tuple | Set | Dictionary |
|---|---|---|---|---|
| Syntax | `[ ]` | `( )` | `{ }` | `{key: value}` |
| Ordered | Yes | Yes | No reliable order | Yes |
| Mutable | Yes | No | Yes | Yes |
| Duplicates | Yes | Yes | No | Keys must be unique |
| Access | Index | Index | Membership | Key |
| Main use | Collection | Fixed collection | Unique values | Structured data |

Mental model:

```text
LIST
→ "Things I have"

TUPLE
→ "Things that should stay fixed"

SET
→ "Unique things I need to compare"

DICTIONARY
→ "Information about something"
```

---

# 28. Cheat Sheet

## Create a dictionary

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10"
}
```

## Access a value

```python
server["name"]
```

## Add a key

```python
server["port"] = 80
```

## Update a value

```python
server["port"] = 443
```

## Delete a key

```python
del server["port"]
```

## Check for a key

```python
if "ip" in server:
    print("Found")
```

## Safely get a value

```python
server.get("ip")
```

## Get a default value

```python
server.get("hostname", "Unknown")
```

## Get keys

```python
server.keys()
```

## Get values

```python
server.values()
```

## Get key-value pairs

```python
server.items()
```

## Loop through a dictionary

```python
for key, value in server.items():
    print(key, value)
```

## Access nested data

```python
server["network"]["ip"]
```

---

# 29. Key Takeaways

The most important concepts from this lesson are:

1. A dictionary stores key-value pairs.
2. Dictionaries use `{}`.
3. `:` separates keys and values.
4. Dictionary values are accessed using keys.
5. Dictionaries are mutable.
6. New keys can be added using assignment.
7. `del` removes a key.
8. `in` checks whether a key exists.
9. `get()` safely retrieves a value when a key may not exist.
10. `.keys()` returns keys.
11. `.values()` returns values.
12. `.items()` gives key-value pairs.
13. Dictionaries can contain other dictionaries.
14. Dictionaries are heavily used when processing JSON and APIs.
15. Dictionaries will be extremely important for AWS automation with `boto3`.

---

# 30. Lesson Files

The completed lesson should contain:

```text
Lesson-12-Dictionaries/
├── 01_dictionaries.py
├── 02_dictionaries.md
└── 03_server_config.py
```

---

# 31. Git Workflow

After saving this Markdown file and verifying the Python programs:

```bash
python3 01_dictionaries.py
python3 03_server_config.py
```

Check the repository:

```bash
git status
```

Stage the lesson:

```bash
git add python-for-devops/Python-lessons/Lesson-12-Dictionaries/
```

Commit:

```bash
git commit -m "Complete Lesson 12: Dictionaries"
```

Push:

```bash
git push
```

---

# 32. Final Mental Model

Remember:

```text
List
    ↓
Ordered collection that can change

Tuple
    ↓
Ordered collection that should stay fixed

Set
    ↓
Unique values + comparison

Dictionary
    ↓
Key → Value
    ↓
Structured information
    ↓
JSON / APIs / AWS / Kubernetes
```

Dictionaries are a major bridge between **Python fundamentals** and the **automation/API/cloud work** we will do later.