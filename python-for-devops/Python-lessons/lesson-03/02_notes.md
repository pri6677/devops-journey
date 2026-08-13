# Chapter 3 — Python Data Types

## 1. What Are Data Types?

A data type tells Python what kind of value a piece of data is.

The main types we need at this stage are:

| Type | Meaning | Example |
|---|---|---|
| `str` | Text | `"web-01"` |
| `int` | Whole number | `80` |
| `float` | Decimal number | `72.5` |
| `bool` | True/False | `True` |
| `None` | No value | `None` |

Understanding data types is important because Python performs different operations depending on the type of value.

---

# 2. String — `str`

A string represents text.

```python
server_name = "web-01"
```

Here:

```text
server_name → "web-01"
```

`"web-01"` is a string.

Strings can use either double quotes:

```python
server_name = "web-01"
```

or single quotes:

```python
server_name = 'web-01'
```

Both are valid.

For consistency, this course generally uses double quotes.

### DevOps examples

```python
server_name = "web-01"
environment = "production"
log_file = "/var/log/nginx/access.log"
region = "ap-south-1"
```

---

# 3. Integer — `int`

An integer is a whole number without a decimal part.

Examples:

```python
port = 80
cpu_count = 4
retry_count = 3
```

These values are integers.

Important difference:

```python
port = 80
```

`80` is a number.

```python
port = "80"
```

`"80"` is text.

They may look similar to humans, but Python treats them as different types.

---

# 4. Float — `float`

A float is a number containing a decimal value.

Examples:

```python
cpu_usage = 72.5
memory_usage = 64.8
temperature = 42.3
```

These values are floats.

Floats are useful when working with measurements such as:

- CPU usage
- Memory usage
- Temperature
- Network measurements
- Performance metrics

---

# 5. Boolean — `bool`

A Boolean represents one of two states:

```python
True
False
```

Example:

```python
server_running = True
```

or:

```python
server_running = False
```

Booleans are extremely useful in automation because scripts frequently need to represent states.

Examples:

```python
service_running = True
backup_exists = False
deployment_successful = True
```

Important:

```python
True
```

is a Boolean.

But:

```python
"True"
```

is a string.

---

# 6. None

`None` represents the absence of a value.

Example:

```python
backup_file = None
```

This can mean:

> There is currently no backup file value.

`None` is different from:

```text
0
""
False
```

It has its own type called `NoneType`.

We will use `None` more when learning functions, APIs, and error handling.

---

# 7. Checking a Data Type

Python provides the `type()` function.

Example:

```python
server_name = "web-01"

print(type(server_name))
```

Output:

```text
<class 'str'>
```

This means the value is a string.

Example:

```python
port = 80

print(type(port))
```

Output:

```text
<class 'int'>
```

Example:

```python
cpu_usage = 72.5

print(type(cpu_usage))
```

Output:

```text
<class 'float'>
```

---

# 8. Checking Multiple Types

```python
server_name = "web-01"
port = 80
cpu_usage = 72.5
server_running = True
backup_file = None

print(type(server_name))
print(type(port))
print(type(cpu_usage))
print(type(server_running))
print(type(backup_file))
```

Output:

```text
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
<class 'NoneType'>
```

---

# 9. What Does `<class 'str'>` Mean?

For now, simply understand:

```text
<class 'str'>
```

means:

> The value is a string.

Similarly:

```text
<class 'int'>
```

means:

> The value is an integer.

We will study Python classes in much more detail later.

---

# 10. Dynamic Typing

Python is dynamically typed.

This means we do not have to explicitly declare the type of a variable before assigning a value.

For example:

```python
value = "hello"
```

Later:

```python
value = 100
```

The variable can now refer to an integer.

Python determines the type from the value.

---

# 11. String vs Integer

These are different:

```python
port = 80
```

and:

```python
port = "80"
```

The first:

```text
80 → int
```

The second:

```text
"80" → str
```

This difference matters when performing operations.

For example:

```python
port = 80

print(port + 1)
```

Output:

```text
81
```

But:

```python
port = "80"

print(port + 1)
```

causes a `TypeError`.

Python cannot directly combine a string and an integer using `+`.

---

# 12. Type Conversion

Type conversion means changing a value from one type to another.

## String to Integer

```python
port = "80"

port = int(port)
```

Now:

```text
"80"
 ↓
80
```

The value is now an integer.

---

## String to Float

```python
cpu_usage = "72.5"

cpu_usage = float(cpu_usage)
```

Now:

```text
"72.5"
 ↓
72.5
```

---

## Integer to String

```python
port = 80

port = str(port)
```

Now:

```text
80
 ↓
"80"
```

---

# 13. Important Conversion Functions

```python
int()
```

Converts a compatible value to an integer.

```python
float()
```

Converts a compatible value to a float.

```python
str()
```

Converts a value to a string.

Example:

```python
age = int("20")
price = float("19.99")
port = str(80)
```

---

# 14. DevOps Example — Configuration Values

External configuration often arrives as text.

For example:

```text
CPU_THRESHOLD=80
```

A Python program may receive:

```python
threshold = "80"
```

If we want to perform numerical calculations, we can convert it:

```python
threshold = int(threshold)
```

Now:

```text
"80"
 ↓
80
```

This will become important when we learn:

- Environment variables
- Configuration files
- Command-line arguments
- APIs

---

# 15. DevOps Example — Monitoring

A monitoring script may work with:

```python
cpu_usage = 72.5
cpu_threshold = 80
```

Later we can compare these values:

```text
CPU usage = 72.5%
Threshold = 80%

72.5 < 80
```

Then the script can determine whether an alert is required.

The comparison and conditional logic will be learned in later chapters.

---

# 16. DevOps Example — Server Information

A server can be represented using different data types:

```python
server_name = "web-01"
port = 80
cpu_usage = 72.5
server_running = True
backup_file = None
```

Here:

```text
server_name    → str
port           → int
cpu_usage      → float
server_running → bool
backup_file    → NoneType
```

---

# 17. Common Mistakes

## Mistake 1 — Number stored as text

```python
port = "80"
```

If numerical operations are required, convert it:

```python
port = int("80")
```

---

## Mistake 2 — Boolean stored as text

Incorrect when a Boolean is required:

```python
server_running = "True"
```

Correct:

```python
server_running = True
```

---

## Mistake 3 — Decimal stored as text

```python
cpu_usage = "72.5"
```

If numerical calculations are required:

```python
cpu_usage = float("72.5")
```

---

# 18. Industry Note

DevOps and SRE automation constantly receives data from external systems.

Typical flow:

```text
Linux
  ↓
Command output
  ↓
Python
  ↓
Data conversion
  ↓
Automation logic
```

Other sources include:

```text
Environment variables
Configuration files
APIs
AWS
Docker
Kubernetes
Monitoring systems
CI/CD pipelines
```

A large part of reliable automation is making sure the data has the correct type before using it.

---

# 19. DevOps Roadmap Connection

Data types will appear throughout the entire Python-for-DevOps roadmap.

### Linux Automation

Command output often needs to be processed as text or numbers.

### APIs

JSON responses contain strings, numbers, Booleans, lists, dictionaries, and null values.

### AWS

`boto3` returns structured Python data containing many different types.

### Docker

Container information can contain names, IDs, ports, states, and resource values.

### Kubernetes

Kubernetes API responses contain structured data that Python scripts process.

### Monitoring

CPU, memory, disk, network, and threshold values often require numerical types.

### CI/CD

Pipeline configuration frequently arrives as strings and may need conversion.

---

# 20. Practice Code

```python
server_name = "web-01"
port = 80
cpu_usage = 72.5
server_running = True
backup_file = None

print(type(server_name))
print(type(port))
print(type(cpu_usage))
print(type(server_running))
print(type(backup_file))
```

---

# 21. Project Code

```python
server_name = "web-01"
port = 80
cpu_usage = 72.5
server_running = True
backup_file = None

print("Server:", server_name)
print("Port:", port)
print("CPU Usage:", cpu_usage)
print("Running:", server_running)
print("Backup:", backup_file)
```

---

# 22. Quick Reference

```text
str
→ text
→ "web-01"

int
→ whole number
→ 80

float
→ decimal number
→ 72.5

bool
→ True / False
→ True

None
→ no value
→ None
```

Type checking:

```python
type(value)
```

Conversions:

```python
int(value)
float(value)
str(value)
```

---

# 23. Chapter Summary

We learned:

1. What data types are.
2. `str`
3. `int`
4. `float`
5. `bool`
6. `None`
7. `type()`
8. Dynamic typing.
9. Difference between `"80"` and `80`.
10. Type conversion.
11. Why types matter in DevOps automation.

---

# 24. Next Chapter

## Chapter 4 — Input and Output

We will learn how a Python program can receive information from a user and produce useful output.

This will lead directly toward:

```text
Input
  ↓
Process
  ↓
Output
```

which is the foundation of automation scripts.