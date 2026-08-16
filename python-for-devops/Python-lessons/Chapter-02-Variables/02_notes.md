# Chapter 2 — Python Variables

## 1. What is a Variable?

A variable is a name that refers to a value.

Example:

```python
server_name = "web-01"
```

Here:

- `server_name` is the variable name.
- `=` is the assignment operator.
- `"web-01"` is the value.

Conceptually:

server_name → "web-01"

We can use the variable later:

```python
print(server_name)
```

Output:

```text
web-01
```

---

## 2. Why Do We Need Variables?

Variables allow programs to store and reuse information.

Without variables:

```python
print("web-01")
print("web-01 is running")
print("Restarting web-01")
```

If the server changes, multiple lines may need to be changed.

With a variable:

```python
server_name = "web-01"

print(server_name)
print(server_name, "is running")
print("Restarting", server_name)
```

Now we can change the server name in one place:

```python
server_name = "web-02"
```

The rest of the program automatically uses the new value.

---

## 3. Real-World Analogy

A variable is similar to a labelled storage box.

For example:

```text
Label: SERVER_NAME
Value: web-01
```

In Python:

```python
server_name = "web-01"
```

The variable name gives us a way to refer to the stored value.

---

## 4. Assignment Operator

The `=` symbol is the assignment operator.

Example:

```python
server_name = "web-01"
```

It means that the value `"web-01"` is assigned to the name `server_name`.

It does NOT mean mathematical equality.

Python uses `==` for equality comparison.

Example:

```python
server_name == "web-01"
```

The `==` operator will be studied properly later when conditions are introduced.

---

## 5. Using Variables

Example:

```python
server_name = "web-01"

print(server_name)
```

Output:

```text
web-01
```

`print()` displays the value referred to by the variable.

---

## 6. Reassigning Variables

A variable can be assigned a new value.

```python
server_name = "web-01"

print(server_name)

server_name = "web-02"

print(server_name)
```

Output:

```text
web-01
web-02
```

The second assignment changes the value associated with `server_name`.

---

## 7. Multiple Variables

A program can contain many variables.

```python
server_name = "web-01"
ip_address = "192.168.1.10"
environment = "production"
status = "online"
```

They can be used later:

```python
print(server_name)
print(ip_address)
print(environment)
print(status)
```

---

## 8. Printing Text and Variables

Python's `print()` function can receive multiple values.

```python
server_name = "web-01"
status = "online"

print("Server:", server_name)
print("Status:", status)
```

Output:

```text
Server: web-01
Status: online
```

---

## 9. Variable vs String

These two statements are different:

```python
print(server_name)
```

and:

```python
print("server_name")
```

The first uses the variable.

The second prints the literal text `server_name`.

Example:

```python
server_name = "web-01"

print(server_name)
print("server_name")
```

Output:

```text
web-01
server_name
```

Quotation marks tell Python that something is text.

---

## 10. Python is Case-Sensitive

Python treats uppercase and lowercase letters as different.

These are different names:

```python
server_name
Server_name
SERVER_NAME
```

Example:

```python
server_name = "web-01"

print(Server_name)
```

This produces a `NameError` because `Server_name` was never defined.

The correct version is:

```python
print(server_name)
```

---

## 11. Variable Naming Rules

Python variable names can contain:

- Letters
- Numbers
- Underscores

A variable name cannot start with a number.

Valid:

```python
server_name = "web-01"
server1 = "web-01"
ip_address = "192.168.1.10"
cpu_usage = 75
```

Invalid:

```python
1server = "web-01"
```

Variable names cannot contain spaces.

Invalid:

```python
server name = "web-01"
```

Use an underscore instead:

```python
server_name = "web-01"
```

---

## 12. Snake Case

Python commonly uses `snake_case` for variable names.

Examples:

```python
server_name
ip_address
cpu_usage
disk_usage
log_file
backup_directory
```

This makes code easier to read.

---

## 13. Variables and Different Values

Variables can refer to different types of values.

```python
server_name = "web-01"
port = 80
cpu_usage = 75.5
server_running = True
```

Basic meanings:

```text
"web-01" → text
80       → whole number
75.5     → decimal number
True     → Boolean value
```

Python data types will be studied in the next chapter.

---

# 14. Common Errors

## NameError

Example:

```python
print(server_name)
```

when `server_name` has not been defined.

Python does not know what `server_name` refers to.

Another common cause is incorrect capitalization:

```python
server_name = "web-01"

print(Server_name)
```

`server_name` and `Server_name` are different names.

---

## SyntaxError

Example:

```python
server name = "web-01"
```

The space makes the variable declaration invalid.

Correct:

```python
server_name = "web-01"
```

---

# 15. Best Practices

Use descriptive names:

```python
server_name = "web-01"
ip_address = "192.168.1.10"
cpu_usage = 75
disk_usage = 80
```

Avoid unclear names:

```python
x = "web-01"
a = 75
thing = "production"
```

Descriptive names become especially important in large automation scripts.

---

# 16. DevOps Connection

Variables are fundamental to automation.

A DevOps script may use variables for:

- Server names
- IP addresses
- Ports
- CPU thresholds
- Disk thresholds
- File paths
- Log files
- AWS regions
- AWS resource names
- Docker container names
- Kubernetes namespaces
- Deployment environments

Example:

```python
cpu_usage = 92
cpu_threshold = 80
```

Later we can use these values to implement monitoring logic:

```text
CPU usage
    ↓
Compare with threshold
    ↓
If usage is too high
    ↓
Generate an alert
```

---

# 17. Linux Automation Connection

A future Linux automation script might contain:

```python
service_name = "nginx"
```

and use that value when checking or managing the service.

Another script might store:

```python
log_file = "/var/log/nginx/access.log"
```

and use it to analyze logs.

Variables allow the same automation logic to work with different values.

---

# 18. AWS Connection

Later, with `boto3`, we may use variables such as:

```python
region = "ap-south-1"
bucket_name = "my-backup-bucket"
```

These values can then be used by AWS automation code.

---

# 19. Docker Connection

A Docker automation script may use:

```python
container_name = "web-app"
```

to identify a container.

---

# 20. Kubernetes Connection

A Kubernetes automation script may use:

```python
namespace = "production"
```

to identify the target namespace.

---

# 21. CI/CD Connection

Automation scripts can use variables to represent:

```python
environment = "production"
version = "1.2.0"
```

These values can later come from environment variables or CI/CD pipeline configuration.

---

# 22. Industry Note

Professional DevOps and SRE engineers use variables constantly.

However, production scripts usually avoid hard-coding important configuration values directly into the source code.

Later we will learn how to obtain values from:

- Environment variables
- Configuration files
- Command-line arguments
- APIs
- Cloud services
- Secrets/configuration systems

These concepts will be introduced when they become useful.

---

# 23. Practice Code

```python
server_name = "web-01"
ip_address = "192.168.1.10"
environment = "production"
status = "online"

print("Server:", server_name)
print("IP:", ip_address)
print("Environment:", environment)
print("Status:", status)
```

---

# 24. Important Takeaways

Remember:

```text
variable = value
```

Example:

```python
server_name = "web-01"
```

Use a variable:

```python
print(server_name)
```

Reassign it:

```python
server_name = "web-02"
```

Python is case-sensitive:

```text
server_name != Server_name
```

Use snake_case:

```python
server_name
ip_address
cpu_usage
```

---

# 25. Next Chapter

The next chapter is:

**Chapter 3 — Python Data Types**

We will learn:

```text
str
int
float
bool
None
```

and immediately use them in DevOps-related examples.