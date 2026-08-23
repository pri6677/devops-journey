# Lesson 18 — Python `subprocess`

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
- Lesson 17 — `os` Module ✅
- Lesson 18 — `subprocess` ✅ **Current**
- Lesson 19 — Environment Variables ⬜
- Lesson 20 — JSON ⬜
- Lesson 21 — YAML ⬜
- Lesson 22 — Logging ⬜

---

# 2. Previous Lesson Recap

In Lesson 17, we learned the `os` module.

Important concepts:

```python
import os

os.getcwd()
os.listdir()
os.mkdir()
os.makedirs()
os.environ
os.getenv()
os.name
```

The main idea was:

```text
Python
   ↓
os
   ↓
Operating System
```

We learned that Python can interact with the Linux environment.

---

# 3. Practical Problem

A DevOps engineer frequently needs to execute Linux commands.

For example:

```bash
pwd
ls
df -h
uptime
hostname
```

We could manually execute these commands.

But imagine a Python script that automatically:

1. Runs a Linux command.
2. Captures its output.
3. Checks whether it succeeded.
4. Reads errors.
5. Makes an automation decision.

This is where `subprocess` becomes useful.

---

# 4. What Is `subprocess`?

`subprocess` is a Python standard-library module used to start and communicate with other processes.

One of its most important DevOps uses is:

> Running Linux commands from Python and getting their results back.

Import it:

```python
import subprocess
```

No external package installation is required.

---

# 5. Why Do We Need It?

Python itself cannot automatically perform every Linux operation.

Linux already provides powerful command-line tools.

Examples:

```text
df
du
ps
systemctl
ip
ss
docker
kubectl
terraform
git
```

Instead of rewriting everything in Python, we can sometimes use Python to control existing command-line tools.

The architecture becomes:

```text
Python
   ↓
subprocess
   ↓
Linux / CLI tool
   ↓
Result
   ↓
Python
```

---

# 6. Real-World Analogy

Imagine Python is a manager.

Linux commands are workers.

Python says:

> "Run `df -h` and give me the result."

The worker runs the command and reports:

```text
Output
Errors
Success / failure
```

Python can then decide what to do next.

```text
Python
  │
  │ Run command
  ↓
Linux process
  │
  ├── stdout
  ├── stderr
  └── return code
  ↓
Python
```

---

# 7. Running a Linux Command

Example:

```python
import subprocess

result = subprocess.run(["pwd"])

print(result)
```

`subprocess.run()`:

> Starts a process, waits for it to finish, and returns information about the process.

The command:

```python
["pwd"]
```

represents:

```bash
pwd
```

---

# 8. Passing Arguments

Linux:

```bash
ls -l
```

Python:

```python
subprocess.run(["ls", "-l"])
```

Linux:

```bash
df -h
```

Python:

```python
subprocess.run(["df", "-h"])
```

Each command component is a separate list item.

```text
["ls", "-l"]
   │      │
   │      └── argument
   └───────── command
```

This is the preferred style for normal command execution.

---

# 9. Capturing Output

By default, the command's output is displayed in the terminal.

To capture the output inside Python:

```python
import subprocess

result = subprocess.run(
    ["pwd"],
    capture_output=True,
    text=True
)

print(result.stdout)
```

Now Python has access to the command output.

---

# 10. `capture_output=True`

This tells Python:

> Capture the command's standard output and standard error.

Without it, you normally won't have the command's output stored in:

```python
result.stdout
```

---

# 11. `text=True`

Without `text=True`, captured output is returned as bytes.

You may see something like:

```text
b'/home/pri/...'
```

With:

```python
text=True
```

Python returns normal text.

Therefore:

```python
result.stdout
```

is much easier to work with.

---

# 12. `stdout`

`stdout` means:

```text
Standard Output
```

It represents normal output produced by the command.

Example:

```bash
pwd
```

might produce:

```text
/home/pri/my-journey/devops-journey
```

Python can access that using:

```python
result.stdout
```

---

# 13. `stderr`

`stderr` means:

```text
Standard Error
```

Commands can send error messages through stderr.

Example:

```python
import subprocess

result = subprocess.run(
    ["ls", "/does-not-exist"],
    capture_output=True,
    text=True
)

print(result.stderr)
```

You should see an error indicating that the directory does not exist.

---

# 14. `returncode`

Another important property is:

```python
result.returncode
```

It tells us whether the command succeeded.

Normally:

```text
0
```

means success.

A non-zero value generally indicates failure.

Example:

```python
import subprocess

result = subprocess.run(
    ["pwd"],
    capture_output=True,
    text=True
)

print(result.returncode)
```

Expected:

```text
0
```

---

# 15. DevOps Mental Model

Think about a Linux command as a process that gives Python three important things:

```text
Command
   │
   ├── stdout → normal output
   │
   ├── stderr → error output
   │
   └── returncode → success/failure
```

Python can use these results to make decisions.

---

# 16. Running `df -h`

A real DevOps example:

```python
import subprocess

result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True
)

print(result.stdout)
```

Linux equivalent:

```bash
df -h
```

The exact output depends on the machine.

---

# 17. Checking Command Success

We can use `returncode`:

```python
import subprocess

result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Command succeeded")
else:
    print("Command failed")
```

This is a common automation pattern.

---

# 18. `check=True`

Python can automatically raise an exception when a command fails.

```python
import subprocess

subprocess.run(
    ["df", "-h"],
    check=True
)
```

If the command succeeds, execution continues.

If it fails, Python raises:

```text
subprocess.CalledProcessError
```

---

# 19. `returncode` vs `check=True`

### Manual checking

```python
result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("Command failed")
```

### Automatic failure handling

```python
subprocess.run(
    ["df", "-h"],
    check=True
)
```

Both approaches are useful.

The correct choice depends on how the automation should behave when a command fails.

---

# 20. Handling Command Errors

We can combine `subprocess` with `try/except`.

```python
import subprocess

try:
    result = subprocess.run(
        ["ls", "/does-not-exist"],
        capture_output=True,
        text=True,
        check=True
    )

    print(result.stdout)

except subprocess.CalledProcessError as error:
    print("Command failed")
    print(error.stderr)
```

The flow is:

```text
Run command
     ↓
Success?
 ┌───┴────┐
Yes       No
 ↓         ↓
Continue  Handle error
```

---

# 21. `subprocess` vs `os.system()`

Previously we saw:

```python
os.system("pwd")
```

`os.system()` can execute commands, but it gives us less control.

`subprocess` allows us to:

- Capture output
- Capture errors
- Check return codes
- Raise exceptions
- Pass arguments separately
- Control the process

For professional command execution, prefer `subprocess`.

---

# 22. Mini Project — Linux System Check

File:

```text
03_system_check.py
```

Code:

```python
import subprocess

print("===== SYSTEM CHECK =====")

commands = [
    ["hostname"],
    ["uptime"],
    ["df", "-h"]
]

for command in commands:
    print(f"\n$ {' '.join(command)}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Command failed:")
        print(result.stderr)
```

Run:

```bash
python3 03_system_check.py
```

---

# 23. Understanding the Mini Project

The variable:

```python
commands = [
    ["hostname"],
    ["uptime"],
    ["df", "-h"]
]
```

contains Linux commands.

The `for` loop:

```python
for command in commands:
```

processes each command.

Then:

```python
subprocess.run(command, ...)
```

runs it.

Then:

```python
if result.returncode == 0:
```

checks whether it succeeded.

Finally:

```python
result.stdout
```

prints the command output.

This combines several concepts learned previously:

```text
Lists
Loops
Conditions
Functions
Modules
Error handling
```

with:

```text
Linux commands
```

---

# 24. Common Mistakes

## Mistake 1 — Wrong command list

Preferred:

```python
subprocess.run(["ls", "-l"])
```

Not:

```python
subprocess.run(["ls -l"])
```

The first treats:

```text
ls
-l
```

as separate command components.

---

## Mistake 2 — Forgetting `capture_output=True`

If you want:

```python
result.stdout
```

you normally need:

```python
capture_output=True
```

---

## Mistake 3 — Forgetting `text=True`

Without it, captured output is bytes.

With:

```python
text=True
```

you get a normal Python string.

---

## Mistake 4 — Assuming commands always succeed

Commands can fail.

Always consider:

```python
result.returncode
```

or:

```python
check=True
```

depending on your requirements.

---

# 25. Debugging

When a subprocess script fails:

### Check the Linux command manually first

For example:

```bash
df -h
```

If the command itself doesn't work, the Python script isn't the first problem.

### Then check Python

```python
result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)
print(result.returncode)
```

This gives you:

```text
stdout
stderr
returncode
```

which is often enough to understand what happened.

---

# 26. Industry Note

Professional DevOps engineers use subprocess-based automation when Python needs to interact with existing command-line tools.

Examples:

```text
Linux administration
Docker CLI automation
Kubernetes CLI automation
Git automation
Terraform automation
System health checks
Deployment scripts
CI/CD helper scripts
```

For example:

```text
Python
   ↓
subprocess
   ↓
docker
```

or:

```text
Python
   ↓
subprocess
   ↓
kubectl
```

or:

```text
Python
   ↓
subprocess
   ↓
terraform
```

This makes Python useful as an automation layer around existing infrastructure tools.

---

# 27. How This Helps in DevOps

Our automation stack is now:

```text
Python
  │
  ├── pathlib
  │      ↓
  │   Files / Paths
  │
  ├── os
  │      ↓
  │   Operating System
  │
  └── subprocess
         ↓
      Linux Commands
```

This foundation will be useful for:

- Linux automation
- Server administration
- Docker automation
- Kubernetes automation
- CI/CD scripts
- Infrastructure tooling

---

# 28. Future Connections

```text
pathlib                    ✅
os                         ✅
subprocess                 ✅
Environment Variables      NEXT
JSON
YAML
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

# 29. Cheat Sheet

## Import

```python
import subprocess
```

## Run a command

```python
subprocess.run(["pwd"])
```

## Capture output

```python
result = subprocess.run(
    ["pwd"],
    capture_output=True,
    text=True
)
```

## Normal output

```python
result.stdout
```

## Error output

```python
result.stderr
```

## Success/failure

```python
result.returncode
```

## Automatically raise on failure

```python
subprocess.run(
    ["pwd"],
    check=True
)
```

## Handle command failure

```python
try:
    subprocess.run(
        ["command"],
        check=True
    )
except subprocess.CalledProcessError:
    print("Command failed")
```

---

# 30. Key Concepts

Remember:

```text
subprocess.run()
capture_output=True
text=True
stdout
stderr
returncode
check=True
CalledProcessError
```

The most useful basic pattern is:

```python
result = subprocess.run(
    ["command", "argument"],
    capture_output=True,
    text=True
)

print(result.stdout)
```

---

# 31. DevOps Roadmap Connection

The path we're building is:

```text
Python
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

# 32. GitHub Integration

Repository:

```text
devops-journey/
└── python-for-devops/
    └── Python-lessons/
        └── Lesson-18-Subprocess/
            ├── 01_subprocess.py
            ├── 02_subprocess.md
            └── 03_system_check.py
```

Portfolio components:

```text
02_subprocess.md
    ↓
Detailed lesson notes

03_system_check.py
    ↓
Practical DevOps project
```

---

# 33. Git Workflow

Test the programs:

```bash
python3 01_subprocess.py
python3 03_system_check.py
```

Go to the repository root:

```bash
cd ~/my-journey/devops-journey
```

Check:

```bash
git status
```

Stage:

```bash
git add python-for-devops/Python-lessons/Lesson-18-Subprocess/
```

Commit:

```bash
git commit -m "Complete Lesson 18: subprocess Linux automation"
```

Push:

```bash
git push
```

---

# 34. Next Lesson

## Lesson 19 — Environment Variables

Environment variables are particularly important for professional DevOps work.

We will use them for concepts such as:

```text
AWS configuration
API configuration
Docker configuration
CI/CD variables
Secrets
Environment-specific configuration
```

The core idea:

```text
Environment
     ↓
Python
     ↓
Automation / Application
```

After that:

```text
Environment Variables
        ↓
JSON
        ↓
YAML
        ↓
Logging
```