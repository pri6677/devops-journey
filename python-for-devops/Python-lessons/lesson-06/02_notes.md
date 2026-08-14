# Chapter 6 — Conditions

## 1. What Are Conditions?

Conditions allow Python programs to make decisions.

Basic structure:

```python
if condition:
    statement
```

---

## 2. `if`

Example:

```python
cpu_usage = 87

if cpu_usage > 80:
    print("WARNING: High CPU usage")
```

Python checks whether the condition is `True`.

If it is true, the indented code runs.

---

## 3. `else`

`else` runs when the `if` condition is false.

```python
cpu_usage = 60

if cpu_usage > 80:
    print("WARNING: High CPU usage")
else:
    print("CPU usage is normal")
```

---

## 4. `elif`

`elif` allows additional conditions.

```python
cpu_usage = 75

if cpu_usage > 80:
    print("High CPU usage")
elif cpu_usage >= 70:
    print("CPU usage needs monitoring")
else:
    print("CPU usage is normal")
```

---

## 5. Indentation

Python uses indentation to define blocks.

Correct:

```python
if cpu_usage > 80:
    print("High CPU")
```

Normally, use four spaces for indentation.

---

## 6. Colon

The `:` marks the beginning of the code block.

```python
if cpu_usage > 80:
    print("High CPU")
```

---

## 7. Conditions and Boolean Values

A condition normally evaluates to:

```text
True
```

or:

```text
False
```

Example:

```python
cpu_usage = 90

print(cpu_usage > 80)
```

Output:

```text
True
```

---

## 8. Logical Operators

Conditions can be combined.

### `and`

Both conditions must be true.

```python
if cpu_usage > 80 and memory_usage > 80:
    print("High resource usage")
```

### `or`

At least one condition must be true.

```python
if cpu_usage > 80 or memory_usage > 80:
    print("Resource warning")
```

### `not`

Reverses a Boolean.

```python
if not server_running:
    print("Server is down")
```

---

## 9. DevOps Example

```python
disk_usage = 92

if disk_usage >= 90:
    print("CRITICAL: Disk usage is very high")
elif disk_usage >= 80:
    print("WARNING: Disk usage is high")
else:
    print("Disk usage is normal")
```

This is a basic monitoring decision.

---

## 10. Common Errors

### Missing colon

Wrong:

```python
if cpu_usage > 80
```

Correct:

```python
if cpu_usage > 80:
```

### Missing indentation

Wrong:

```python
if cpu_usage > 80:
print("High CPU")
```

Correct:

```python
if cpu_usage > 80:
    print("High CPU")
```

### Assignment instead of comparison

Wrong:

```python
if status = "running":
```

Correct:

```python
if status == "running":
```

---

## 11. Automation Pattern

Conditions create the decision-making part of automation:

```text
Get data
   ↓
Evaluate condition
   ↓
Make decision
   ↓
Take action
```

Examples:

```text
CPU > threshold
Disk > threshold
Container != running
Exit code != 0
HTTP status != 200
Replica count < desired count
```

---

## 12. Mini Project

```python
cpu_usage = 87
memory_usage = 65
disk_usage = 91

print("========== SERVER HEALTH ==========")

if cpu_usage > 80:
    print("WARNING: High CPU usage")
else:
    print("CPU usage is normal")

if memory_usage > 80:
    print("WARNING: High memory usage")
else:
    print("Memory usage is normal")

if disk_usage >= 90:
    print("CRITICAL: Disk usage is very high")
elif disk_usage >= 80:
    print("WARNING: Disk usage is high")
else:
    print("Disk usage is normal")

print("===================================")
```

---

## 13. DevOps Connections

Conditions will be used in:

- Linux automation
- AWS automation
- Docker automation
- Kubernetes automation
- Monitoring
- CI/CD
- API automation
- SRE scripts

The core pattern is:

```text
Observe → Evaluate → Decide → Act
```