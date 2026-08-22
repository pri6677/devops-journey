# Lesson 16 — pathlib

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
- Lesson 16 — pathlib ✅ **Current**
- Lesson 17 — os Module ⬜
- Lesson 18 — subprocess ⬜
- Lesson 19 — Environment Variables ⬜
- Lesson 20 — JSON ⬜
- Lesson 21 — YAML ⬜
- Lesson 22 — Logging ⬜

---

# 2. Previous Lesson Recap

In Lesson 15, we learned how Python works with files.

Important concepts:

```python
open()
```

```python
with open("server.log", "r") as file:
    content = file.read()
```

We learned:

- Reading files
- Writing files
- Appending to files
- Reading files line by line
- `read()`
- `write()`
- `strip()`
- File modes
- `FileNotFoundError`

We also created a basic log analyzer.

The main idea was:

```text
File
 ↓
Python
 ↓
Read / Process
 ↓
Automation
```

---

# 3. Practical Problem

DevOps engineers work with many files and directories.

For example:

```text
logs/
├── nginx/
│   ├── access.log
│   └── error.log
├── application/
│   └── app.log
└── system.log
```

A Python automation script may need to:

- Check whether a file exists
- Create directories
- Find log files
- Get file names
- Get file extensions
- Build file paths
- Search directories
- Create backup directories

We could construct paths manually using strings:

```python
"log" + "/" + "nginx" + "/" + "error.log"
```

But this quickly becomes difficult to manage.

Python provides `pathlib` to make filesystem paths easier to work with.

---

# 4. What Is pathlib?

`pathlib` is a Python module for working with filesystem paths.

It provides tools for working with:

- Files
- Directories
- Paths
- File existence
- File types
- Directory contents

We import it using:

```python
from pathlib import Path
```

---

# 5. Understanding the Import

```python
from pathlib import Path
```

### `from`

Means we want something from a module.

### `pathlib`

The Python module containing filesystem path functionality.

### `import`

Brings something into our Python program.

### `Path`

The object we use to represent and work with paths.

For now, think of `Path` as:

> A Python-friendly representation of a filesystem path.

We will study classes in more detail later.

---

# 6. Creating a Path

Example:

```python
from pathlib import Path

path = Path("server.log")

print(path)
```

Output:

```text
server.log
```

The `Path` object represents:

```text
server.log
```

---

# 7. Checking Whether a Path Exists

Use:

```python
path.exists()
```

Example:

```python
from pathlib import Path

path = Path("server.log")

print(path.exists())
```

If the file exists:

```text
True
```

If it doesn't exist:

```text
False
```

This is very useful in automation.

Instead of blindly trying to use a file, our script can check first.

---

# 8. Checking Whether Something Is a File

Use:

```python
path.is_file()
```

Example:

```python
from pathlib import Path

path = Path("server.log")

print(path.is_file())
```

If `server.log` is a file:

```text
True
```

---

# 9. Checking Whether Something Is a Directory

Use:

```python
path.is_dir()
```

Example:

```python
from pathlib import Path

path = Path("logs")

print(path.is_dir())
```

If `logs` is a directory:

```text
True
```

---

# 10. File vs Directory

These methods are useful for automation:

```python
path.exists()
```

Checks whether the path exists.

```python
path.is_file()
```

Checks whether the path points to a file.

```python
path.is_dir()
```

Checks whether the path points to a directory.

Mental model:

```text
Path
 │
 ├── exists()
 │
 ├── is_file()
 │
 └── is_dir()
```

---

# 11. Current Working Directory

Use:

```python
Path.cwd()
```

`cwd` means:

```text
Current Working Directory
```

Example:

```python
from pathlib import Path

current = Path.cwd()

print(current)
```

This is similar to the Linux command:

```bash
pwd
```

The Python version:

```python
Path.cwd()
```

The Linux version:

```bash
pwd
```

---

# 12. Home Directory

Use:

```python
Path.home()
```

Example:

```python
from pathlib import Path

home = Path.home()

print(home)
```

This returns the current user's home directory.

For example:

```text
/home/pri
```

---

# 13. Building Paths

This is one of the most important features of `pathlib`.

Instead of:

```python
"log" + "/" + "nginx" + "/" + "error.log"
```

we can write:

```python
from pathlib import Path

log_file = Path("logs") / "nginx" / "error.log"

print(log_file)
```

Output:

```text
logs/nginx/error.log
```

The `/` here does **not** mean mathematical division.

With `Path` objects, `/` joins path components.

---

# 14. Why Path Joining Is Useful

Instead of:

```python
path = "logs/" + server + "/" + filename
```

we can write:

```python
path = Path("logs") / server / filename
```

Example:

```python
from pathlib import Path

server = "nginx"
filename = "error.log"

path = Path("logs") / server / filename

print(path)
```

Output:

```text
logs/nginx/error.log
```

This is cleaner and easier to maintain.

---

# 15. Creating a Directory

`pathlib` can create directories.

Example:

```python
from pathlib import Path

directory = Path("logs")

directory.mkdir()
```

After running the program:

```bash
ls
```

You should see:

```text
logs
```

---

# 16. `exist_ok=True`

If the directory already exists:

```python
directory.mkdir()
```

can produce an error.

We can use:

```python
directory.mkdir(exist_ok=True)
```

This means:

> Create the directory if it doesn't exist, but don't raise an error if it already exists.

This is useful for automation scripts because scripts are often run repeatedly.

---

# 17. Creating Nested Directories

Suppose we want:

```text
logs/
└── nginx/
    └── backups/
```

We can write:

```python
from pathlib import Path

backup_dir = Path("logs") / "nginx" / "backups"

backup_dir.mkdir(parents=True, exist_ok=True)
```

### `parents=True`

Allows Python to create the required parent directories.

So Python can create:

```text
logs/
logs/nginx/
logs/nginx/backups/
```

if they don't already exist.

---

# 18. Reading a Text File

`pathlib` can also read text files.

Example:

```python
from pathlib import Path

log_file = Path("server.log")

content = log_file.read_text()

print(content)
```

This reads the file contents into a Python string.

This is another way to perform simple file reading.

---

# 19. Writing a Text File

We can also write text:

```python
from pathlib import Path

report = Path("report.txt")

report.write_text("Server health check completed\n")
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

# 20. Getting the File Name

Suppose:

```python
from pathlib import Path

path = Path("/var/log/nginx/error.log")

print(path.name)
```

Output:

```text
error.log
```

`.name` gives the final filename.

---

# 21. Getting the Parent Directory

Example:

```python
from pathlib import Path

path = Path("/var/log/nginx/error.log")

print(path.parent)
```

Output:

```text
/var/log/nginx
```

Therefore:

```text
path.name
    ↓
error.log

path.parent
    ↓
/var/log/nginx
```

---

# 22. Getting the File Extension

Use:

```python
path.suffix
```

Example:

```python
from pathlib import Path

path = Path("/var/log/nginx/error.log")

print(path.suffix)
```

Output:

```text
.log
```

This is useful when processing files based on their type.

Examples:

```text
.log
.txt
.json
.yaml
.py
```

---

# 23. Listing Directory Contents

Use:

```python
path.iterdir()
```

Example:

```python
from pathlib import Path

directory = Path("logs")

for item in directory.iterdir():
    print(item)
```

`iterdir()` allows us to iterate through the contents of a directory.

If:

```text
logs/
├── server.log
├── application.log
└── config.txt
```

the program can print the items inside the directory.

---

# 24. Finding Log Files

We can combine `iterdir()` with `suffix`.

```python
from pathlib import Path

log_directory = Path("logs")

for file in log_directory.iterdir():
    if file.suffix == ".log":
        print(file)
```

This prints files ending in:

```text
.log
```

This is a basic form of automation.

---

# 25. Recursive Search with `rglob()`

Suppose our directory looks like:

```text
logs/
├── nginx/
│   └── access.log
├── app/
│   └── app.log
└── system.log
```

We can search all directories recursively:

```python
from pathlib import Path

log_directory = Path("logs")

for file in log_directory.rglob("*.log"):
    print(file)
```

`rglob()` searches recursively.

It can find:

```text
logs/system.log
logs/nginx/access.log
logs/app/app.log
```

This is extremely useful for log-analysis automation.

---

# 26. Mini Project — File Manager

Create:

```text
03_file_manager.py
```

Code:

```python
from pathlib import Path

base_dir = Path("devops_files")

logs_dir = base_dir / "logs"
backups_dir = base_dir / "backups"

logs_dir.mkdir(parents=True, exist_ok=True)
backups_dir.mkdir(parents=True, exist_ok=True)

log_file = logs_dir / "server.log"

if not log_file.exists():
    log_file.write_text("INFO: Server started\n")

print("DevOps directory structure:")
print(base_dir)

for item in base_dir.rglob("*"):
    print(item)
```

---

# 27. How the Project Works

### Step 1 — Create the base directory

```python
base_dir = Path("devops_files")
```

Creates a `Path` object representing:

```text
devops_files/
```

---

### Step 2 — Build the logs path

```python
logs_dir = base_dir / "logs"
```

Result:

```text
devops_files/logs
```

---

### Step 3 — Build the backup path

```python
backups_dir = base_dir / "backups"
```

Result:

```text
devops_files/backups
```

---

### Step 4 — Create directories

```python
logs_dir.mkdir(parents=True, exist_ok=True)
backups_dir.mkdir(parents=True, exist_ok=True)
```

The required directories are created.

---

### Step 5 — Build the log file path

```python
log_file = logs_dir / "server.log"
```

Result:

```text
devops_files/logs/server.log
```

---

### Step 6 — Check if the log exists

```python
if not log_file.exists():
```

`not` reverses the Boolean result.

So:

```python
log_file.exists()
```

means:

```text
Does it exist?
```

while:

```python
not log_file.exists()
```

means:

```text
Does it NOT exist?
```

---

### Step 7 — Create the log

```python
log_file.write_text("INFO: Server started\n")
```

Creates the file if it doesn't exist.

---

### Step 8 — Search everything

```python
for item in base_dir.rglob("*"):
```

`rglob("*")` recursively searches everything under `base_dir`.

---

# 28. Resulting Structure

After running:

```bash
python3 03_file_manager.py
```

you should have:

```text
devops_files/
├── logs/
│   └── server.log
└── backups/
```

This is a small example of filesystem automation.

---

# 29. Common Mistakes

## Mistake 1 — Forgetting the Import

Wrong:

```python
path = Path("server.log")
```

Correct:

```python
from pathlib import Path

path = Path("server.log")
```

Without the import, Python can produce:

```text
NameError: name 'Path' is not defined
```

---

## Mistake 2 — Confusing `/`

Normally:

```python
10 / 2
```

means division.

But:

```python
Path("logs") / "server.log"
```

means joining paths.

The behavior depends on the objects being used.

---

## Mistake 3 — Directory Already Exists

This:

```python
Path("logs").mkdir()
```

can fail if `logs` already exists.

For reusable automation, use:

```python
Path("logs").mkdir(exist_ok=True)
```

---

## Mistake 4 — Wrong Working Directory

If Python cannot find a relative path, check:

```bash
pwd
```

and:

```bash
ls
```

Remember:

```python
Path("server.log")
```

is a relative path.

---

# 30. Debugging Approach

When a filesystem automation script fails:

### Step 1

Check where you are:

```bash
pwd
```

### Step 2

Check what exists:

```bash
ls
```

### Step 3

Check the Python path:

```python
from pathlib import Path

print(Path.cwd())
```

### Step 4

Check whether the expected path exists:

```python
print(path.exists())
```

This gives us a systematic debugging process instead of guessing.

---

# 31. Industry Note

Professional Python developers commonly use `pathlib` for filesystem paths because it provides a clean and readable interface.

DevOps engineers use it for tasks such as:

- Backup automation
- Log processing
- File organization
- Configuration management
- Deployment scripts
- Temporary files
- Infrastructure automation

It is especially useful when a script needs to manipulate many files and directories.

---

# 32. How This Helps in DevOps

The relationship is:

```text
pathlib
   ↓
Files + Directories
   ↓
Filesystem Automation
   ↓
Linux Automation
   ↓
Logs / Backups / Configurations
   ↓
Monitoring / CI/CD
```

Later we will combine `pathlib` with other tools.

For example:

```text
pathlib
   +
subprocess
   ↓
Run Linux commands
   ↓
Automation
```

And:

```text
pathlib
   +
JSON / YAML
   ↓
Configuration automation
```

---

# 33. Future DevOps Connections

```text
Lesson 15 — File Handling
        ↓
Lesson 16 — pathlib
        ↓
Lesson 17 — os
        ↓
Lesson 18 — subprocess
        ↓
Lesson 19 — Environment Variables
        ↓
Lesson 20 — JSON
        ↓
Lesson 21 — YAML
        ↓
Lesson 22 — Logging
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

# 34. Cheat Sheet

## Import

```python
from pathlib import Path
```

## Create a path

```python
path = Path("server.log")
```

## Current working directory

```python
Path.cwd()
```

## Home directory

```python
Path.home()
```

## Check existence

```python
path.exists()
```

## Check if file

```python
path.is_file()
```

## Check if directory

```python
path.is_dir()
```

## Get filename

```python
path.name
```

## Get parent directory

```python
path.parent
```

## Get extension

```python
path.suffix
```

## Join paths

```python
Path("logs") / "nginx" / "error.log"
```

## Create directory

```python
path.mkdir()
```

## Don't fail if directory exists

```python
path.mkdir(exist_ok=True)
```

## Create nested directories

```python
path.mkdir(parents=True, exist_ok=True)
```

## Read text

```python
path.read_text()
```

## Write text

```python
path.write_text("Hello")
```

## List directory contents

```python
path.iterdir()
```

## Recursive search

```python
path.rglob("*.log")
```

---

# 35. Key Concepts to Remember

The most important concepts from this lesson are:

```text
Path
exists()
is_file()
is_dir()
mkdir()
read_text()
write_text()
name
parent
suffix
iterdir()
rglob()
```

Especially remember:

```python
from pathlib import Path
```

and:

```python
Path("logs") / "server.log"
```

---

# 36. Final Mental Model

Think of `pathlib` as Python's filesystem navigation and management tool.

```text
                  Path
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      Files    Directories   Paths
        │          │          │
        └──────────┼──────────┘
                   ↓
              Automation
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      Logs       Backups    Configs
```

---

# 37. Lesson Summary

In this lesson we learned:

- What `pathlib` is
- `Path`
- `Path.cwd()`
- `Path.home()`
- `exists()`
- `is_file()`
- `is_dir()`
- `mkdir()`
- `parents=True`
- `exist_ok=True`
- `read_text()`
- `write_text()`
- `name`
- `parent`
- `suffix`
- `iterdir()`
- `rglob()`
- Building paths with `/`

The key progression is:

```text
File Handling
      ↓
pathlib
      ↓
Filesystem Automation
      ↓
Linux Automation
      ↓
DevOps Automation
```

---

# 38. Lesson Files

The lesson should contain:

```text
Lesson-16-Pathlib/
├── 01_pathlib.py
├── 02_pathlib.md
└── 03_file_manager.py
```

The project creates:

```text
devops_files/
├── logs/
│   └── server.log
└── backups/
```

---

# 39. GitHub Workflow

After testing the code:

```bash
python3 01_pathlib.py
python3 03_file_manager.py
```

Go to the repository root:

```bash
cd ~/my-journey/devops-journey
```

Check Git:

```bash
git status
```

Stage the lesson:

```bash
git add python-for-devops/Python-lessons/Lesson-16-Pathlib/
```

Commit:

```bash
git commit -m "Complete Lesson 16: pathlib and file manager"
```

Push:

```bash
git push
```

---

# 40. Next Lesson

## Lesson 17 — `os` Module

Next we will learn how Python interacts more directly with the operating system.

We'll work with:

```text
Directories
Files
Environment information
Current working directory
Linux system information
Operating system operations
```

This will take us another step closer to real Linux automation.