````markdown
# Advanced Bash — Part 2

## Overview

Advanced Bash helps us write more flexible, reusable, and practical shell scripts.

In Part 2, we learned:

- Bash arrays
- Indexed arrays
- Array indexing
- Array length
- Associative arrays
- String manipulation
- `read`
- Reading multiple values
- Silent input
- `getopts`
- `$OPTARG`
- Command-line options
- Argument validation
- A practical server information script

---

# 1. Bash Arrays

A normal variable stores one value:

```bash
name="Pri"
````

An array can store multiple values:

```bash
servers=("web01" "web02" "web03")
```

Think of an array like this:

```text
servers
   │
   ├── [0] web01
   ├── [1] web02
   └── [2] web03
```

Bash arrays start at index `0`.

---

# 2. Creating an Array

```bash
servers=("web01" "web02" "web03")
```

Access the first element:

```bash
echo "${servers[0]}"
```

Output:

```text
web01
```

Access the second element:

```bash
echo "${servers[1]}"
```

Output:

```text
web02
```

Access the third element:

```bash
echo "${servers[2]}"
```

Output:

```text
web03
```

---

# 3. Display the Entire Array

```bash
echo "${servers[@]}"
```

Output:

```text
web01 web02 web03
```

`${servers[@]}` means:

> All elements of the array.

---

# 4. Count Array Elements

```bash
echo "${#servers[@]}"
```

Output:

```text
3
```

Here:

* `${servers[@]}` → all elements
* `${#servers[@]}` → number of elements

---

# 5. Loop Through an Array

Arrays are especially useful with loops.

```bash
#!/bin/bash

servers=("web01" "web02" "web03")

for server in "${servers[@]}"; do
    echo "Checking $server"
done
```

Output:

```text
Checking web01
Checking web02
Checking web03
```

The flow is:

```text
servers array
     ↓
web01 → loop
     ↓
web02 → loop
     ↓
web03 → loop
```

---

# 6. DevOps Example — Multiple Servers

```bash
#!/bin/bash

servers=("web01" "web02" "web03")

for server in "${servers[@]}"; do
    echo "Checking server: $server"
done
```

Output:

```text
Checking server: web01
Checking server: web02
Checking server: web03
```

This pattern can be used when automation needs to process:

* Multiple servers
* Multiple files
* Multiple services
* Multiple environments
* Multiple directories

---

# 7. Adding an Element to an Array

Existing array:

```bash
servers=("web01" "web02" "web03")
```

Add another server:

```bash
servers+=("web04")
```

Display the array:

```bash
echo "${servers[@]}"
```

Output:

```text
web01 web02 web03 web04
```

---

# 8. Associative Arrays

Bash also supports key-value pairs.

Create one using:

```bash
declare -A server_ip
```

Add values:

```bash
server_ip["web01"]="192.168.1.10"
server_ip["web02"]="192.168.1.11"
server_ip["web03"]="192.168.1.12"
```

Access a value:

```bash
echo "${server_ip["web01"]}"
```

Output:

```text
192.168.1.10
```

Think of it like:

```text
web01 → 192.168.1.10
web02 → 192.168.1.11
web03 → 192.168.1.12
```

Associative arrays are useful for configuration-style data.

---

# 9. String Manipulation

Bash can manipulate strings directly.

Example:

```bash
name="DevOps"
```

Find the length:

```bash
echo "${#name}"
```

Output:

```text
6
```

Because:

```text
D e v O p s
1 2 3 4 5 6
```

---

# 10. Convert String to Uppercase

```bash
name="devops"

echo "${name^^}"
```

Output:

```text
DEVOPS
```

`${name^^}` converts the string to uppercase.

---

# 11. Convert String to Lowercase

```bash
name="DEVOPS"

echo "${name,,}"
```

Output:

```text
devops
```

`${name,,}` converts the string to lowercase.

---

# 12. Remove a Prefix

Example:

```bash
filename="backup-server.log"
```

Remove everything through the first `-`:

```bash
echo "${filename#*-}"
```

Output:

```text
server.log
```

`#` removes the shortest matching prefix.

---

# 13. Remove a Suffix

Example:

```bash
filename="backup-server.log"
```

Remove the file extension:

```bash
echo "${filename%.*}"
```

Output:

```text
backup-server
```

`%` removes the shortest matching suffix.

This is useful for manipulating file names.

---

# 14. Replace Text

Example:

```bash
text="Linux is difficult"
```

Replace `difficult` with `easy`:

```bash
echo "${text/difficult/easy}"
```

Output:

```text
Linux is easy
```

---

# 15. Replace All Occurrences

Example:

```bash
text="Linux Linux Linux"
```

Replace every `Linux`:

```bash
echo "${text//Linux/DevOps}"
```

Output:

```text
DevOps DevOps DevOps
```

Difference:

```text
${text/old/new}
```

Replaces the first matching occurrence.

```text
${text//old/new}
```

Replaces all matching occurrences.

---

# 16. `read`

The `read` command gets input from the user.

Example:

```bash
#!/bin/bash

read -p "Enter your name: " name

echo "Hello $name"
```

Run:

```bash
bash script.sh
```

Example:

```text
Enter your name: Pri
Hello Pri
```

---

# 17. Understanding `read -p`

This:

```bash
read -p "Enter your name: " name
```

can be understood as:

```text
read
 │
 ├── -p
 │    └── display a prompt
 │
 └── name
      └── store the input in this variable
```

---

# 18. Reading Multiple Values

Bash can read multiple values at once.

```bash
#!/bin/bash

read -p "Enter first name and role: " name role

echo "Name: $name"
echo "Role: $role"
```

Input:

```text
Pri DevOps
```

Output:

```text
Name: Pri
Role: DevOps
```

---

# 19. Silent Input

The `-s` option hides what the user types.

This is useful for passwords.

```bash
read -s -p "Enter password: " password
echo
```

Example:

```text
Enter password:
```

The password is not displayed while typing.

`-s` means:

> Silent input.

---

# 20. What Is `getopts`?

`getopts` allows a Bash script to process command-line options.

For example:

```bash
./script.sh -n Pri -r DevOps
```

Instead of simply:

```bash
./script.sh Pri DevOps
```

The options make the command easier to understand.

---

# 21. Basic `getopts` Example

Create the script:

```bash
nano options.sh
```

Add:

```bash
#!/bin/bash

name=""
role=""

while getopts "n:r:" opt; do
    case "$opt" in
        n)
            name="$OPTARG"
            ;;
        r)
            role="$OPTARG"
            ;;
        *)
            echo "Usage: $0 -n name -r role"
            exit 1
            ;;
    esac
done

echo "Name: $name"
echo "Role: $role"
```

Make it executable:

```bash
chmod +x options.sh
```

Run:

```bash
./options.sh -n Pri -r DevOps
```

Output:

```text
Name: Pri
Role: DevOps
```

---

# 22. Understanding `getopts "n:r:"`

This:

```bash
getopts "n:r:" opt
```

defines two options:

```text
n: → -n requires a value
r: → -r requires a value
```

Therefore:

```bash
-n Pri
```

is valid.

And:

```bash
-r DevOps
```

is valid.

The colon means:

> This option expects an argument/value.

---

# 23. `$OPTARG`

`OPTARG` contains the value supplied to an option.

For example:

```bash
./options.sh -n Pri
```

The value:

```text
Pri
```

is available through:

```bash
$OPTARG
```

Therefore:

```bash
name="$OPTARG"
```

stores the supplied value inside `name`.

---

# 24. Why `getopts` Is Useful

Compare:

```bash
./script.sh Pri DevOps
```

with:

```bash
./script.sh -n Pri -r DevOps
```

The second form clearly tells us:

```text
-n → name
-r → role
```

This becomes useful when a script accepts many parameters.

---

# 25. Combining `getopts` With Validation

A professional script should not blindly trust user input.

We can check whether required arguments were provided.

Example:

```bash
if [ -z "$name" ] || [ -z "$role" ]; then
    echo "Error: name and role are required."
    exit 1
fi
```

`-z` checks whether a string is empty.

Therefore:

```text
-z "$name"
```

means:

> Is `name` empty?

---

# 26. Mini Project — Server Information Script

Create:

```bash
nano server-info.sh
```

Add:

```bash
#!/bin/bash

set -euo pipefail

name=""
environment=""

while getopts "n:e:" opt; do
    case "$opt" in
        n)
            name="$OPTARG"
            ;;
        e)
            environment="$OPTARG"
            ;;
        *)
            echo "Usage: $0 -n server-name -e environment"
            exit 1
            ;;
    esac
done

if [ -z "$name" ] || [ -z "$environment" ]; then
    echo "Error: server name and environment are required."
    echo "Usage: $0 -n server-name -e environment"
    exit 1
fi

echo "===== SERVER INFO ====="
echo "Server: $name"
echo "Environment: $environment"
echo "Status: Ready"
echo "======================"
```

Make it executable:

```bash
chmod +x server-info.sh
```

Run:

```bash
./server-info.sh -n web01 -e production
```

Expected output:

```text
===== SERVER INFO =====
Server: web01
Environment: production
Status: Ready
======================
```

---

# 27. Testing Missing Arguments

Run:

```bash
./server-info.sh
```

Expected output:

```text
Error: server name and environment are required.
Usage: ./server-info.sh -n server-name -e environment
```

The script exits with:

```text
1
```

because required arguments were missing.

---

# 28. DevOps Connection

These concepts are useful in real automation.

For example:

```text
Bash Script
     ↓
Accept arguments
     ↓
Validate arguments
     ↓
Process servers/files
     ↓
Perform automation
     ↓
Return exit status
```

Arrays can represent multiple servers:

```text
web01
web02
web03
```

`getopts` can accept configuration:

```text
-n web01
-e production
```

`read` can collect interactive input.

String manipulation can process:

```text
server names
file names
log lines
configuration values
```

These are common building blocks of Linux and DevOps automation.

---

# 29. Important Cheat Sheet

| Syntax / Command   | Purpose                       |
| ------------------ | ----------------------------- |
| `array=("a" "b")`  | Create indexed array          |
| `${array[0]}`      | Access an element             |
| `${array[@]}`      | Get all elements              |
| `${#array[@]}`     | Count elements                |
| `array+=("c")`     | Add element                   |
| `declare -A array` | Create associative array      |
| `${#name}`         | String length                 |
| `${name^^}`        | Uppercase                     |
| `${name,,}`        | Lowercase                     |
| `${text/old/new}`  | Replace first occurrence      |
| `${text//old/new}` | Replace all occurrences       |
| `${text#pattern}`  | Remove shortest prefix        |
| `${text%pattern}`  | Remove shortest suffix        |
| `read variable`    | Read user input               |
| `read -p`          | Read input with prompt        |
| `read -s`          | Silent input                  |
| `getopts`          | Process command-line options  |
| `$OPTARG`          | Value of current option       |
| `-z "$var"`        | Check whether string is empty |

---

# 30. Common Mistakes

## Mistake 1 — Forgetting array indexes start at 0

Wrong assumption:

```text
[1] = first element
```

Correct:

```text
[0] = first element
[1] = second element
[2] = third element
```

---

## Mistake 2 — Forgetting quotes around array expansion

Prefer:

```bash
"${servers[@]}"
```

instead of:

```bash
${servers[@]}
```

Quoting helps preserve individual array elements correctly, especially when values contain spaces.

---

## Mistake 3 — Forgetting the colon in `getopts`

If an option needs a value:

```bash
getopts "n:r:" opt
```

The colon is important.

Without:

```text
n:
```

Bash does not know that `-n` requires an argument.

---

## Mistake 4 — Not validating arguments

Don't assume users will always provide the correct input.

Always consider:

```bash
if [ -z "$name" ]; then
    echo "Name is required"
    exit 1
fi
```

---

## Mistake 5 — Using `read` for automation when arguments are better

Interactive:

```bash
read -p "Enter server: " server
```

Automation-friendly:

```bash
./script.sh -s web01
```

For DevOps automation, command-line arguments are often preferable because CI/CD systems can provide them automatically.

---

# 31. Advanced Bash — Part 2 Summary

We learned:

1. Indexed arrays
2. Array indexing
3. Array length
4. Array loops
5. Adding array elements
6. Associative arrays
7. String length
8. Uppercase conversion
9. Lowercase conversion
10. Prefix removal
11. Suffix removal
12. Text replacement
13. `read`
14. Multiple input values
15. Silent input
16. `getopts`
17. `$OPTARG`
18. Command-line options
19. Argument validation
20. A practical server information script

The progression is:

```text
Basic Bash
    ↓
Variables
    ↓
Conditions
    ↓
Loops
    ↓
Functions
    ↓
Advanced Bash
    ↓
Arrays + Strings + Input
    ↓
Command-line arguments
    ↓
Reliable automation
```

---

# Your Turn

Practice these commands:

### 1. Create an array

```bash
servers=("web01" "web02" "db01" "db02")
```

Print all servers.

### 2. Count the servers

Print the number of elements.

### 3. Loop through the servers

Print:

```text
Checking web01
Checking web02
Checking db01
Checking db02
```

### 4. String manipulation

Create:

```bash
filename="backup-server.log"
```

Extract:

```text
backup-server
```

without `.log`.

### 5. Uppercase

Convert:

```text
devops
```

into:

```text
DEVOPS
```

### 6. `read`

Create a script that asks:

```text
Enter your name:
```

and prints:

```text
Hello <name>
```

### 7. `getopts`

Modify `server-info.sh` so it accepts:

```bash
-n server-name
-e environment
```

and rejects missing values.

### 8. Debugging

Run your script with:

```bash
bash -x server-info.sh -n web01 -e production
```

Observe how Bash executes each command.

---

# Next Lesson

## Advanced Bash — Part 3

Next we will cover:

* `stdin`
* `stdout`
* `stderr`
* Advanced redirection
* `2>`
* `2>&1`
* `&>`
* `tee`
* `trap`
* Signals
* Temporary files
* Logging
* Functions with return values
* Robust argument validation
* A larger Bash automation project

```
```
