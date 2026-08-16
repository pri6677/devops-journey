# Lesson 11 — Tuples and Sets

> Python for Cloud & DevOps Engineering

---

## 1. Where I Am in the Python Roadmap

We are currently learning Python fundamentals.

```text
Python Fundamentals
│
├── Lesson 01 — Running Python              ✅
├── Lesson 02 — Variables                   ✅
├── Lesson 03 — Data Types                  ✅
├── Lesson 04 — Input / Output              ✅
├── Lesson 05 — Operators                   ✅
├── Lesson 06 — Conditions                  ✅
├── Lesson 07 — Loops                       ✅
├── Lesson 08 — Functions                   ✅
├── Lesson 09 — Error Handling              ✅
├── Lesson 10 — Lists                       ✅
├── Lesson 11 — Tuples and Sets             ✅
│
├── Dictionaries
├── Strings
├── Modules
├── File Handling
└── ...
```

The goal of this lesson is to understand two additional Python collection types:

- Tuples
- Sets

These are useful when working with infrastructure data, configuration, server inventories, IP addresses, ports, and resource comparisons.

---

# 2. Previous Lesson Recap

In the previous lesson, we learned about **lists**.

A list stores multiple values:

```python
servers = ["web-01", "web-02", "web-03"]
```

Lists are:

- Ordered
- Mutable
- Able to contain duplicates

Example:

```python
servers.append("web-04")
```

The list changes.

This lesson introduces two different collection types that solve different problems.

---

# 3. Practical Problem

Imagine a DevOps script containing allowed network ports:

```python
allowed_ports = (22, 80, 443)
```

These values represent a fixed configuration.

We don't want another part of the program accidentally changing them.

A tuple is useful here.

Now imagine a monitoring system gives us duplicate IP addresses:

```python
ips = [
    "10.0.0.1",
    "10.0.0.2",
    "10.0.0.1",
    "10.0.0.3",
    "10.0.0.2"
]
```

We only want unique IP addresses.

A set is useful here.

Therefore:

```text
Fixed collection
      ↓
    Tuple

Unique collection
      ↓
     Set
```

---

# 4. What Is a Tuple?

A tuple is a Python collection that stores multiple values in a fixed, ordered structure.

Example:

```python
ports = (22, 80, 443)
```

A tuple uses parentheses:

```text
(22, 80, 443)
```

Compare it with a list:

```python
ports = [22, 80, 443]
```

The important difference is:

```text
List
→ mutable
→ can be changed

Tuple
→ immutable
→ cannot normally be changed
```

---

# 5. Why Do We Need Tuples?

Some data represents information that should not change during the execution of a program.

For example:

```python
allowed_ports = (22, 80, 443)
```

These might represent standard ports allowed by a security policy.

If the program should treat them as fixed values, a tuple communicates that intention.

Another example:

```python
server_location = ("India", "Mumbai")
```

The values form a fixed pair of information.

---

# 6. Tuple Indexing

Tuples use indexes just like lists.

Example:

```python
ports = (22, 80, 443)

print(ports[0])
print(ports[1])
print(ports[2])
```

Output:

```text
22
80
443
```

Python indexes start from `0`.

```text
Index:     0    1    2
Value:    22   80   443
```

---

# 7. Tuple Cannot Be Modified

Consider:

```python
ports = (22, 80, 443)
```

Trying to change an item:

```python
ports[0] = 8080
```

causes an error.

The reason is that tuples are immutable.

```text
Immutable
    ↓
Cannot be modified after creation
```

This is different from a list:

```python
ports = [22, 80, 443]

ports[0] = 8080
```

A list allows this modification.

---

# 8. Looping Through a Tuple

A tuple can be used in a `for` loop.

```python
ports = (22, 80, 443)

for port in ports:
    print(port)
```

Output:

```text
22
80
443
```

The tuple can therefore be processed just like other collections.

---

# 9. One-Item Tuple

There is an important syntax detail.

This:

```python
port = (22)
```

is not a tuple.

It is simply the number:

```text
22
```

A one-item tuple requires a comma:

```python
port = (22,)
```

The comma is what tells Python that this is a tuple.

Example:

```python
print(type((22)))
print(type((22,)))
```

The first is an integer.

The second is a tuple.

---

# 10. What Is a Set?

A set is a collection that stores **unique values**.

Example:

```python
servers = {
    "web-01",
    "web-02",
    "web-03"
}
```

A set automatically removes duplicate values.

Example:

```python
servers = {
    "web-01",
    "web-02",
    "web-01"
}

print(servers)
```

The duplicate `"web-01"` is stored only once.

---

# 11. Why Do We Need Sets?

Sets are extremely useful when we care about:

- Unique values
- Membership checking
- Comparing collections
- Finding missing resources
- Finding unexpected resources
- Removing duplicates

These operations are common in automation.

For example:

```text
Expected servers
       ↓
Compare
       ↑
Running servers
       ↓
Find differences
```

A set makes this kind of comparison simple.

---

# 12. Creating a Set from a List

Suppose we receive duplicate IP addresses:

```python
ips = [
    "10.0.0.1",
    "10.0.0.2",
    "10.0.0.1",
    "10.0.0.3",
    "10.0.0.2"
]
```

We can convert the list to a set:

```python
unique_ips = set(ips)
```

Now duplicate IP addresses are removed.

Conceptually:

```text
List:

10.0.0.1
10.0.0.2
10.0.0.1
10.0.0.3
10.0.0.2

        ↓ set()

Set:

10.0.0.1
10.0.0.2
10.0.0.3
```

---

# 13. Empty Set

A common beginner mistake is:

```python
data = {}
```

This creates an empty dictionary, not an empty set.

An empty set is created with:

```python
data = set()
```

We will learn dictionaries in detail later.

Remember:

```python
{}
```

→ empty dictionary

```python
set()
```

→ empty set

---

# 14. Adding Values to a Set

Use the `add()` method.

```python
ports = {22, 80}

ports.add(443)

print(ports)
```

The set now contains:

```text
22
80
443
```

If we add a value that already exists:

```python
ports.add(80)
```

Python does not create a duplicate.

---

# 15. Removing Values from a Set

Use:

```python
remove()
```

Example:

```python
ports = {22, 80, 443}

ports.remove(80)

print(ports)
```

Now `80` has been removed.

However, `remove()` raises an error if the value does not exist.

---

# 16. `remove()` vs `discard()`

Sets also have:

```python
discard()
```

Example:

```python
ports = {22, 443}

ports.discard(80)
```

No error occurs even though `80` is not present.

Difference:

```text
remove()
→ removes the value
→ raises an error if value doesn't exist

discard()
→ removes the value
→ does nothing if value doesn't exist
```

This distinction can be useful in automation scripts.

---

# 17. Set Membership

Sets are useful for checking whether a value exists.

Example:

```python
allowed_ports = {22, 80, 443}

if 22 in allowed_ports:
    print("SSH is allowed")
```

Output:

```text
SSH is allowed
```

The `in` operator checks membership.

Conceptually:

```text
Is 22 inside allowed_ports?
          ↓
         YES
          ↓
   SSH is allowed
```

This becomes useful for:

- Port validation
- IP validation
- Server validation
- Permission checking
- Resource checking

---

# 18. Set Order

Sets should not be treated as ordered collections.

For example:

```python
servers = {"web-01", "web-02", "web-03"}

print(servers)
```

The display order should not be relied upon.

If order matters, use a list or another appropriate structure.

The important property of a set is **uniqueness and efficient membership/comparison**, not ordering.

---

# 19. Set Operations

Sets become especially powerful when comparing collections.

Suppose we have:

```python
production = {
    "web-01",
    "web-02",
    "web-03"
}

backup = {
    "web-02",
    "web-03",
    "web-04"
}
```

We can compare them.

---

## Intersection

Intersection finds values present in both sets.

```python
common = production & backup

print(common)
```

Conceptually:

```text
Production:
web-01
web-02
web-03

Backup:
web-02
web-03
web-04

Common:
web-02
web-03
```

---

## Union

Union combines values from both sets.

```python
all_servers = production | backup

print(all_servers)
```

Duplicates are automatically removed.

Conceptually:

```text
web-01
web-02
web-03
web-04
```

---

## Difference

Difference finds values that exist in one set but not the other.

```python
missing = production - backup

print(missing)
```

This means:

> Values in `production` that are not in `backup`.

---

# 20. DevOps Infrastructure Example

Suppose we have the expected infrastructure:

```python
expected_servers = {
    "web-01",
    "web-02",
    "web-03",
    "db-01"
}
```

But the monitoring system reports:

```python
running_servers = {
    "web-01",
    "web-02",
    "db-01"
}
```

We can find missing servers:

```python
missing_servers = expected_servers - running_servers
```

Result:

```text
web-03
```

This is a simple example of **desired state vs actual state**.

```text
Desired state
      ↓
expected_servers
      ↓
     compare
      ↑
running_servers
      ↓
Actual state
```

This concept becomes extremely important later in:

- Terraform
- Kubernetes
- Configuration management
- Cloud automation
- Monitoring

---

# 21. Infrastructure Inventory Project

Our project contains:

```python
expected_servers = {
    "web-01",
    "web-02",
    "web-03",
    "db-01"
}

running_servers = {
    "web-01",
    "web-02",
    "db-01"
}

missing_servers = expected_servers - running_servers
unexpected_servers = running_servers - expected_servers
```

We then display the differences.

The purpose is to simulate a basic infrastructure validation tool.

---

# 22. Complete Project Code

```python
expected_servers = {
    "web-01",
    "web-02",
    "web-03",
    "db-01"
}

running_servers = {
    "web-01",
    "web-02",
    "db-01"
}

missing_servers = expected_servers - running_servers
unexpected_servers = running_servers - expected_servers

print("========== INFRASTRUCTURE CHECK ==========")

print(f"Expected servers: {len(expected_servers)}")
print(f"Running servers: {len(running_servers)}")

print("\nMissing servers:")

if missing_servers:
    for server in missing_servers:
        print(f"- {server}")
else:
    print("None")

print("\nUnexpected servers:")

if unexpected_servers:
    for server in unexpected_servers:
        print(f"- {server}")
else:
    print("None")

print("==========================================")
```

---

# 23. What the Project Demonstrates

This project combines concepts we have already learned:

```text
Sets
  ↓
Set difference
  ↓
Variables
  ↓
if condition
  ↓
for loop
  ↓
f-string
  ↓
len()
  ↓
Terminal output
```

This is important because DevOps scripts are rarely built from one concept.

They combine several small programming concepts to solve a real problem.

---

# 24. How This Helps in DevOps

Tuples and sets have practical applications in infrastructure automation.

### Tuples

Useful for fixed collections such as:

```python
allowed_ports = (22, 80, 443)
```

Possible uses:

- Fixed port configuration
- Fixed environment values
- Fixed coordinates/configuration pairs
- Data that should not be accidentally modified

### Sets

Useful for:

```python
expected_servers = {...}
running_servers = {...}
```

Possible uses:

- Infrastructure inventory
- Unique IP addresses
- Resource IDs
- Server names
- Security groups
- Permission comparisons
- Monitoring checks

---

# 25. Industry Note

Professional DevOps engineers frequently compare **desired state** with **actual state**.

For example:

```text
Desired:
10 EC2 instances

Actual:
8 EC2 instances
```

An automation script can detect:

```text
2 instances missing
```

Python sets can help represent and compare these collections.

Later, instead of hardcoded server names, our scripts can obtain real information from:

```text
AWS APIs
Kubernetes APIs
Linux systems
Configuration files
Monitoring systems
```

Then Python can compare the results.

---

# 26. Connection to the Future Roadmap

Today's concepts will appear again later.

```text
Tuples / Sets
      ↓
Data processing
      ↓
File handling
      ↓
JSON / YAML
      ↓
Linux automation
      ↓
APIs
      ↓
AWS boto3
      ↓
Infrastructure inventory
      ↓
Monitoring
      ↓
Kubernetes automation
```

For example, later we may retrieve EC2 instances using `boto3`:

```text
AWS
 ↓
boto3
 ↓
Get EC2 instances
 ↓
Python set
 ↓
Compare with expected resources
 ↓
Report differences
```

---

# 27. Common Mistakes

## Mistake 1 — Trying to modify a tuple

```python
ports = (22, 80, 443)

ports.append(8080)
```

This fails because tuples don't support `append()`.

---

## Mistake 2 — Thinking `{}` creates a set

```python
data = {}
```

This creates an empty dictionary.

Use:

```python
data = set()
```

for an empty set.

---

## Mistake 3 — Expecting set order

Don't write code that depends on:

```python
print(my_set)
```

producing a specific order.

---

## Mistake 4 — Using `remove()` when an item may not exist

```python
servers.remove("web-99")
```

This can raise:

```text
KeyError
```

If absence is acceptable:

```python
servers.discard("web-99")
```

---

# 28. Tuple vs List vs Set

| Feature | List | Tuple | Set |
|---|---|---|---|
| Syntax | `[ ]` | `( )` | `{ }` |
| Ordered | Yes | Yes | No |
| Mutable | Yes | No | Yes |
| Duplicates | Yes | Yes | No |
| Indexing | Yes | Yes | No |
| Main purpose | Changeable collection | Fixed collection | Unique values/comparison |

A useful mental model:

```text
LIST
"Things that can change"

TUPLE
"Things that should stay fixed"

SET
"Unique things I need to compare/check"
```

---

# 29. Cheat Sheet

### Create a tuple

```python
ports = (22, 80, 443)
```

### Access tuple item

```python
print(ports[0])
```

### Loop through tuple

```python
for port in ports:
    print(port)
```

### Create a set

```python
servers = {"web-01", "web-02"}
```

### Create an empty set

```python
servers = set()
```

### Add

```python
servers.add("web-03")
```

### Remove

```python
servers.remove("web-03")
```

### Safely discard

```python
servers.discard("web-03")
```

### Membership

```python
if "web-01" in servers:
    print("Found")
```

### Convert list to set

```python
unique_items = set(items)
```

### Intersection

```python
common = set_a & set_b
```

### Union

```python
combined = set_a | set_b
```

### Difference

```python
missing = expected - actual
```

---

# 30. Files for This Lesson

Our GitHub lesson directory:

```text
Lesson-11-Tuples-and-Set/
├── 01_tuples_sets.py
├── 03_infrastructure_inventory.py
└── Lesson_11_Tuples_Sets.md
```

The Python files contain the practical work.

This Markdown file contains the complete lesson documentation.

---

# 31. Git Workflow

After testing the files:

```bash
python3 01_tuples_sets.py
python3 03_infrastructure_inventory.py
```

Check the repository:

```bash
git status
```

Stage the lesson:

```bash
git add python-for-devops/Python-lessons/Lesson-11-Tuples-and-Set/
```

Commit:

```bash
git commit -m "Complete Lesson 11: Tuples and Sets"
```

Push:

```bash
git push
```

---

# 32. Final Summary

In this lesson we learned:

- What tuples are
- Why tuples are immutable
- Tuple indexing
- Tuple looping
- One-item tuple syntax
- What sets are
- Why sets contain unique values
- Creating sets
- Converting lists to sets
- Adding and removing set values
- `remove()` vs `discard()`
- Set membership
- Set intersection
- Set union
- Set difference
- Comparing expected and actual infrastructure

The most important mental model is:

```text
List
 ↓
Changeable collection

Tuple
 ↓
Fixed collection

Set
 ↓
Unique values + comparison
```

These concepts are small, but they become useful building blocks for real DevOps automation.