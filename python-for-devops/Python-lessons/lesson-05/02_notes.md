# Chapter 5 — Python Operators

## 1. What Are Operators?

Operators are symbols or keywords that tell Python to perform an operation.

Examples:

```python
10 + 5
cpu_usage > 80
server_running and backup_exists
```

---

# 2. Arithmetic Operators

| Operator | Meaning |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `//` | Floor division |
| `%` | Remainder |
| `**` | Power |

Examples:

```python
print(10 + 5)
print(10 - 5)
print(10 * 5)
print(10 / 5)
print(10 // 3)
print(10 % 3)
print(2 ** 3)
```

---

# 3. Comparison Operators

Comparison operators compare two values and return a Boolean.

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

Examples:

```python
print(10 == 10)
print(10 != 20)
print(10 > 5)
print(10 < 20)
print(10 >= 10)
print(10 <= 10)
```

Results are:

```text
True
True
True
True
True
True
```

---

# 4. `=` vs `==`

This is extremely important.

Assignment:

```python
port = 80
```

means:

> Store 80 in `port`.

Comparison:

```python
port == 80
```

means:

> Is `port` equal to 80?

They are completely different.

---

# 5. Logical Operators

Python provides:

```text
and
or
not
```

## `and`

Both conditions must be true.

```python
cpu_high = True
disk_high = True

print(cpu_high and disk_high)
```

Result:

```text
True
```

---

## `or`

At least one condition must be true.

```python
cpu_high = True
disk_high = False

print(cpu_high or disk_high)
```

Result:

```text
True
```

---

## `not`

Reverses a Boolean.

```python
server_running = True

print(not server_running)
```

Result:

```text
False
```

---

# 6. DevOps Example

```python
cpu_usage = 87
cpu_threshold = 80

print(cpu_usage > cpu_threshold)
```

Output:

```text
True
```

This represents a basic monitoring check.

---

# 7. Arithmetic in DevOps

```python
cpu_usage = 87

remaining = 100 - cpu_usage

print(remaining)
```

Output:

```text
13
```

Calculations like this can be used when processing system metrics.

---

# 8. Operator Precedence

Python follows an order when evaluating expressions.

Example:

```python
result = 10 + 5 * 2
```

Multiplication happens first:

```text
5 * 2 = 10
10 + 10 = 20
```

Parentheses can make the desired order explicit:

```python
result = (10 + 5) * 2
```

Result:

```text
30
```

---

# 9. Common Mistakes

## Using `=` instead of `==`

Wrong:

```python
print(cpu_usage = 80)
```

Correct:

```python
print(cpu_usage == 80)
```

---

## Comparing incompatible types

Problem:

```python
cpu_usage = "90"

print(cpu_usage > 80)
```

`"90"` is a string while `80` is an integer.

Convert it when numerical data is required:

```python
cpu_usage = int("90")
```

---

# 10. Industry Note

DevOps and SRE scripts constantly compare values.

Examples:

```text
CPU > threshold
Disk > threshold
Memory > threshold
HTTP status == 200
Exit code == 0
Replica count != desired count
Container status == running
```

Operators are therefore a fundamental part of automation.

---

# 11. DevOps Connections

Operators will be used in:

- Linux automation
- Monitoring
- Log analysis
- AWS automation
- Docker automation
- Kubernetes automation
- CI/CD
- API automation

The general automation pattern becomes:

```text
Get data
   ↓
Compare / calculate
   ↓
Make decision
   ↓
Take action
```

---

# 12. Mini Project

Server Health Calculator:

```python
cpu_usage = 87
memory_usage = 65
disk_usage = 91

cpu_threshold = 80
memory_threshold = 80
disk_threshold = 90

print("========== SERVER HEALTH ==========")

print(f"CPU Usage: {cpu_usage}%")
print(f"Memory Usage: {memory_usage}%")
print(f"Disk Usage: {disk_usage}%")

print()

print(f"CPU high: {cpu_usage > cpu_threshold}")
print(f"Memory high: {memory_usage > memory_threshold}")
print(f"Disk high: {disk_usage > disk_threshold}")

print("===================================")
```

---

# 13. Cheat Sheet

```text
+    addition
-    subtraction
*    multiplication
/    division
//   floor division
%    remainder
**   power

==   equal
!=   not equal
>    greater than
<    less than
>=   greater than or equal
<=   less than or equal

and  both conditions
or   at least one condition
not  reverse Boolean
```