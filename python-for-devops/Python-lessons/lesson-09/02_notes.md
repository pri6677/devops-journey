# Chapter 9 — Python Error Handling

## 1. Why Error Handling?

Real automation can fail because of:

- Invalid input
- Missing files
- Network problems
- API failures
- Invalid configuration
- Permission problems

Error handling lets us decide what the program should do when something goes wrong.

---

## 2. Exception

An exception is a problem raised while Python is running.

Example:

```python
number = int("hello")
```

This raises:

```text
ValueError
```

---

## 3. `try` and `except`

Basic structure:

```python
try:
    risky_code()
except SomeError:
    handle_error()
```

Example:

```python
try:
    number = int("hello")
except ValueError:
    print("Invalid number")
```

---

## 4. User Input

```python
try:
    port = int(input("Enter port: "))
    print(f"Port: {port}")
except ValueError:
    print("Port must be a number")
```

---

## 5. `else`

`else` runs when no exception occurs.

```python
try:
    number = int("100")
except ValueError:
    print("Invalid number")
else:
    print("Conversion successful")
```

---

## 6. `finally`

`finally` runs regardless of whether an exception occurred.

```python
try:
    number = int("100")
except ValueError:
    print("Invalid number")
finally:
    print("Finished")
```

This becomes useful for cleanup operations.

---

## 7. `raise`

`raise` deliberately creates an exception.

```python
cpu_usage = 150

if cpu_usage > 100:
    raise ValueError("CPU usage cannot exceed 100%")
```

---

## 8. Common Exceptions

| Exception | Meaning |
|---|---|
| `ValueError` | Invalid value |
| `TypeError` | Wrong type |
| `FileNotFoundError` | File doesn't exist |
| `KeyError` | Dictionary key missing |
| `IndexError` | List index missing |
| `ZeroDivisionError` | Division by zero |

---

## 9. Specific Exceptions

Prefer:

```python
except ValueError:
```

instead of always using:

```python
except:
```

Specific exceptions make programs easier to debug and maintain.

---

## 10. Safe Server Configuration

```python
def validate_port(port):
    try:
        port = int(port)

        if port < 1 or port > 65535:
            return False

        return True

    except ValueError:
        return False


port = input("Enter server port: ")

if validate_port(port):
    print(f"Port {port} is valid")
else:
    print("ERROR: Invalid port")
```

---

## 11. Common Mistake

This does not catch `ZeroDivisionError`:

```python
try:
    print(10 / 0)
except ValueError:
    print("Error")
```

Correct:

```python
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")
```

---

## 12. Avoid Hiding Errors

Avoid:

```python
try:
    # code
except:
    pass
```

This can silently hide serious problems.

---

## 13. DevOps Connection

Error handling is essential for:

- Linux automation
- AWS automation
- API automation
- Docker automation
- Kubernetes automation
- CI/CD
- SRE scripts

Typical pattern:

```text
Perform operation
       ↓
Did it fail?
   ↓        ↓
  YES       NO
   ↓         ↓
Handle      Continue
error
```

Reliable automation requires intentional error handling.