# Chapter 10 — Python Lists

## 1. What Is a List?

A list stores multiple values in one variable.

```python
servers = ["web-01", "web-02", "web-03"]
```

Lists use square brackets:

```text
[ ]
```

Items are separated by commas.

---

## 2. Why Lists Matter in DevOps

Lists can store:

- Servers
- Files
- Containers
- Kubernetes pods
- IP addresses
- Ports
- API results
- Monitoring data

Example:

```python
servers = ["web-01", "web-02", "db-01"]
```

---

## 3. Indexing

List indexes start at `0`.

```python
servers = ["web-01", "web-02", "db-01"]

print(servers[0])
```

Output:

```text
web-01
```

Index positions:

```text
web-01 → 0
web-02 → 1
db-01  → 2
```

---

## 4. Changing an Item

Lists are mutable.

```python
servers = ["web-01", "web-02", "db-01"]

servers[1] = "web-03"

print(servers)
```

---

## 5. `append()`

Adds an item to the end.

```python
servers.append("web-04")
```

---

## 6. `remove()`

Removes an item by value.

```python
servers.remove("web-02")
```

---

## 7. `pop()`

Removes an item by index.

```python
removed = servers.pop(1)
```

`pop()` also returns the removed value.

---

## 8. `len()`

Returns the number of items.

```python
print(len(servers))
```

---

## 9. Looping Through Lists

```python
for server in servers:
    print(server)
```

This is extremely useful in automation because the same operation can be performed on many resources.

---

## 10. Membership

Use `in` to check whether a value exists.

```python
if "web-01" in servers:
    print("Server exists")
```

Use `not in` to check that something does not exist.

```python
if "web-05" not in servers:
    print("Server not found")
```

---

## 11. Sorting

```python
servers.sort()
```

Sorts the list.

---

## 12. Reversing

```python
servers.reverse()
```

Reverses the order.

---

## 13. Common Methods

| Method | Purpose |
|---|---|
| `append()` | Add item |
| `remove()` | Remove by value |
| `pop()` | Remove by index |
| `sort()` | Sort list |
| `reverse()` | Reverse list |

Useful function:

```python
len()
```

---

## 14. Common Error

```python
servers = ["web-01", "web-02"]

print(servers[2])
```

This causes:

```text
IndexError
```

because valid indexes are:

```text
0
1
```

---

## 15. DevOps Example

```python
servers = ["web-01", "web-02", "db-01"]

for server in servers:
    print(f"Checking {server}...")
```

This same pattern will later be used with:

- AWS resources
- Docker containers
- Kubernetes pods
- API results
- Files
- Monitoring data

---

## 16. Server Inventory Project

```python
servers = [
    "web-01",
    "web-02",
    "web-03",
    "db-01"
]

print("========== SERVER INVENTORY ==========")

for server in servers:
    print(f"Server: {server}")

print("--------------------------------------")
print(f"Total servers: {len(servers)}")

if "db-01" in servers:
    print("Database server found")

if "web-05" not in servers:
    print("web-05 is not in the inventory")

print("======================================")
```

---

## 17. Important Concept

A very common DevOps pattern is:

```text
Collection
    ↓
Loop
    ↓
Process each item
```

Example:

```python
for server in servers:
    check_server(server)
```

We'll use this pattern repeatedly throughout the course.

---

## 18. DSA Connection

A Python list is similar to the array/list data structure commonly discussed in DSA.

Important concepts we'll eventually study:

- Indexing
- Searching
- Traversal
- Sorting
- Time complexity

We will learn these gradually rather than stopping the DevOps roadmap for a separate DSA course.