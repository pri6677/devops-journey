# Lesson 17 — Python `os` Module

> Python for Cloud & DevOps Engineering

---

## 1. Where I Am in the Python Roadmap

### Phase 1 — Python Foundations

- Lesson 01 — Running Python ✅
- Lesson 02 — Variables ✅
- Lesson 03 — Data Types ✅
- Lesson 04 — Input / Output ✅
- Lesson 05 — Operators ✅
- Lesson 06 — Conditions ✅
- Lesson 07 — Loops ✅
- Lesson 08 — Functions ✅
- Lesson 09 — Error Handling ✅
- Lesson 10 — Lists ✅
- Lesson 11 — Tuples & Sets ✅
- Lesson 12 — Dictionaries ✅
- Lesson 13 — Strings ✅
- Lesson 14 — Modules & Imports ✅

### Phase 2 — Python Automation

- Lesson 15 — File Handling ✅
- Lesson 16 — `pathlib` ✅
- Lesson 17 — `os` Module ✅ **Current**
- Lesson 18 — `subprocess` ⬜
- Lesson 19 — Environment Variables ⬜
- Lesson 20 — JSON ⬜
- Lesson 21 — YAML ⬜
- Lesson 22 — Logging ⬜

---

# 2. Previous Lesson Recap

In Lesson 16, we learned `pathlib`.

`pathlib` is used to work with filesystem paths.

Important examples:

```python
from pathlib import Path

path = Path("server.log")

print(path.exists())
print(path.is_file())
print(path.is_dir())
```

We also learned:

```python
Path.cwd()
Path.home()
path.name
path.parent
path.suffix
path.mkdir()
path.read_text()
path.write_text()
path.iterdir()
path.rglob()
```

The main idea was:

```text
Python
   ↓
pathlib
   ↓
Files + Directories + Paths
```

---

# 3. Practical Problem

A DevOps engineer often needs Python to interact with the operating system.

For example:

```text
Where am I?
What files are here?
Who is the current user?
What is the home directory?
What environment variables are available?
What operating system am I using?
```

Linux can answer these questions:

```bash
pwd
ls
whoami
echo $HOME
```

Python can interact with the operating system using the `os` module.

---

# 4. What Is the `os` Module?

`os` is a Python standard-library module that provides operating-system-related functionality.

Import it with:

```python
import os
```

No separate installation is required.

The `os` module can help Python interact with:

- Files
- Directories
- Environment variables
- Operating-system information
- Processes and system functionality

---

# 5. Why Do We Need It?

A DevOps script often needs information from the machine where it is running.

For example:

```text
Python script
     ↓
Operating system
     ↓
Information / files / environment
     ↓
Python processes the information
     ↓
Automation
```

Without OS interaction, Python would be much less useful for system automation.

---

# 6. Real-World Analogy

Think of Python as a DevOps engineer.

The operating system is the server.

The `os` module is one of the communication tools Python uses to interact with that server.

```text
Python
  │
  │ os module
  ↓
Linux
  │
  ├── Files
  ├── Directories
  ├── Environment
  └── System information
```

---

# 7. Importing `os`

```python
import os
```

### `import`

Tells Python to load a module.

### `os`

The module we want to use.

After importing it, we can access functionality using:

```python
os.something()
```

For example:

```python
os.getcwd()
```

---

# 8. Current Working Directory

Linux command:

```bash
pwd
```

Python:

```python
import os

print(os.getcwd())
```

`getcwd()` means:

```text
get current working directory
```

Example output:

```text
/home/pri/my-journey/devops-journey/python-for-devops/Python-lessons/Lesson-17-OS-Module
```

So:

```text
Linux                     Python

pwd                ↔      os.getcwd()
```

---

# 9. Listing Directory Contents

Linux:

```bash
ls
```

Python:

```python
import os

print(os.listdir())
```

`listdir()` means:

```text
list directory
```

It returns a Python list containing the directory contents.

Example:

```text
['01_os_module.py', '02_os_module.md', '03_system_info.py']
```

This connects directly to the Python list concept we learned earlier.

---

# 10. Listing a Specific Directory

We can specify a directory:

```python
import os

print(os.listdir("/tmp"))
```

This lists the contents of:

```text
/tmp
```

This is useful when an automation script needs to inspect another directory.

---

# 11. Creating a Directory

Python can create a directory:

```python
import os

os.mkdir("logs")
```

After running the program:

```bash
ls
```

you should see:

```text
logs
```

---

# 12. Creating Nested Directories

For multiple levels, use:

```python
import os

os.makedirs("logs/nginx/backups")
```

This can create:

```text
logs/
└── nginx/
    └── backups/
```

---

# 13. `exist_ok=True`

If the directory already exists, this:

```python
os.makedirs("logs/nginx/backups")
```

can produce an error.

We can use:

```python
os.makedirs("logs/nginx/backups", exist_ok=True)
```

`exist_ok=True` means:

> Don't raise an error if the directory already exists.

This is useful for automation scripts that may run repeatedly.

---

# 14. `os` and `pathlib`

There is some overlap between `os` and `pathlib`.

For example:

```python
os.getcwd()
```

and:

```python
from pathlib import Path

Path.cwd()
```

Both can obtain the current working directory.

A useful mental model is:

```text
pathlib
   ↓
Filesystem paths

os
   ↓
Operating-system interaction
```

Modern Python code often uses both.

We will choose the appropriate tool depending on the task.

---

# 15. Environment Variables

Environment variables are values provided by the operating system to processes.

Linux:

```bash
echo $HOME
```

Python:

```python
import os

print(os.environ["HOME"])
```

Example:

```text
/home/pri
```

---

# 16. `os.environ`

`os.environ` provides access to environment variables.

Example:

```python
import os

print(os.environ["USER"])
```

This reads the `USER` environment variable.

On Linux, you can compare it with:

```bash
echo $USER
```

---

# 17. `os.getenv()`

Another way to read an environment variable is:

```python
import os

print(os.getenv("USER"))
```

The advantage is that `getenv()` safely returns `None` when the variable doesn't exist.

Example:

```python
import os

value = os.getenv("DOES_NOT_EXIST")

print(value)
```

Output:

```text
None
```

---

# 18. `os.environ[]` vs `os.getenv()`

### `os.environ[]`

```python
os.environ["USER"]
```

If the variable doesn't exist, Python can raise:

```text
KeyError
```

### `os.getenv()`

```python
os.getenv("USER")
```

If the variable doesn't exist:

```text
None
```

For many automation scripts, `getenv()` is convenient when a variable may not exist.

---

# 19. Setting an Environment Variable in Linux

In the terminal:

```bash
export DEVOPS_ENV="development"
```

Check it:

```bash
echo $DEVOPS_ENV
```

Output:

```text
development
```

Python can read it:

```python
import os

print(os.getenv("DEVOPS_ENV"))
```

Output:

```text
development
```

This becomes very important later for:

- AWS
- Docker
- CI/CD
- Application configuration
- Automation scripts

We will study environment variables properly in Lesson 19.

---

# 20. Operating-System Name

Python can provide the OS interface name:

```python
import os

print(os.name)
```

On Linux, you will normally see:

```text
posix
```

`posix` relates to the standard interface used by Unix-like operating systems.

We do not need to study POSIX deeply yet.

---

# 21. Current User

On Linux, we can get the current user using:

```python
import os

print(os.getenv("USER"))
```

Linux equivalent:

```bash
whoami
```

This is useful when a script needs to know which user is running it.

---

# 22. Running a Linux Command

The `os` module has:

```python
os.system()
```

Example:

```python
import os

os.system("pwd")
```

This executes the Linux command:

```bash
pwd
```

However, `os.system()` is not the tool we will use for serious command automation.

For professional command execution, we will learn:

```python
subprocess
```

in the next lesson.

---

# 23. Mini Project — System Information Script

File:

```text
03_system_info.py
```

Code:

```python
import os

print("===== SYSTEM INFORMATION =====")

print("Operating system:", os.name)
print("Current directory:", os.getcwd())
print("Current user:", os.getenv("USER"))
print("Home directory:", os.getenv("HOME"))

print("\n===== DIRECTORY CONTENTS =====")

for item in os.listdir():
    print(item)
```

Run:

```bash
python3 03_system_info.py
```

Example output:

```text
===== SYSTEM INFORMATION =====
Operating system: posix
Current directory: /home/pri/...
Current user: pri
Home directory: /home/pri

===== DIRECTORY CONTENTS =====
01_os_module.py
02_os_module.md
03_system_info.py
```

The exact output depends on your machine and current directory.

---

# 24. Understanding the Project

## `import os`

```python
import os
```

Loads the `os` module.

## `os.name`

```python
os.name
```

Provides the operating-system interface name.

## `os.getcwd()`

```python
os.getcwd()
```

Gets the current working directory.

## `os.getenv()`

```python
os.getenv("USER")
```

Gets an environment variable.

## `os.listdir()`

```python
os.listdir()
```

Returns the contents of the current directory as a list.

## `for`

```python
for item in os.listdir():
```

Loops through every item in the returned list.

---

# 25. Common Mistakes

## Mistake 1 — Forgetting the Import

Wrong:

```python
print(os.getcwd())
```

Correct:

```python
import os

print(os.getcwd())
```

Without the import:

```text
NameError: name 'os' is not defined
```

---

## Mistake 2 — Accessing a Missing Environment Variable

This can fail:

```python
os.environ["DOES_NOT_EXIST"]
```

because the variable may not exist.

Safer:

```python
os.getenv("DOES_NOT_EXIST")
```

which returns:

```text
None
```

---

## Mistake 3 — Confusing `os` and `pathlib`

Don't think that one completely replaces the other.

Use this mental model:

```text
pathlib → paths

os → operating-system interaction
```

There is some overlap.

---

## Mistake 4 — Wrong Working Directory

If a script cannot find files, first check:

```bash
pwd
```

Then:

```bash
ls
```

You can also check from Python:

```python
print(os.getcwd())
```

---

# 26. Debugging

When filesystem or OS automation fails, follow this process:

### Step 1 — Check your Linux location

```bash
pwd
```

### Step 2 — Check available files

```bash
ls
```

### Step 3 — Check Python's location

```python
import os

print(os.getcwd())
```

### Step 4 — Check environment variables

```python
print(os.getenv("USER"))
print(os.getenv("HOME"))
```

This gives you useful information before changing the code.

---

# 27. Industry Note

Professional DevOps engineers use Python's `os` module when automation needs information or functionality from the operating system.

Common examples include:

```text
Environment detection
Environment variables
Directory inspection
Directory creation
System information
Process-related operations
Linux automation
Configuration handling
```

In real projects, `os` is often combined with:

```text
pathlib
subprocess
logging
json
yaml
boto3
```

---

# 28. How This Helps in DevOps

The progression is:

```text
Python
   ↓
pathlib
   ↓
Files + Paths
   ↓
os
   ↓
Operating System
   ↓
Linux Automation
```

Soon we will add:

```text
subprocess
   ↓
Execute Linux commands
   ↓
Capture command output
   ↓
Automate servers
```

---

# 29. Future DevOps Connections

Our automation roadmap is becoming:

```text
File Handling              ✅
      ↓
pathlib                    ✅
      ↓
os Module                  ✅
      ↓
subprocess                 NEXT
      ↓
Environment Variables
      ↓
JSON
      ↓
YAML
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

---

# 30. Cheat Sheet

## Import

```python
import os
```

## Current directory

```python
os.getcwd()
```

## List directory

```python
os.listdir()
```

## List specific directory

```python
os.listdir("/tmp")
```

## Create directory

```python
os.mkdir("logs")
```

## Create nested directories

```python
os.makedirs("logs/nginx/backups")
```

## Avoid error if directory exists

```python
os.makedirs("logs", exist_ok=True)
```

## Environment variable

```python
os.environ["USER"]
```

## Safer environment variable access

```python
os.getenv("USER")
```

## OS interface name

```python
os.name
```

## Execute a simple command

```python
os.system("pwd")
```

For serious command execution:

```python
subprocess
```

---

# 31. Key Concepts to Remember

The most important concepts are:

```text
import os
os.getcwd()
os.listdir()
os.mkdir()
os.makedirs()
os.environ
os.getenv()
os.name
```

Especially:

```python
os.getenv("VARIABLE_NAME")
```

Environment variables will become very important in DevOps.

---

# 32. Final Mental Model

Think of `os` as a bridge between Python and the operating system:

```text
                  Python
                     │
                     ↓
                  os module
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Files     Environment    OS
          │          │          │
          ↓          ↓          ↓
    Directories  Variables   Information
          │          │          │
          └──────────┼──────────┘
                     ↓
             DevOps Automation
```

---

# 33. Lesson Summary

In this lesson we learned:

- What the `os` module is
- How to import `os`
- `os.getcwd()`
- `os.listdir()`
- `os.mkdir()`
- `os.makedirs()`
- `exist_ok=True`
- `os.environ`
- `os.getenv()`
- `os.name`
- Environment variables
- Basic operating-system interaction
- Why `subprocess` is preferred for serious command execution
- How `os` connects Python to Linux and DevOps

The key progression is:

```text
File Handling
      ↓
pathlib
      ↓
os
      ↓
Operating-System Automation
```

---

# 34. Lesson Files

The lesson structure is:

```text
Lesson-17-OS-Module/
├── 01_os_module.py
├── 02_os_module.md
└── 03_system_info.py
```

---

# 35. GitHub Integration

Repository:

```text
devops-journey/
└── python-for-devops/
    └── Python-lessons/
        └── Lesson-17-OS-Module/
```

Files:

```text
01_os_module.py
02_os_module.md
03_system_info.py
```

The two important GitHub portfolio components are:

1. Detailed lesson notes:
   ```text
   02_os_module.md
   ```

2. Practical project:
   ```text
   03_system_info.py
   ```

---

# 36. Git Workflow

After testing the programs:

```bash
python3 01_os_module.py
python3 03_system_info.py
```

Go to the repository:

```bash
cd ~/my-journey/devops-journey
```

Check:

```bash
git status
```

Stage:

```bash
git add python-for-devops/Python-lessons/Lesson-17-OS-Module/
```

Commit:

```bash
git commit -m "Complete Lesson 17: os module and system info"
```

Push:

```bash
git push
```

---

# 37. Next Lesson

## Lesson 18 — `subprocess`

We will learn how Python can execute Linux commands and capture their output.

The basic architecture will be:

```text
Python
   ↓
subprocess
   ↓
Linux command
   ↓
Command output
   ↓
Python
```

This is a major step toward real Linux and DevOps automation.