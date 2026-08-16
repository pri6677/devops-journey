# Lesson 13 — Strings

> Python for Cloud & DevOps Engineering

---

## 1. Where I Am in the Python Roadmap

We are currently in **Phase 1 — Python Foundations**.

```text
Lesson 01 — Running Python        ✅
Lesson 02 — Variables             ✅
Lesson 03 — Data Types            ✅
Lesson 04 — Input / Output        ✅
Lesson 05 — Operators             ✅
Lesson 06 — Conditions            ✅
Lesson 07 — Loops                 ✅
Lesson 08 — Functions             ✅
Lesson 09 — Error Handling        ✅
Lesson 10 — Lists                 ✅
Lesson 11 — Tuples & Sets         ✅
Lesson 12 — Dictionaries          ✅
Lesson 13 — Strings               ✅ CURRENT
```

Strings are especially important for DevOps because automation involves processing:

- Linux command output
- Log files
- Server names
- IP addresses
- URLs
- Error messages
- Configuration data
- Docker/Kubernetes output
- API information

---

# 2. Previous Lesson Recap

In Lesson 12, we learned dictionaries.

A dictionary stores data using key-value pairs:

```python
server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "status": "running"
}
```

We learned:

```python
server["name"]
server.get("ip")
server.keys()
server.values()
server.items()
```

Dictionaries will become extremely important when working with:

- JSON
- APIs
- AWS boto3
- Kubernetes
- Configuration data

---

# 3. Practical Problem

Imagine a Linux server produces this log:

```text
ERROR: nginx connection refused
```

A DevOps engineer may need to:

- Check whether it contains `ERROR`
- Extract information
- Convert text to uppercase/lowercase
- Split the message
- Search for specific words
- Detect whether a filename ends in `.log`

Python strings provide the tools to do this.

---

# 4. What Is a String?

A string is a sequence of text characters.

Example:

```python
server = "web-01"
```

Strings can be created using double quotes:

```python
"hello"
```

or single quotes:

```python
'hello'
```

Both represent strings.

You can check the type:

```python
name = "web-01"

print(type(name))
```

Output:

```text
<class 'str'>
```

`str` means **string**.

---

# 5. String Indexing

Every character in a string has a position called an index.

Example:

```python
server = "web01"
```

The indexes are:

```text
Character:  w  e  b  0  1
Index:      0  1  2  3  4
```

Python starts indexing from `0`.

Therefore:

```python
print(server[0])
```

Output:

```text
w
```

And:

```python
print(server[3])
```

Output:

```text
0
```

---

# 6. Negative Indexing

Python also allows counting from the end.

```python
server = "web01"

print(server[-1])
```

Output:

```text
1
```

The indexes are:

```text
Character:  w   e   b   0   1
Positive:   0   1   2   3   4
Negative:  -5  -4  -3  -2  -1
```

Negative indexing is useful when you need information near the end of a string.

---

# 7. String Slicing

Slicing extracts part of a string.

Syntax:

```python
string[start:end]
```

Example:

```python
server = "web01"

print(server[0:3])
```

Output:

```text
web
```

The important rule is:

> The `end` index is not included.

Therefore:

```python
server[0:3]
```

means:

```text
0 → included
1 → included
2 → included
3 → stop
```

---

# 8. `.upper()`

The `upper()` method converts letters to uppercase.

```python
status = "running"

print(status.upper())
```

Output:

```text
RUNNING
```

---

# 9. `.lower()`

The `lower()` method converts letters to lowercase.

```python
status = "RUNNING"

print(status.lower())
```

Output:

```text
running
```

This is useful when comparing text without caring about capitalization.

For example:

```python
status = "Running"

if status.lower() == "running":
    print("Server is running")
```

---

# 10. `.strip()`

`strip()` removes whitespace from the beginning and end of a string.

Example:

```python
text = "   server running   "

print(text.strip())
```

Output:

```text
server running
```

This is particularly useful when processing:

- Files
- User input
- Linux command output
- Log lines

---

# 11. `.replace()`

`replace()` replaces one piece of text with another.

Example:

```python
server = "web-server"

new_server = server.replace("web", "api")

print(new_server)
```

Output:

```text
api-server
```

Syntax:

```python
string.replace(old, new)
```

---

# 12. `.split()`

`split()` breaks a string into smaller pieces.

Example:

```python
data = "web01,10.0.0.10,running"

parts = data.split(",")

print(parts)
```

Output:

```text
['web01', '10.0.0.10', 'running']
```

Notice that the result is a **list**.

The concept is:

```text
String
   ↓
split()
   ↓
List
```

This is extremely useful when processing command output or log data.

---

# 13. `.join()`

`join()` combines multiple strings into one string.

Example:

```python
servers = ["web01", "web02", "web03"]

result = ",".join(servers)

print(result)
```

Output:

```text
web01,web02,web03
```

Mental model:

```text
split()
String → List

join()
List → String
```

---

# 14. Searching with `in`

The `in` operator checks whether text exists inside another string.

Example:

```python
log = "ERROR nginx connection refused"

if "ERROR" in log:
    print("Error found")
```

Output:

```text
Error found
```

This is one of the most useful operations for basic log analysis.

---

# 15. `.find()`

`find()` searches for text and returns its position.

Example:

```python
log = "ERROR nginx connection refused"

position = log.find("nginx")

print(position)
```

If the text is found, Python returns its starting position.

If it isn't found:

```python
log.find("docker")
```

returns:

```text
-1
```

---

# 16. `.startswith()`

`startswith()` checks whether a string begins with specific text.

Example:

```python
log = "ERROR: disk full"

print(log.startswith("ERROR"))
```

Output:

```text
True
```

Useful for:

- Log classification
- Filename checks
- Server naming conventions
- Command output

---

# 17. `.endswith()`

`endswith()` checks whether a string ends with specific text.

Example:

```python
filename = "server.log"

print(filename.endswith(".log"))
```

Output:

```text
True
```

This is useful when processing files.

For example:

```python
if filename.endswith(".log"):
    print("This is a log file")
```

---

# 18. f-Strings

We have already used f-strings in previous lessons.

Example:

```python
server = "web01"
ip = "10.0.0.10"

print(f"Server {server} has IP {ip}")
```

Output:

```text
Server web01 has IP 10.0.0.10
```

The `f` tells Python that expressions inside `{}` should be evaluated.

Example:

```python
status = "running"

print(f"Server status: {status}")
```

f-strings are very useful for producing readable automation output.

---

# 19. Complete Practice Program

File:

```text
01_strings.py
```

Code:

```python
log = "ERROR: nginx connection refused"

print("Original log:")
print(log)

print("\nUppercase:")
print(log.upper())

print("\nLowercase:")
print(log.lower())

print("\nContains ERROR:")
print("ERROR" in log)

print("\nStarts with ERROR:")
print(log.startswith("ERROR"))

print("\nLog parts:")
parts = log.split(":")
print(parts)
```

Run:

```bash
python3 01_strings.py
```

---

# 20. Mini Project — Log Analyzer

File:

```text
03_log_analyzer.py
```

Code:

```python
logs = [
    "INFO: Server started",
    "ERROR: Disk full",
    "INFO: Backup completed",
    "ERROR: Connection refused",
    "WARNING: CPU usage high"
]

print("========== LOG ANALYZER ==========")

error_count = 0

for log in logs:
    if "ERROR" in log:
        print(log)
        error_count += 1

print("----------------------------------")
print(f"Total errors: {error_count}")
print("==================================")
```

The script:

1. Stores multiple log messages.
2. Loops through each log.
3. Searches for `"ERROR"`.
4. Counts the errors.
5. Displays the result.

This is the beginning of real log-analysis automation.

---

# 21. Common Mistakes

## Mistake 1 — Forgetting `()`

Wrong:

```python
log.upper
```

Correct:

```python
log.upper()
```

`upper` refers to the method.

`upper()` calls the method.

---

## Mistake 2 — Invalid Index

```python
server = "web"
print(server[5])
```

The string doesn't contain index `5`.

Python raises:

```text
IndexError
```

---

## Mistake 3 — Forgetting That Slicing Excludes the End

```python
server = "web01"

print(server[0:3])
```

This produces:

```text
web
```

not:

```text
web0
```

because index `3` is excluded.

---

## Mistake 4 — Case Sensitivity

These are different:

```python
"ERROR"
"error"
"Error"
```

For case-insensitive comparison:

```python
if log.lower() == "error":
    ...
```

---

# 22. Industry Note

DevOps engineers constantly deal with text.

A typical automation workflow can look like:

```text
Linux command
      ↓
Text output
      ↓
Python string
      ↓
Search / split / clean
      ↓
Extract information
      ↓
Make decision
      ↓
Take action
```

For example, later we can use Python's `subprocess` module to run:

```bash
systemctl status nginx
```

Then Python can process the command's output and determine whether the service is healthy.

That is one of the reasons strings are important before learning `subprocess`.

---

# 23. How This Helps in DevOps

| DevOps Area | String Usage |
|---|---|
| Linux | Process command output |
| Log Analysis | Search and filter logs |
| APIs | Process URLs and text |
| AWS | Process resource names and metadata |
| Docker | Process container output |
| Kubernetes | Process CLI/API information |
| CI/CD | Process build/deployment output |
| Monitoring | Process alert messages |

The important progression is:

```text
Strings
   ↓
Files
   ↓
Logs
   ↓
subprocess
   ↓
Linux Automation
   ↓
Monitoring / SRE
```

---

# 24. Future Roadmap Connection

Strings will be used throughout the rest of the course.

```text
Strings
   ↓
File Handling
   ↓
pathlib
   ↓
os
   ↓
subprocess
   ↓
Environment Variables
   ↓
JSON / YAML
   ↓
Logging
   ↓
Linux Automation
   ↓
APIs
   ↓
AWS boto3
```

They will also appear when working with:

```text
Docker
Kubernetes
Terraform
CI/CD
Monitoring
```

---

# 25. String Methods Learned

| Method / Operator | Purpose |
|---|---|
| `upper()` | Convert to uppercase |
| `lower()` | Convert to lowercase |
| `strip()` | Remove surrounding whitespace |
| `replace()` | Replace text |
| `split()` | Split string into a list |
| `join()` | Combine strings |
| `find()` | Find text position |
| `startswith()` | Check beginning |
| `endswith()` | Check ending |
| `in` | Check whether text exists |

---

# 26. Cheat Sheet

### Create a string

```python
name = "web01"
```

### Access character

```python
name[0]
```

### Negative index

```python
name[-1]
```

### Slice

```python
name[0:3]
```

### Uppercase

```python
name.upper()
```

### Lowercase

```python
name.lower()
```

### Remove surrounding whitespace

```python
name.strip()
```

### Replace text

```python
name.replace("web", "api")
```

### Split

```python
data.split(",")
```

### Join

```python
",".join(items)
```

### Search

```python
"ERROR" in log
```

### Find position

```python
log.find("ERROR")
```

### Check beginning

```python
log.startswith("ERROR")
```

### Check ending

```python
filename.endswith(".log")
```

### Formatted string

```python
f"Server: {server}"
```

---

# 27. Final Mental Model

Remember:

```text
STRING
  │
  ├── Indexing       → get a character
  ├── Slicing        → get part of text
  ├── upper/lower    → change case
  ├── strip          → clean text
  ├── replace        → modify text
  ├── split          → String → List
  ├── join           → List → String
  ├── find           → locate text
  ├── startswith     → check beginning
  ├── endswith       → check ending
  └── in             → search text
```

The most important DevOps connection:

```text
Linux / APIs / Logs
        ↓
      TEXT
        ↓
    Python String
        ↓
 Search / Clean / Extract
        ↓
    Automation
```

---

# 28. Lesson Files

The completed lesson should contain:

```text
Lesson-13-Strings/
├── 01_strings.py
├── 02_strings.md
└── 03_log_analyzer.py
```

---

# 29. Git Workflow

After saving the Markdown file and testing both Python programs:

```bash
python3 01_strings.py
python3 03_log_analyzer.py
```

Check:

```bash
git status
```

Stage:

```bash
git add python-for-devops/Python-lessons/Lesson-13-Strings/
```

Commit:

```bash
git commit -m "Complete Lesson 13: Strings and log analyzer"
```

Push:

```bash
git push
```

---

# 30. Summary

In this lesson we learned:

- What strings are
- String indexing
- Negative indexing
- String slicing
- `upper()`
- `lower()`
- `strip()`
- `replace()`
- `split()`
- `join()`
- `in`
- `find()`
- `startswith()`
- `endswith()`
- f-strings
- Basic log analysis

The most important concepts for DevOps are:

```text
split()
in
find()
startswith()
endswith()
strip()
replace()
```

These will become especially useful when we start working with **Linux files, logs, command output, APIs, and monitoring data**.