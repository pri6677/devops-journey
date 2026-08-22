# Lesson 15 — File Handling

> Python for Cloud & DevOps Engineering

---

# 1. Where I Am in the Python Roadmap

We have completed the core Python fundamentals and are now moving deeper into Python automation.

```text
PHASE 1 — PYTHON FOUNDATIONS

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
Lesson 13 — Strings               ✅
Lesson 14 — Modules & Imports     ✅

PHASE 2 — PYTHON AUTOMATION

Lesson 15 — File Handling         ✅ CURRENT
Lesson 16 — pathlib                ⬜
Lesson 17 — os Module              ⬜
Lesson 18 — subprocess              ⬜
Lesson 19 — Environment Variables ⬜
Lesson 20 — JSON                   ⬜
Lesson 21 — YAML                   ⬜
Lesson 22 — Logging                ⬜
```

---

# 2. Previous Lesson Recap

In Lesson 14, we learned about modules and imports.

We learned:

```python
import os
```

and:

```python
os.getcwd()
```

We also created our own module:

```text
server_tools.py
```

and imported it using:

```python
import server_tools
```

Modules allow us to organize reusable Python code into separate files.

---

# 3. Practical Problem

DevOps engineers work with files constantly.

A Linux server may contain:

```text
/var/log/
├── syslog
├── auth.log
└── nginx/
    ├── access.log
    └── error.log
```

Automation scripts may need to:

- Read logs
- Search for errors
- Create reports
- Write configuration files
- Create backups
- Append information to logs
- Process text files

Doing this manually is inefficient.

Python can automate these tasks.

---

# 4. What Is File Handling?

File handling means using Python to interact with files.

Python can:

```text
Create
Read
Write
Append
Modify
Process
```

files.

The basic function we use is:

```python
open()
```

---

# 5. Opening a File

Basic syntax:

```python
open("filename.txt")
```

A more explicit example:

```python
file = open("server.log", "r")
```

Here:

```text
open()      → opens the file
server.log  → filename
"r"         → read mode
```

However, the preferred pattern is:

```python
with open("server.log", "r") as file:
    ...
```

---

# 6. Reading a File

Example:

```python
with open("server.log", "r") as file:
    content = file.read()

print(content)
```

`read()` reads the contents of the file.

The basic flow is:

```text
server.log
    ↓
open()
    ↓
read()
    ↓
Python string
```

The contents of the file become a Python string.

---

# 7. Understanding `with`

Consider:

```python
with open("server.log", "r") as file:
    content = file.read()
```

The `with` statement manages the file for us.

After the `with` block finishes, Python handles closing the file.

This is safer and cleaner than manually managing the file.

The general pattern is:

```python
with open("file") as variable:
    # work with the file
```

---

# 8. Reading Line by Line

A file can contain many lines.

Instead of loading the entire file at once, we can process it line by line:

```python
with open("server.log", "r") as file:
    for line in file:
        print(line.strip())
```

Here we combine:

```text
File handling
+
for loop
+
string method
```

This is useful for processing large log files.

---

# 9. Why Line-by-Line Processing Matters

Imagine a log file is:

```text
5 GB
```

Reading the entire file into memory may be inefficient.

Instead:

```text
5 GB log
   ↓
Read one line
   ↓
Process it
   ↓
Read next line
   ↓
Process it
```

This is a useful pattern for log analysis.

---

# 10. Writing to a File

Use write mode:

```python
with open("report.txt", "w") as file:
    file.write("Server health check completed\n")
```

Then:

```bash
cat report.txt
```

Output:

```text
Server health check completed
```

---

# 11. The `"w"` Mode

`"w"` means:

```text
write
```

Important:

If the file already exists, `"w"` can overwrite its existing contents.

For example:

```python
with open("report.txt", "w") as file:
    file.write("New report")
```

Existing content may be replaced.

Therefore, be careful when using `"w"` on important files.

---

# 12. Appending to a File

Use:

```python
"a"
```

which means:

```text
append
```

Example:

```python
with open("report.txt", "a") as file:
    file.write("CPU usage: 42%\n")
```

This adds the new text to the end of the file.

It does not replace the existing content.

---

# 13. File Modes

Important file modes:

| Mode | Meaning |
|---|---|
| `"r"` | Read |
| `"w"` | Write / overwrite |
| `"a"` | Append |
| `"x"` | Create a new file |
| `"r+"` | Read and write |

For now, focus mainly on:

```text
r → read
w → write
a → append
```

The other modes can be learned when required.

---

# 14. Creating a Test Log

Our lesson uses:

```text
server.log
```

Example contents:

```text
INFO: Server started
ERROR: Disk full
INFO: Backup completed
ERROR: Connection refused
WARNING: CPU usage high
```

We can create it from the terminal:

```bash
cat > server.log <<'EOF'
INFO: Server started
ERROR: Disk full
INFO: Backup completed
ERROR: Connection refused
WARNING: CPU usage high
EOF
```

Check it:

```bash
cat server.log
```

---

# 15. Searching a File

We can combine file handling with strings and conditions.

Example:

```python
with open("server.log", "r") as file:
    for line in file:
        if "ERROR" in line:
            print(line.strip())
```

Output:

```text
ERROR: Disk full
ERROR: Connection refused
```

This is a basic log-analysis technique.

---

# 16. Why `strip()`?

When reading lines from a file, each line normally contains a newline character:

```text
\n
```

For example:

```python
line = "ERROR: Disk full\n"
```

Using:

```python
line.strip()
```

removes surrounding whitespace, including the newline.

Therefore:

```python
print(line.strip())
```

produces cleaner output.

---

# 17. Combining Previous Concepts

This lesson demonstrates how previous concepts start working together.

```text
File Handling
      +
Strings
      +
Loops
      +
Conditions
      +
Variables
      ↓
Real Automation
```

Example:

```python
error_count = 0

with open("server.log", "r") as file:
    for line in file:
        line = line.strip()

        if "ERROR" in line:
            print(line)
            error_count += 1

print(f"Total errors: {error_count}")
```

This is much closer to real DevOps scripting than isolated syntax exercises.

---

# 18. Mini Project — Log File Analyzer

File:

```text
03_log_file_analyzer.py
```

Code:

```python
error_count = 0

with open("server.log", "r") as file:
    for line in file:
        line = line.strip()

        if "ERROR" in line:
            print(f"ERROR FOUND: {line}")
            error_count += 1

print("----------------------------")
print(f"Total errors: {error_count}")
```

Run:

```bash
python3 03_log_file_analyzer.py
```

Expected output:

```text
ERROR FOUND: ERROR: Disk full
ERROR FOUND: ERROR: Connection refused
----------------------------
Total errors: 2
```

---

# 19. Understanding the Project

Let's break down the program.

### Step 1

```python
error_count = 0
```

Creates a variable to keep track of the number of errors.

---

### Step 2

```python
with open("server.log", "r") as file:
```

Opens the log file in read mode.

---

### Step 3

```python
for line in file:
```

Processes the file one line at a time.

---

### Step 4

```python
line = line.strip()
```

Removes surrounding whitespace and the newline.

---

### Step 5

```python
if "ERROR" in line:
```

Checks whether the line contains the word:

```text
ERROR
```

---

### Step 6

```python
error_count += 1
```

Increases the error counter by one.

This is equivalent to:

```python
error_count = error_count + 1
```

---

### Step 7

```python
print(f"Total errors: {error_count}")
```

Uses an f-string to display the final result.

---

# 20. Common Mistakes

## Mistake 1 — File Doesn't Exist

Example:

```python
with open("missing.log", "r") as file:
```

If the file doesn't exist, Python raises:

```text
FileNotFoundError
```

This is a very common automation error.

---

## Mistake 2 — Wrong Working Directory

Suppose the file is:

```text
Lesson-15-File-Handling/
└── server.log
```

but you run Python from:

```text
Python-lessons/
```

Then:

```python
open("server.log")
```

may fail.

Why?

Because `"server.log"` is a relative path.

Python searches relative to the current working directory.

Check your current directory with:

```bash
pwd
```

---

## Mistake 3 — Accidentally Overwriting a File

This:

```python
open("report.txt", "w")
```

can overwrite existing content.

Use:

```python
"a"
```

when you want to append.

---

## Mistake 4 — Forgetting `with`

Technically, this works:

```python
file = open("server.log", "r")
content = file.read()
file.close()
```

But for normal file handling, prefer:

```python
with open("server.log", "r") as file:
    content = file.read()
```

because the `with` statement handles cleanup automatically.

---

# 21. Debugging Challenge

Suppose this code produces:

```text
FileNotFoundError
```

```python
with open("server.log", "r") as file:
    print(file.read())
```

Check:

```bash
pwd
ls
```

Then ask:

```text
Is server.log actually in my current directory?
```

If not, either:

- move into the correct directory
- or provide the correct path

This is an important Linux + Python debugging skill.

---

# 22. Industry Note

Professional DevOps engineers frequently automate tasks involving files.

Examples:

```text
Log processing
Backup scripts
Configuration management
Report generation
Deployment files
Monitoring data
Temporary files
```

However, professional scripts usually become more robust than our current examples.

Later we'll learn:

```text
pathlib
exception handling
logging
configuration
environment variables
```

These allow us to build safer and more reusable automation.

---

# 23. How This Helps in DevOps

File handling is one of the first genuinely useful automation skills.

### Linux Automation

```text
Linux files
    ↓
Python
    ↓
Read / modify / create
```

### Monitoring

```text
Log file
    ↓
Python
    ↓
Search errors
    ↓
Generate report
```

### Backup Automation

```text
Important files
    ↓
Python
    ↓
Copy / archive
    ↓
Backup
```

### CI/CD

```text
Build output
    ↓
Python
    ↓
Read / analyze
    ↓
Success / failure
```

---

# 24. Future DevOps Connections

Our roadmap will eventually look like:

```text
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
API Automation
      ↓
AWS boto3
      ↓
Docker
      ↓
Kubernetes
      ↓
Monitoring
      ↓
CI/CD
```

File handling is therefore not an isolated Python topic.

It becomes part of many later automation projects.

---

# 25. Industry Best Practice

For normal file operations, prefer:

```python
with open("file.txt", "r") as file:
    ...
```

instead of manually opening and closing files.

Keep file processing simple and readable.

For large files, process line by line when possible:

```python
with open("server.log", "r") as file:
    for line in file:
        ...
```

Avoid loading huge files into memory unnecessarily.

---

# 26. Lesson Files

The final directory should look like:

```text
Lesson-15-File-Handling/
├── 01_file_handling.py
├── 02_file_handling.md
├── 03_log_file_analyzer.py
└── server.log
```

---

# 27. Cheat Sheet

## Open for reading

```python
with open("file.txt", "r") as file:
    content = file.read()
```

## Read line by line

```python
with open("file.txt", "r") as file:
    for line in file:
        print(line)
```

## Write

```python
with open("file.txt", "w") as file:
    file.write("Hello\n")
```

## Append

```python
with open("file.txt", "a") as file:
    file.write("New line\n")
```

## Remove whitespace

```python
line.strip()
```

## Search text

```python
if "ERROR" in line:
    ...
```

## Count errors

```python
error_count += 1
```

---

# 28. Key Concepts

Remember these:

```text
open()
with
"r"
"w"
"a"
read()
write()
strip()
```

And especially:

```python
with open("file.txt", "r") as file:
```

This will become a very common pattern in your automation scripts.

---

# 29. Final Mental Model

Think of file automation like this:

```text
             Linux Server
                  │
                  ↓
              File / Log
                  │
                  ↓
             Python open()
                  │
          ┌───────┴────────┐
          ↓                ↓
        read()           write()
          │                │
          ↓                ↓
       Analyze          Generate
          │                │
          └───────┬────────┘
                  ↓
             Automation
```

For log analysis:

```text
Log file
   ↓
Read line
   ↓
Clean line
   ↓
Search "ERROR"
   ↓
Count errors
   ↓
Generate result
```

---

# 30. Lesson Summary

In this lesson we learned:

- What file handling is
- `open()`
- `with`
- Read mode `"r"`
- Write mode `"w"`
- Append mode `"a"`
- `read()`
- `write()`
- Reading line by line
- `strip()`
- Relative paths
- `FileNotFoundError`
- Searching files
- Building a basic log analyzer

Most importantly, we combined previous Python concepts:

```text
Variables
+
Loops
+
Conditions
+
Strings
+
File Handling
        ↓
DevOps Automation
```

---

# 31. GitHub Workflow

After testing the lesson:

```bash
python3 01_file_handling.py
python3 03_log_file_analyzer.py
```

Check the files:

```bash
ls
```

Expected:

```text
01_file_handling.py
02_file_handling.md
03_log_file_analyzer.py
server.log
```

Go to the repository root:

```bash
cd ~/my-journey/devops-journey
```

Check Git:

```bash
git status
```

Stage the complete lesson:

```bash
git add python-for-devops/Python-lessons/Lesson-15-File-Handling/
```

Commit:

```bash
git commit -m "Complete Lesson 15: File handling and log analyzer"
```

Push:

```bash
git push
```

---

# 32. Next Lesson

The next lesson is:

```text
Lesson 16 — pathlib
```

We will improve our file and directory automation.

Instead of relying heavily on strings such as:

```python
"logs/server.log"
```

we'll learn a cleaner way to work with paths:

```python
Path("logs") / "server.log"
```

This will be especially useful for:

- Linux automation
- File management
- Backups
- Log processing
- Infrastructure scripts
- Cross-platform Python scripts