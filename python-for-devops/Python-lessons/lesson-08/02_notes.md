# Chapter 8 — Python Functions

## 1. What Is a Function?

A function is a reusable block of code that performs a specific task.

Example:

```python
def greet():
    print("Hello!")
```

Call it:

```python
greet()
```

---

## 2. Defining a Function

```python
def greet():
    print("Hello!")
```

### `def`

Python keyword used to define a function.

### Function name

```python
greet
```

### `()`

Contains parameters if the function needs inputs.

### `:`

Starts the function block.

### Indentation

The indented code belongs to the function.

---

## 3. Calling a Function

Defining:

```python
def greet():
    print("Hello!")
```

Calling:

```python
greet()
```

The function runs when it is called.

---

## 4. Parameters

A function can receive input.

```python
def greet(name):
    print(f"Hello, {name}!")
```

Call:

```python
greet("Pri")
```

`name` is a parameter.

`"Pri"` is an argument.

---

## 5. Return

Functions can return values.

```python
def add(a, b):
    return a + b
```

Then:

```python
result = add(10, 20)
print(result)
```

Output:

```text
30
```

---

## 6. `print()` vs `return`

`print()` displays something:

```python
def add(a, b):
    print(a + b)
```

`return` sends a value back:

```python
def add(a, b):
    return a + b
```

For reusable automation logic, `return` is usually more useful.

---

## 7. DevOps Example

```python
def check_cpu(cpu_usage):
    if cpu_usage > 80:
        return "WARNING: High CPU usage"
    else:
        return "CPU usage is normal"
```

Usage:

```python
print(check_cpu(87))
print(check_cpu(45))
```

---

## 8. Multiple Parameters

```python
def check_resource(resource, usage, threshold):
    if usage > threshold:
        print(f"WARNING: {resource} usage is high")
    else:
        print(f"{resource} usage is normal")
```

Usage:

```python
check_resource("CPU", 87, 80)
check_resource("Memory", 65, 80)
check_resource("Disk", 91, 90)
```

---

## 9. Server Health Functions

```python
def check_cpu(cpu_usage):
    if cpu_usage >= 80:
        return "WARNING: High CPU usage"
    return "CPU usage is normal"


def check_memory(memory_usage):
    if memory_usage >= 80:
        return "WARNING: High memory usage"
    return "Memory usage is normal"


def check_disk(disk_usage):
    if disk_usage >= 90:
        return "CRITICAL: Disk usage is very high"
    elif disk_usage >= 80:
        return "WARNING: Disk usage is high"
    return "Disk usage is normal"
```

---

## 10. Common Mistakes

### Not calling the function

```python
def greet():
    print("Hello")
```

Nothing happens until:

```python
greet()
```

### Wrong indentation

```python
def greet():
    print("Hello")
```

### Using `print()` instead of `return`

```python
def add(a, b):
    print(a + b)
```

This displays the result but doesn't return it.

Use:

```python
def add(a, b):
    return a + b
```

---

## 11. Industry Note

Professional DevOps scripts are usually divided into small reusable functions.

Example structure:

```text
main()
 ├── get_servers()
 ├── check_health()
 ├── process_results()
 └── send_alert()
```

Each function should have a clear responsibility.

---

## 12. DevOps Applications

Functions will be used for:

- Linux automation
- AWS automation
- Docker automation
- Kubernetes automation
- Monitoring
- API automation
- CI/CD
- SRE tools

Typical pattern:

```text
Get data
   ↓
Function processes data
   ↓
Return result
   ↓
Make decision
   ↓
Take action
```

---

## 13. Cheat Sheet

```text
def          define function
()           parameters / call
argument     value passed to function
parameter    input variable
return       send value back
```

Basic:

```python
def function_name(parameter):
    return value


result = function_name(argument)
```