# Lesson 19 — Environment Variables

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
- Lesson 18 — `subprocess` ✅
- Lesson 19 — Environment Variables ✅ **Current**
- Lesson 20 — JSON ⬜
- Lesson 21 — YAML ⬜
- Lesson 22 — Logging ⬜

---

# 2. Previous Lesson Recap

In Lesson 18, we learned `subprocess`.

Important concepts:

```python
import subprocess

result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)
print(result.returncode)
```

We learned that Python can execute Linux commands and work with their:

- Standard output
- Standard error
- Return code

The main idea was:

```text
Python
   ↓
subprocess
   ↓
Linux command
   ↓
Result
   ↓
Python
```

---

# 3. Practical Problem

A DevOps engineer may write a script that needs:

- AWS configuration
- API keys
- Server configuration
- Database configuration
- Environment name
- Docker configuration
- CI/CD variables

We should not normally hard-code configuration directly into the Python program.

Bad:

```python
api_key = "secret123"
```

Instead, configuration can be provided externally:

```text
Linux environment
       ↓
Environment variable
       ↓
Python
       ↓
Automation
```

---

# 4. What Is an Environment Variable?

An environment variable is a named value provided by the operating system to a running process.

Linux commonly has variables such as:

```text
HOME=/home/pri
USER=pri
SHELL=/bin/bash
```

You can see one in Linux:

```bash
echo $HOME
```

or:

```bash
echo $USER
```

---

# 5. Why Do We Need Environment Variables?

Consider:

```python
environment = "production"
```

If the script moves between environments, the source code has to be changed.

Instead:

```text
Development
    ↓
ENVIRONMENT=development

Production
    ↓
ENVIRONMENT=production
```

The same Python program can use different configuration.

This is useful in:

- DevOps
- CI/CD
- Docker
- Kubernetes
- AWS
- APIs
- Automation

---

# 6. Real-World Analogy

Think of a Python script as a machine.

The machine needs settings.

Instead of rebuilding the machine every time, you provide settings from outside.

```text
             Python script
                  ↑
                  │
          Environment variables
                  ↑
                  │
              Linux / CI/CD
```

The code stays the same while the configuration changes.

---

# 7. Creating an Environment Variable

In Linux:

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

General syntax:

```bash
export NAME="VALUE"
```

Example:

```bash
export SERVER_NAME="web-server-01"
```

---

# 8. Reading an Environment Variable From Python

Python:

```python
import os

environment = os.getenv("DEVOPS_ENV")

print("Environment:", environment)
```

Run:

```bash
python3 01_environment_variables.py
```

Output:

```text
Environment: development
```

The connection is:

```text
Linux
 ↓
DEVOPS_ENV=development
 ↓
os.getenv()
 ↓
Python variable
```

---

# 9. `os.getenv()`

We learned `os` in Lesson 17.

```python
os.getenv("DEVOPS_ENV")
```

means:

> Get the value of the `DEVOPS_ENV` environment variable.

We can store the result:

```python
environment = os.getenv("DEVOPS_ENV")
```

Now `environment` is a normal Python variable.

---

# 10. What Happens If the Variable Does Not Exist?

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

`None` means that there is currently no value.

This is different from an empty string:

```text
""
```

---

# 11. Providing a Default Value

We can provide a fallback value:

```python
import os

environment = os.getenv("DEVOPS_ENV", "development")

print(environment)
```

The second argument is the default value.

Meaning:

> If `DEVOPS_ENV` does not exist, use `"development"`.

This can be useful for local development.

---

# 12. `os.environ`

Another way to access an environment variable is:

```python
import os

environment = os.environ["DEVOPS_ENV"]

print(environment)
```

This works when the variable exists.

If it does not exist, Python raises:

```text
KeyError
```

Therefore:

```python
os.getenv("DEVOPS_ENV")
```

is often convenient when a variable may be missing.

---

# 13. `os.environ[]` vs `os.getenv()`

### `os.environ[]`

```python
os.environ["DEVOPS_ENV"]
```

Missing variable:

```text
KeyError
```

### `os.getenv()`

```python
os.getenv("DEVOPS_ENV")
```

Missing variable:

```text
None
```

A default can also be provided:

```python
os.getenv("DEVOPS_ENV", "development")
```

---

# 14. Environment Variables Are Strings

This is very important.

Linux:

```bash
export SERVER_PORT="8080"
```

Python:

```python
import os

port = os.getenv("SERVER_PORT")

print(port)
print(type(port))
```

Output:

```text
8080
<class 'str'>
```

Even though `8080` looks like a number, environment variables are received as strings.

If an integer is required:

```python
port = int(os.getenv("SERVER_PORT"))
```

Now the type is:

```text
<class 'int'>
```

---

# 15. Environment Variable + Condition

We can combine environment variables with conditions:

```python
import os

environment = os.getenv("DEVOPS_ENV", "development")

if environment == "production":
    print("Production environment")
else:
    print("Non-production environment")
```

Now the behavior of the program depends on external configuration.

---

# 16. Mini Project — Environment Configuration

File:

```text
03_environment_config.py
```

Code:

```python
import os

environment = os.getenv("DEVOPS_ENV", "development")
server_name = os.getenv("SERVER_NAME", "localhost")
server_port = int(os.getenv("SERVER_PORT", "8080"))

print("===== ENVIRONMENT CONFIGURATION =====")
print("Environment:", environment)
print("Server:", server_name)
print("Port:", server_port)

if environment == "production":
    print("WARNING: Production environment")
else:
    print("Safe development/test environment")
```

---

# 17. Configure the Project From Linux

Set the variables:

```bash
export DEVOPS_ENV="production"
export SERVER_NAME="web-server-01"
export SERVER_PORT="80"
```

Check them:

```bash
echo $DEVOPS_ENV
echo $SERVER_NAME
echo $SERVER_PORT
```

Run:

```bash
python3 03_environment_config.py
```

Expected output:

```text
===== ENVIRONMENT CONFIGURATION =====
Environment: production
Server: web-server-01
Port: 80
WARNING: Production environment
```

---

# 18. Why This Is a DevOps Pattern

Notice that we didn't change:

```text
03_environment_config.py
```

We only changed the environment:

```text
Linux environment
```

Therefore the same Python program can behave differently.

### Development

```bash
export DEVOPS_ENV="development"
export SERVER_NAME="localhost"
export SERVER_PORT="8080"
```

### Production

```bash
export DEVOPS_ENV="production"
export SERVER_NAME="web-server-01"
export SERVER_PORT="80"
```

Same Python code.

Different configuration.

---

# 19. Environment Variables and Secrets

Environment variables are commonly used to provide configuration and secrets to programs.

Examples:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
API_KEY
DATABASE_URL
```

Instead of:

```python
api_key = "my-secret-key"
```

applications can receive configuration externally.

However:

> Environment variables are not magically secure.

They can potentially be exposed through processes, logs, debugging, CI systems, or misconfiguration.

Later, when we study AWS and CI/CD, we will learn proper secret-management practices.

---

# 20. Docker Connection

Docker commonly passes configuration through environment variables.

Conceptually:

```text
Docker container
       ↓
Environment variables
       ↓
Python application
```

For example:

```text
ENVIRONMENT=production
PORT=8080
```

Python can read them:

```python
os.getenv("ENVIRONMENT")
os.getenv("PORT")
```

---

# 21. Kubernetes Connection

Kubernetes commonly provides application configuration through environment variables.

Conceptually:

```text
Kubernetes
    ↓
Pod
    ↓
Environment variables
    ↓
Python application
```

The concept learned here will appear again when we study Kubernetes.

---

# 22. CI/CD Connection

CI/CD systems can provide variables to scripts.

Conceptually:

```text
GitHub Actions / Jenkins
          ↓
Environment variables
          ↓
Python script
          ↓
Deployment / automation
```

For example:

```text
ENVIRONMENT=production
```

The Python automation can read it without changing the source code.

---

# 23. AWS Connection

Later, when we learn `boto3`, you will see AWS configuration such as:

```text
AWS_REGION
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Python AWS automation can work with environment-based configuration.

The path is:

```text
Python
   ↓
Environment Variables
   ↓
AWS
   ↓
boto3
```

---

# 24. Common Mistakes

## Mistake 1 — Forgetting `export`

This:

```bash
DEVOPS_ENV="production"
```

creates a shell variable but does not automatically make it available to child processes.

Use:

```bash
export DEVOPS_ENV="production"
```

Then Python can access it.

---

## Mistake 2 — Expecting an Integer

Environment variables are strings.

```python
port = os.getenv("SERVER_PORT")
```

returns a string.

If you need an integer:

```python
port = int(os.getenv("SERVER_PORT"))
```

---

## Mistake 3 — Using `os.environ[]` Without Checking

This:

```python
os.environ["MISSING_VARIABLE"]
```

can produce:

```text
KeyError
```

Use:

```python
os.getenv("MISSING_VARIABLE")
```

when the variable is optional.

---

## Mistake 4 — Hard-Coding Secrets

Avoid:

```python
API_KEY = "secret123"
```

Especially in code that will be committed to GitHub.

Use external configuration instead.

---

# 25. Debugging

When an environment-variable script does not behave as expected:

### Check Linux

```bash
echo $DEVOPS_ENV
echo $SERVER_NAME
echo $SERVER_PORT
```

### Check Python

```python
import os

print(os.getenv("DEVOPS_ENV"))
print(os.getenv("SERVER_NAME"))
print(os.getenv("SERVER_PORT"))
```

### Check the type

```python
print(type(os.getenv("SERVER_PORT")))
```

Remember:

```text
Environment variables
        ↓
      strings
```

---

# 26. Industry Note

Professional DevOps engineers separate:

```text
Code
```

from:

```text
Configuration
```

For example:

```text
Code
 ↓
GitHub

Configuration
 ↓
Environment / CI/CD / Secret Manager
```

This allows the same automation code to run in:

```text
Development
Staging
Production
```

without changing the source code.

---

# 27. How This Helps in DevOps

This concept appears everywhere:

```text
Linux
  ↓
Environment variables
  ↓
Python automation
```

Later:

```text
Python
 ├── AWS
 ├── Docker
 ├── Kubernetes
 ├── CI/CD
 ├── APIs
 └── Monitoring
```

You will repeatedly see configuration being passed into programs externally.

---

# 28. Cheat Sheet

### Create variable in Linux

```bash
export NAME="value"
```

### Read in Linux

```bash
echo $NAME
```

### Read in Python

```python
import os

value = os.getenv("NAME")
```

### Default value

```python
value = os.getenv("NAME", "default")
```

### Direct access

```python
value = os.environ["NAME"]
```

### Convert to integer

```python
port = int(os.getenv("PORT", "8080"))
```

### Check variable

```python
if os.getenv("ENVIRONMENT") == "production":
    print("Production")
```

---

# 29. Key Mental Model

Remember:

```text
Environment Variable
        ↓
      String
        ↓
    os.getenv()
        ↓
 Python variable
        ↓
Automation logic
```

Bigger DevOps architecture:

```text
Configuration
     ↓
Environment
     ↓
Python
     ↓
Automation
```

---

# 30. Future Connections

```text
pathlib                    ✅
os                         ✅
subprocess                 ✅
Environment Variables      ✅
JSON                       NEXT
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

# 31. Lesson Files

```text
Lesson-19-Environment-Variables/
├── 01_environment_variables.py
├── 02_environment_variables.md
└── 03_environment_config.py
```

---

# 32. GitHub Integration

Repository:

```text
devops-journey/
└── python-for-devops/
    └── Python-lessons/
        └── Lesson-19-Environment-Variables/
```

Files:

```text
01_environment_variables.py
02_environment_variables.md
03_environment_config.py
```

Portfolio components:

```text
02_environment_variables.md
    ↓
Detailed lesson notes

03_environment_config.py
    ↓
Practical project
```

---

# 33. Git Workflow

Test the programs:

```bash
python3 01_environment_variables.py
python3 03_environment_config.py
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
git add python-for-devops/Python-lessons/Lesson-19-Environment-Variables/
```

Commit:

```bash
git commit -m "Complete Lesson 19: environment variables"
```

Push:

```bash
git push
```

---

# 34. Next Lesson

## Lesson 20 — JSON

We will learn how Python works with structured data such as:

```json
{
    "server": "web-01",
    "port": 8080,
    "environment": "production"
}
```

This is useful for:

- APIs
- Configuration
- Cloud automation
- AWS
- Monitoring
- CI/CD
- Infrastructure tooling

The important distinction is:

```text
Environment Variables
        ↓
External configuration

JSON
        ↓
Structured data
```

We will later use both together in real DevOps projects.
