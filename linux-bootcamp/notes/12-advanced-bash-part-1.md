# Advanced Bash — Part 1

## 1. Overview

Advanced Bash helps us write shell scripts that are more reliable, safer, and easier to debug.

In basic Bash scripting, we learned:

* Variables
* Conditions
* Loops
* Functions
* Arguments
* Exit codes

Now we are learning how to make scripts behave more like reliable DevOps automation tools.

---

# 2. Exit Status

Every Linux command finishes with an **exit status**.

The exit status tells us whether the command succeeded or failed.

### Important rule

```text
0       = Success
Non-zero = Failure
```

For example:

```bash
ls
echo $?
```

Possible output:

```text
0
```

This means `ls` succeeded.

Now try:

```bash
ls /does-not-exist
echo $?
```

Possible output:

```text
ls: cannot access '/does-not-exist': No such file or directory
2
```

The non-zero value means the command failed.

---

## 3. `$?`

`$?` contains the exit status of the **most recently executed command**.

Example:

```bash
mkdir test
echo $?
```

Output:

```text
0
```

The `mkdir` command succeeded.

Another example:

```bash
mkdir test
echo $?
```

If the directory already exists, you may see:

```text
mkdir: cannot create directory ‘test’: File exists
1
```

The command failed, so the exit status is non-zero.

---

## 4. Important Rule About `$?`

`$?` changes after every command.

Example:

```bash
ls
echo "Hello"
echo $?
```

The `$?` here belongs to:

```bash
echo "Hello"
```

NOT:

```bash
ls
```

Because `echo "Hello"` was executed immediately before `$?`.

---

# 5. `set -e`

`set -e` tells Bash:

> Stop the script when a command fails.

Example:

```bash
#!/bin/bash

set -e

echo "Starting..."

ls /does-not-exist

echo "This will not run"
```

Run:

```bash
bash script.sh
```

Output will look similar to:

```text
Starting...
ls: cannot access '/does-not-exist': No such file or directory
```

The script stops after the failed command.

Without `set -e`, Bash may continue executing later commands.

---

## Why `set -e` is useful

Imagine a deployment script:

```text
Install software
      ↓
Copy configuration
      ↓
Restart service
      ↓
Deployment complete
```

If copying the configuration fails, we usually don't want the script to continue and restart the service using an old or broken configuration.

`set -e` helps stop the script early.

---

# 6. `set -u`

`set -u` tells Bash:

> Treat an unset variable as an error.

Example:

```bash
#!/bin/bash

set -u

echo "$username"
```

If `username` was never defined, Bash reports an error similar to:

```text
username: unbound variable
```

Without `set -u`, an unset variable can behave like an empty string.

---

## Example

Without `set -u`:

```bash
#!/bin/bash

echo "User: $username"
```

Possible output:

```text
User:
```

This can hide mistakes.

With:

```bash
set -u
```

Bash immediately tells us that the variable was never defined.

---

# 7. `set -o pipefail`

Normally, when commands are connected using a pipe:

```bash
command1 | command2
```

the exit status normally comes from the **last command**.

This can hide failures in earlier commands.

`pipefail` changes this behavior.

```bash
set -o pipefail
```

Now a pipeline fails if an important command in the pipeline fails.

---

## Example

```bash
set -o pipefail

cat /does-not-exist | grep hello
echo $?
```

Because `cat` failed, the pipeline reports a failure.

---

# 8. The Safe Bash Combination

A very common pattern in reliable Bash scripts is:

```bash
set -euo pipefail
```

This combines:

```text
-e
│
└── Stop when commands fail

-u
│
└── Detect unset variables

-o pipefail
│
└── Detect failures inside pipelines
```

Example:

```bash
#!/bin/bash

set -euo pipefail

echo "Script started"

name="Pri"

echo "Hello $name"

ls /tmp

echo "Script completed successfully"
```

This is a common starting point for production-oriented Bash scripts.

---

# 9. `&&`

`&&` means:

> Run the next command only if the previous command succeeds.

Syntax:

```bash
command1 && command2
```

Example:

```bash
mkdir test && echo "Directory created"
```

If `mkdir` succeeds:

```text
Directory created
```

If `mkdir` fails, the `echo` command does not run.

---

## DevOps Example

```bash
sudo apt update && sudo apt upgrade
```

The second command runs only if the first command succeeds.

---

# 10. `||`

`||` means:

> Run the next command only if the previous command fails.

Syntax:

```bash
command1 || command2
```

Example:

```bash
ls /does-not-exist || echo "Directory does not exist"
```

Output:

```text
ls: cannot access '/does-not-exist': No such file or directory
Directory does not exist
```

Because `ls` failed, the `echo` command ran.

---

# 11. Combining `&&` and `||`

We can create simple success/failure logic.

Example:

```bash
mkdir backup && echo "Backup directory created" || echo "Backup creation failed"
```

Conceptually:

```text
mkdir backup
     │
     ├── success → echo "Backup directory created"
     │
     └── failure → echo "Backup creation failed"
```

---

# 12. Explicit Error Handling with `if`

For important scripts, explicit `if` statements are often clearer than complicated `&&` / `||` chains.

Example:

```bash
#!/bin/bash

if mkdir backup; then
    echo "Backup directory created"
else
    echo "Failed to create backup directory"
    exit 1
fi
```

The structure is:

```text
if command succeeds
        ↓
    success code
        ↓
else
        ↓
    failure code
        ↓
    exit 1
```

This is easier to understand and extend.

---

# 13. `exit`

`exit` terminates a Bash script.

Syntax:

```bash
exit STATUS
```

Example:

```bash
exit 0
```

means:

```text
Script completed successfully
```

Example:

```bash
exit 1
```

means:

```text
Script failed
```

---

## Example

```bash
#!/bin/bash

echo "Checking server..."

if [ -d /etc ]; then
    echo "Server check successful"
    exit 0
else
    echo "Server check failed"
    exit 1
fi
```

Check the exit status:

```bash
bash script.sh
echo $?
```

Successful output:

```text
Checking server...
Server check successful
0
```

---

# 14. Why Exit Codes Matter in DevOps

Exit codes are extremely important in automation.

For example:

```text
Bash script
     ↓
CI/CD pipeline
     ↓
Did script return 0?
     ↓
 ┌───────────────┐
 │               │
Yes             No
 │               │
 ↓               ↓
Continue       Stop/fail
deployment     pipeline
```

CI/CD systems use exit codes to determine whether commands succeeded.

Therefore:

```text
0 → success
non-zero → failure
```

is one of the most important concepts in Linux automation.

---

# 15. Debugging Bash with `bash -x`

`bash -x` runs a script in **debug/trace mode**.

It shows commands as Bash executes them.

Example:

```bash
bash -x script.sh
```

Suppose the script contains:

```bash
#!/bin/bash

name="Pri"

echo "Hello $name"
```

Run:

```bash
bash -x script.sh
```

Possible output:

```text
+ name=Pri
+ echo 'Hello Pri'
Hello Pri
```

The `+` lines show the commands being executed.

---

# 16. Why `bash -x` Is Useful

Suppose a script is not behaving as expected.

Instead of only seeing:

```text
Something went wrong
```

we can run:

```bash
bash -x script.sh
```

and observe the execution step by step.

For example:

```text
+ name=Pri
+ number=10
+ '[' 10 -gt 20 ']'
+ echo 'Number is small'
Number is small
```

This helps us understand what Bash actually executed.

---

# 17. `set -x`

We can also enable debugging from inside a script.

```bash
set -x
```

Example:

```bash
#!/bin/bash

name="Pri"

set -x

echo "Hello $name"
echo "Learning DevOps"
```

The commands after `set -x` are traced.

---

# 18. `set +x`

To stop tracing:

```bash
set +x
```

Example:

```bash
#!/bin/bash

set -x

name="Pri"

echo "Hello $name"

set +x

echo "Debugging stopped"
```

Concept:

```text
set -x
   ↓
Debugging ON

set +x
   ↓
Debugging OFF
```

---

# 19. `bash -x` vs `set -x`

### `bash -x`

Used when starting the script:

```bash
bash -x script.sh
```

It traces the script execution.

### `set -x`

Used inside the script:

```bash
set -x
```

It enables tracing from that point onward.

### `set +x`

Disables tracing:

```bash
set +x
```

---

# 20. Recommended Bash Script Starting Point

For reliable automation scripts, a common pattern is:

```bash
#!/bin/bash

set -euo pipefail
```

Then write the script normally.

Example:

```bash
#!/bin/bash

set -euo pipefail

echo "===== SERVER CHECK ====="

hostname
whoami

echo "===== CHECK COMPLETE ====="
```

This gives the script stronger error handling than a completely unprotected Bash script.

---

# 21. Real DevOps Connection

These concepts are directly useful in:

* Server automation
* Deployment scripts
* Backup scripts
* Linux administration
* CI/CD pipelines
* Docker entrypoint scripts
* Monitoring scripts
* Log-processing scripts
* Cloud automation
* Infrastructure automation

Example:

```text
Developer
   ↓
Git push
   ↓
CI/CD pipeline
   ↓
Bash automation
   ↓
Linux server
   ↓
Application deployment
```

If a Bash command fails, the exit code can tell the CI/CD system:

```text
0       → Continue
non-zero → Fail deployment
```

---

# 22. Important Commands Cheat Sheet

| Command                | Purpose                             |           |                                |
| ---------------------- | ----------------------------------- | --------- | ------------------------------ |
| `echo $?`              | Show previous command's exit status |           |                                |
| `set -e`               | Stop script when a command fails    |           |                                |
| `set -u`               | Treat unset variables as errors     |           |                                |
| `set -o pipefail`      | Detect failures inside pipelines    |           |                                |
| `set -euo pipefail`    | Enable all three protections        |           |                                |
| `command1 && command2` | Run command2 if command1 succeeds   |           |                                |
| `command1              |                                     | command2` | Run command2 if command1 fails |
| `exit 0`               | Exit successfully                   |           |                                |
| `exit 1`               | Exit with failure                   |           |                                |
| `bash -x script.sh`    | Run script with debugging           |           |                                |
| `set -x`               | Enable debugging inside script      |           |                                |
| `set +x`               | Disable debugging                   |           |                                |

---

# 23. Common Mistakes

## Mistake 1 — Checking `$?` too late

Wrong:

```bash
ls
echo "Done"
echo $?
```

Here `$?` belongs to:

```bash
echo "Done"
```

Correct:

```bash
ls
echo $?
```

---

## Mistake 2 — Thinking every non-zero code is exactly `1`

Not necessarily.

Linux commands can return different non-zero values.

For example:

```text
0 → success
1 → generic failure
2 → another type of error
```

The important distinction is:

```text
0     = success
!= 0  = failure
```

---

## Mistake 3 — Forgetting `pipefail`

Using:

```bash
set -e
```

does not by itself make every pipeline failure behave as expected.

For robust pipelines, use:

```bash
set -euo pipefail
```

---

## Mistake 4 — Debugging without `bash -x`

Instead of guessing why a script behaves incorrectly, use:

```bash
bash -x script.sh
```

This lets you see Bash's execution flow.

---

# 24. Key Mental Model

Remember this:

```text
COMMAND
   ↓
Exit status
   ↓
┌───────────────┐
│ 0             │ non-zero
│               │
Success         Failure
│               │
↓               ↓
Continue        Handle error
```

And for safer scripts:

```text
set -e
   +
set -u
   +
pipefail
   ↓
More reliable Bash automation
```

---

# 25. Advanced Bash — Part 1 Summary

We learned:

1. Exit status
2. `$?`
3. `set -e`
4. `set -u`
5. `set -o pipefail`
6. `set -euo pipefail`
7. `&&`
8. `||`
9. Explicit error handling with `if`
10. `exit 0`
11. `exit 1`
12. `bash -x`
13. `set -x`
14. `set +x`
15. Why these concepts matter in DevOps

The main goal is to move from:

```text
Basic Bash scripts
```

to:

```text
Reliable Bash automation
```

---

# Your Turn

Before moving to Advanced Bash — Part 2, make sure you understand:

1. What does exit status `0` mean?
2. What does a non-zero exit status mean?
3. What does `$?` contain?
4. What does `set -e` do?
5. What does `set -u` protect against?
6. Why is `pipefail` useful?
7. What does `set -euo pipefail` provide?
8. What is the difference between `&&` and `||`?
9. What does `exit 1` mean?
10. How do you debug a Bash script using `bash -x`?
11. What is the difference between `set -x` and `bash -x`?
12. Why are exit codes important in CI/CD?

---

# Next Lesson

## Advanced Bash — Part 2

Next we will cover:

* Arrays
* String manipulation
* `read`
* `getopts`
* Advanced redirection
* `stdin`
* `stdout`
* `stderr`
* `trap`
* Signals
* Temporary files
* Logging
* Functions with return values
* Robust argument validation

These are important for writing **real Linux/DevOps automation scripts**.
