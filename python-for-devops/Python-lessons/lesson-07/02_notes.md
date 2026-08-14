# Chapter 7 — Python Loops

## 1. What Is a Loop?

A loop repeats code.

Instead of:

```python
print("web-01")
print("web-02")
print("web-03")
```

we can use:

```python
servers = ["web-01", "web-02", "web-03"]

for server in servers:
    print(server)
```

---

## 2. `for` Loop

Basic syntax:

```python
for item in collection:
    code
```

Example:

```python
servers = ["web-01", "web-02", "web-03"]

for server in servers:
    print(server)
```

Output:

```text
web-01
web-02
web-03
```

---

## 3. `range()`

`range()` generates a sequence of numbers.

```python
for number in range(5):
    print(number)
```

Output:

```text
0
1
2
3
4
```

The stop value is not included.

```python
range(1, 6)
```

produces:

```text
1
2
3
4
5
```

---

## 4. `while`

A `while` loop repeats while a condition is true.

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

Output:

```text
1
2
3
4
5
```

---

## 5. `+=`

This:

```python
count += 1
```

is shorthand for:

```python
count = count + 1
```

---

## 6. Infinite Loops

A `while` loop can become infinite if its condition never becomes false.

Bad:

```python
count = 1

while count <= 5:
    print(count)
```

Correct:

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

---

## 7. `break`

`break` immediately exits a loop.

```python
for server in servers:
    if server == "web-02":
        break

    print(server)
```

---

## 8. `continue`

`continue` skips the current iteration.

```python
for server in servers:
    if server == "test-01":
        continue

    print(server)
```

---

## 9. DevOps Example

```python
servers = ["web-01", "web-02", "web-03"]

for server in servers:
    print(f"Checking server: {server}")
```

This pattern is fundamental to automation.

---

## 10. Server Health Scanner

```python
servers = ["web-01", "web-02", "web-03"]

cpu_usage = [45, 87, 62]

for i in range(len(servers)):
    server = servers[i]
    cpu = cpu_usage[i]

    print(f"{server}: CPU {cpu}%")

    if cpu > 80:
        print("  WARNING: High CPU usage")
    else:
        print("  CPU usage is normal")
```

---

## 11. DevOps Applications

Loops are used to process:

- Servers
- Files
- Logs
- AWS resources
- Docker containers
- Kubernetes pods
- API responses
- Monitoring metrics
- CI/CD artifacts

Typical automation pattern:

```text
Get resources
     ↓
Loop through resources
     ↓
Check each resource
     ↓
Take action
```

---

## 12. Best Practice

Prefer simple iteration:

```python
for server in servers:
    print(server)
```

rather than unnecessarily using:

```python
for i in range(len(servers)):
    print(servers[i])
```

When we need indexes or paired data, we'll learn better tools later.

---

## 13. Cheat Sheet

```text
for
→ iterate through items

while
→ repeat while condition is true

range()
→ generate number sequence

break
→ exit loop

continue
→ skip current iteration

+=
→ add and assign
```

Examples:

```python
for server in servers:
    print(server)

for number in range(5):
    print(number)

while count <= 5:
    count += 1

break
continue
```