# Lesson 14 — Modules and Imports

> Python for Cloud & DevOps Engineering

---

## 1. Where I Am in the Python Roadmap

We are currently in:

**Phase 1 — Python Foundations**

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
Lesson 13 — Strings               ✅
Lesson 14 — Modules & Imports     ✅ CURRENT
```

---

# 2. Practical Problem

A DevOps automation project can become very large.

For example:

```text
automation/
├── main.py
├── linux.py
├── files.py
├── network.py
├── monitoring.py
└── aws.py
```

Putting everything into one Python file would make the project difficult to maintain.

Python allows us to divide code into separate files and reuse it.

This is where **modules** and **imports** are used.

---

# 3. What Is a Module?

A module is a Python file containing reusable Python code.

For example:

```text
server_tools.py
```

could contain:

```python
def show_server(name, ip):
    print(f"Server: {name}")
    print(f"IP: {ip}")
```

Another Python program can import this module and use the function.

---

# 4. Real-World Analogy

Think of a toolbox.

Instead of carrying every tool separately, you keep tools organized:

```text
Toolbox
│
├── screwdriver
├── hammer
├── wrench
└── pliers
```

Python modules work similarly:

```text
Python project
│
├── server_tools.py
├── file_tools.py
├── network_tools.py
└── monitoring_tools.py
```

Each module contains related functionality.

---

# 5. The `import` Keyword

To use a module, we can write:

```python
import os
```

`import` tells Python:

> Load this module so I can use its functionality.

Example:

```python
import os

print(os.getcwd())
```

---

# 6. Understanding the Dot

Look at:

```python
os.getcwd()
```

There are several parts:

```text
os
 ↓
module

.
 ↓
access something inside the module

getcwd
 ↓
function

()
 ↓
call the function
```

Therefore:

```python
os.getcwd()
```

means:

> Call the `getcwd()` function from the `os` module.

---

# 7. The `os` Module

Python provides a standard-library module called `os`.

It provides functionality for interacting with the operating system.

Example:

```python
import os

print(os.getcwd())
```

`getcwd()` means:

**Get Current Working Directory**

Example output:

```text
/home/pri/my-journey/devops-journey
```

The exact path depends on where the program is executed.

---

# 8. Multiple Imports

We can import multiple modules:

```python
import os
import sys
```

Then:

```python
print(os.getcwd())
print(sys.version)
```

The `sys` module provides functionality related to the Python runtime and system environment.

---

# 9. Importing Specific Functions

Instead of:

```python
import os
```

we can write:

```python
from os import getcwd
```

Then:

```python
print(getcwd())
```

The syntax is:

```python
from module import thing
```

For our beginner DevOps code, we'll generally prefer:

```python
import os
```

because:

```python
os.getcwd()
```

makes it immediately clear where `getcwd()` came from.

---

# 10. Import Aliases

Python allows an alias:

```python
import os as operating_system
```

Then:

```python
print(operating_system.getcwd())
```

The syntax is:

```python
import module as alias
```

Aliases are useful in some situations, but don't use them unnecessarily.

---

# 11. Python Standard Library

Python comes with many useful modules.

These modules are part of the **Python Standard Library**.

Important modules for our DevOps roadmap include:

| Module | Purpose |
|---|---|
| `os` | Operating-system interaction |
| `pathlib` | Files and directories |
| `subprocess` | Execute external commands |
| `json` | JSON data |
| `logging` | Application and automation logs |
| `sys` | Python runtime/system information |
| `shutil` | High-level file operations |
| `datetime` | Dates and times |
| `re` | Pattern matching |

We will study these when they become relevant.

---

# 12. Creating Our Own Module

We can create our own Python module.

File:

```text
server_tools.py
```

Code:

```python
def show_server(name, ip):
    print(f"Server: {name}")
    print(f"IP: {ip}")
```

Another Python file can use it.

File:

```text
03_use_server_tools.py
```

Code:

```python
import server_tools

server_tools.show_server("web-01", "10.0.0.10")
```

Output:

```text
Server: web-01
IP: 10.0.0.10
```

---

# 13. Why the Files Need to Be Located Correctly

For this simple module example, our files are:

```text
Lesson-14-Modules-Imports/
├── server_tools.py
└── 03_use_server_tools.py
```

When Python sees:

```python
import server_tools
```

it needs to be able to locate:

```text
server_tools.py
```

If the file isn't available in Python's module search path, Python can raise:

```text
ModuleNotFoundError
```

---

# 14. The Error We Encountered

We received:

```text
ModuleNotFoundError: No module named 'server_tools'
```

The problem was that:

```text
03_use_server_tools.py
```

was accidentally created in:

```text
Python-lessons/
```

while:

```text
server_tools.py
```

was inside:

```text
Lesson-14-Modules-Imports/
```

Correct structure:

```text
Lesson-14-Modules-Imports/
├── server_tools.py
└── 03_use_server_tools.py
```

After moving the file into the correct directory, Python can find the module.

---

# 15. Mini Project — System Information Tool

File:

```text
04_system_info.py
```

Code:

```python
import os
import sys

print("========== SYSTEM INFORMATION ==========")

print(f"Current directory: {os.getcwd()}")
print(f"Operating system: {os.name}")
print(f"Python version: {sys.version}")

print("=========================================")
```

This is a small DevOps-style utility.

It demonstrates how Python can inspect information about the environment where the script runs.

---

# 16. Common Mistakes

## Mistake 1 — Forgetting `import`

Wrong:

```python
print(os.getcwd())
```

Correct:

```python
import os

print(os.getcwd())
```

Without importing `os`, Python doesn't know what `os` refers to.

This can produce:

```text
NameError: name 'os' is not defined
```

---

## Mistake 2 — Module Doesn't Exist

If you write:

```python
import something
```

but Python cannot find `something`, you may get:

```text
ModuleNotFoundError
```

---

## Mistake 3 — Module Is in the Wrong Location

For our simple custom-module example:

```text
Python-lessons/
├── 03_use_server_tools.py
│
└── Lesson-14-Modules-Imports/
    └── server_tools.py
```

can cause:

```text
ModuleNotFoundError
```

Keep them together:

```text
Lesson-14-Modules-Imports/
├── 03_use_server_tools.py
└── server_tools.py
```

---

# 17. Industry Note

Professional Python automation projects are rarely one giant file.

A project might be organized like:

```text
devops_automation/
│
├── main.py
├── linux_tools.py
├── file_tools.py
├── network_tools.py
├── monitoring.py
└── aws_tools.py
```

Each module has a specific responsibility.

This makes the project:

- Easier to understand
- Easier to maintain
- Easier to test
- Easier to reuse

---

# 18. How This Helps in DevOps

Modules are the bridge between basic Python and real automation.

```text
Modules
   ↓
os
   ↓
Linux interaction

pathlib
   ↓
Files and directories

subprocess
   ↓
Linux commands

json
   ↓
API/configuration data

logging
   ↓
Automation logging

boto3
   ↓
AWS automation
```

---

# 19. Connection to the Future Roadmap

### Linux

```text
Python
  ↓
os
  ↓
Linux system information
```

### AWS

```text
Python
  ↓
boto3
  ↓
AWS APIs
```

### Docker

Python can interact with Docker APIs and automation tools.

### Kubernetes

Python can use Kubernetes libraries and APIs.

### Terraform

Python can automate surrounding infrastructure workflows.

### CI/CD

Python scripts can perform build, deployment, validation, and reporting tasks.

### Monitoring

Python modules can collect, process, and report monitoring information.

---

# 20. Lesson Files

The completed directory should contain:

```text
Lesson-14-Modules-Imports/
├── 01_modules.py
├── 02_modules.md
├── server_tools.py
├── 03_use_server_tools.py
└── 04_system_info.py
```

---

# 21. Testing

Run:

```bash
python3 01_modules.py
```

Then:

```bash
python3 03_use_server_tools.py
```

Expected:

```text
Server: web-01
IP: 10.0.0.10
```

Then:

```bash
python3 04_system_info.py
```

You should see system and Python information.

---

# 22. Cheat Sheet

### Import a module

```python
import os
```

### Use something from a module

```python
os.getcwd()
```

### Import a specific function

```python
from os import getcwd
```

### Import with alias

```python
import os as operating_system
```

### Import your own module

```python
import server_tools
```

### Use a function from your module

```python
server_tools.show_server("web-01", "10.0.0.10")
```

---

# 23. Key Takeaways

Remember:

1. A module is a Python file containing reusable code.
2. `import` loads a module for use.
3. `.` accesses something inside a module.
4. `()` calls a function.
5. Python includes a large Standard Library.
6. `os` is useful for operating-system interaction.
7. We can create our own modules.
8. Python must be able to find imported modules.
9. Large projects should be divided into logical modules.
10. Modules will become extremely important for DevOps automation.

---

# 24. Final Mental Model

```text
Python Program
      │
      ├── import os
      │       ↓
      │    OS tools
      │
      ├── import pathlib
      │       ↓
      │    File tools
      │
      ├── import subprocess
      │       ↓
      │    Linux commands
      │
      ├── import json
      │       ↓
      │    Structured data
      │
      └── import boto3
              ↓
           AWS automation
```

The goal isn't simply to memorize `import`.

The goal is to understand:

> **Python programs can be built from reusable pieces of code.**

That idea becomes essential as our DevOps projects become larger.

---

# 25. GitHub Workflow

After testing all files:

```bash
cd ~/my-journey/devops-journey

git status
```

Stage the complete lesson:

```bash
git add python-for-devops/Python-lessons/Lesson-14-Modules-Imports/
```

Commit:

```bash
git commit -m "Complete Lesson 14: Modules and imports"
```

Push:

```bash
git push
```

---

# 26. Lesson 14 Summary

```text
Modules
   ↓
import
   ↓
Reuse code
   ↓
Organize projects
   ↓
Use Python Standard Library
   ↓
Linux / Files / Commands / APIs / AWS
```

**Lesson 14 is complete when the five files are inside `Lesson-14-Modules-Imports/` and all three Python programs run successfully.**