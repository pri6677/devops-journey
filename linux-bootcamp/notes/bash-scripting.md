# Bash Scripting Fundamentals

## 1. Introduction to Bash Scripting

Bash scripting allows us to automate Linux commands and operations by placing commands inside a script file.

A Bash script normally starts with:

```bash
#!/bin/bash
```

This is called a **shebang**. It tells Linux to execute the script using Bash.

Example:

```bash
#!/bin/bash

echo "Hello, Pri!"
echo "Welcome to Bash scripting."
```

Run a script with:

```bash
bash script.sh
```

Or make it executable:

```bash
chmod +x script.sh
./script.sh
```

---

## 2. Executing a Script

There are two common ways to run a Bash script.

### Using Bash directly

```bash
bash hello.sh
```

The file does not need execute permission.

### Executing the file directly

```bash
chmod +x hello.sh
./hello.sh
```

The `x` permission means the file is executable.

Check permissions:

```bash
ls -l hello.sh
```

Example:

```text
-rwxrwxr-x
```

---

# 3. Bash Variables

Variables store values.

```bash
NAME="Pri"
ROLE="Cloud Engineer"
```

Read a variable using `$`:

```bash
echo "$NAME"
echo "$ROLE"
```

Example:

```bash
NAME="Pri"
PROJECT="DevOps"

echo "I am learning $PROJECT"
```

Output:

```text
I am learning DevOps
```

### Important rule

There must be **no spaces** around `=`:

Correct:

```bash
NAME="Pri"
```

Incorrect:

```bash
NAME = "Pri"
```

---

# 4. Environment Variables

Linux already provides many environment variables.

Useful examples:

```bash
echo "$USER"
echo "$HOME"
echo "$SHELL"
echo "$PATH"
echo "$PWD"
echo "$HOSTNAME"
```

`printenv` displays environment variables:

```bash
printenv
```

Example:

```text
USER=pri
HOME=/home/pri
SHELL=/bin/bash
```

---

# 5. Shell Variables vs Environment Variables

A normal variable belongs to the current shell:

```bash
NAME="Pri"
```

A child Bash shell does not automatically receive it.

To make a variable available to child processes:

```bash
export NAME="Pri"
```

Now:

```bash
bash
echo "$NAME"
```

will still show:

```text
Pri
```

This distinction is important when working with automation, configuration, CI/CD pipelines, and DevOps tools.

---

# 6. `.bashrc`

The file:

```text
~/.bashrc
```

contains Bash configuration for interactive non-login shells.

View it:

```bash
ls -la ~/.bashrc
head -20 ~/.bashrc
```

A variable can be placed inside `.bashrc`:

```bash
export MY_NAME="Pri"
```

After modifying `.bashrc`, reload it:

```bash
source ~/.bashrc
```

Then:

```bash
echo "$MY_NAME"
```

Output:

```text
Pri
```

### `source`

`source` executes a file in the **current shell**.

```bash
source ~/.bashrc
```

This is different from:

```bash
bash ~/.bashrc
```

`.bashrc` is intended to be sourced for shell configuration.

---

# 7. `PATH`

`PATH` tells Bash where to search for executable commands.

View it:

```bash
echo "$PATH"
```

Example:

```text
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Each directory is separated by `:`.

For example:

```bash
which ls
```

may return:

```text
/usr/bin/ls
```

If `/usr/bin` is removed from `PATH`, Bash may no longer find `ls`:

```bash
PATH=/tmp
ls
```

Bash then reports that `ls` cannot be found.

However, the executable still exists:

```bash
/usr/bin/ls
```

This demonstrates the difference between:

* the command existing
* Bash being able to locate it through `PATH`

---

# 8. `type`

`type` tells us what a command actually is.

```bash
type ls
```

Example:

```text
ls is aliased to `ls --color=auto'
```

Check multiple possibilities:

```bash
type -a ls
```

Example:

```text
ls is aliased to `ls --color=auto'
ls is /usr/bin/ls
ls is /bin/ls
```

Other examples:

```bash
type cd
type python3
```

`cd` is a Bash builtin.

---

# 9. `command -v`

`command -v` can be used to determine how Bash resolves a command.

```bash
command -v ls
command -v cd
command -v python3
```

For an alias, it may show:

```text
alias ls='ls --color=auto'
```

For an executable:

```text
/usr/bin/python3
```

---

# 10. Bash Functions

Functions allow us to group commands and reuse them.

Basic function:

```bash
hello() {
    echo "Hello, Pri!"
}
```

Run it:

```bash
hello
```

Output:

```text
Hello, Pri!
```

Check its type:

```bash
type hello
```

Output:

```text
hello is a function
```

---

# 11. Functions with Arguments

Functions can receive arguments using positional parameters.

```bash
hello() {
    echo "Hello, $1!"
}
```

Run:

```bash
hello Pri
```

Output:

```text
Hello, Pri!
```

Here:

```text
$1 → first argument
```

---

## Multiple Function Arguments

```bash
user_info() {
    echo "Name: $1"
    echo "Role: $2"
}
```

Run:

```bash
user_info Pri "Cloud Engineer"
```

Output:

```text
Name: Pri
Role: Cloud Engineer
```

Quotes are important when an argument contains spaces.

---

# 12. Function Argument Variables

Important positional parameters:

| Variable | Meaning             |
| -------- | ------------------- |
| `$1`     | First argument      |
| `$2`     | Second argument     |
| `$#`     | Number of arguments |
| `$@`     | All arguments       |

Example:

```bash
show_args() {
    echo "Number of arguments: $#"
    echo "Arguments: $@"
}
```

Run:

```bash
show_args Pri DevOps Linux Docker
```

Output:

```text
Number of arguments: 4
Arguments: Pri DevOps Linux Docker
```

---

# 13. Script Arguments

The same positional parameter system applies to scripts.

Example:

```bash
#!/bin/bash

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "Number of arguments: $#"
echo "All arguments: $@"
```

Run:

```bash
./arguments.sh Pri DevOps Linux Docker
```

Output:

```text
Script name: ./arguments.sh
First argument: Pri
Second argument: DevOps
Number of arguments: 4
All arguments: Pri DevOps Linux Docker
```

---

# 14. Input Validation

Scripts should validate their input before doing work.

Example:

```bash
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <name> <role>"
    exit 1
fi

echo "Name: $1"
echo "Role: $2"
```

Without arguments:

```bash
./validate.sh
```

Output:

```text
Usage: ./validate.sh <name> <role>
```

Exit status:

```bash
echo $?
```

Output:

```text
1
```

With valid arguments:

```bash
./validate.sh Pri "Cloud Engineer"
```

Output:

```text
Name: Pri
Role: Cloud Engineer
```

Exit status:

```bash
echo $?
```

Output:

```text
0
```

---

# 15. Exit Status

Every Linux command finishes with an exit status.

Generally:

```text
0     → success
non-0 → failure/error
```

The previous command's exit status is available through:

```bash
echo $?
```

Example:

```bash
mkdir test
echo $?
```

If successful:

```text
0
```

If an operation fails:

```text
1
```

Exit statuses are extremely important in automation because scripts and CI/CD systems use them to determine whether an operation succeeded.

---

# 16. Numeric Comparisons

Bash uses special operators for numeric comparisons.

| Operator | Meaning               |
| -------- | --------------------- |
| `-eq`    | Equal                 |
| `-ne`    | Not equal             |
| `-gt`    | Greater than          |
| `-lt`    | Less than             |
| `-ge`    | Greater than or equal |
| `-le`    | Less than or equal    |

Example:

```bash
if [ "$1" -gt 10 ]; then
    echo "The number is greater than 10."
elif [ "$1" -eq 10 ]; then
    echo "The number is exactly 10."
else
    echo "The number is less than 10."
fi
```

---

# 17. String Comparisons

Strings can also be compared.

Example:

```bash
if [ "$1" = "DevOps" ]; then
    echo "You are learning DevOps."
else
    echo "You are learning something else."
fi
```

Run:

```bash
./check-role.sh DevOps
```

Output:

```text
You are learning DevOps.
```

Run:

```bash
./check-role.sh Developer
```

Output:

```text
You are learning something else.
```

For strings:

```bash
[ "$1" = "DevOps" ]
```

For numbers:

```bash
[ "$1" -eq 10 ]
```

---

# 18. `if`, `elif`, and `else`

Bash can make decisions:

```bash
if condition
then
    command
elif another_condition
then
    command
else
    command
fi
```

Example:

```bash
if [ "$1" -gt 10 ]; then
    echo "Greater than 10"
elif [ "$1" -eq 10 ]; then
    echo "Exactly 10"
else
    echo "Less than 10"
fi
```

This allows scripts to react differently depending on conditions.

---

# 19. `&&`

`&&` means:

> Run the next command only if the previous command succeeds.

Example:

```bash
mkdir devops-test && echo "Directory created"
```

If `mkdir` succeeds:

```text
Directory created
```

If it fails, the `echo` command does not run.

---

# 20. `||`

`||` means:

> Run the next command only if the previous command fails.

Example:

```bash
cd /does-not-exist || echo "Directory not found"
```

The `cd` command fails, so the `echo` command executes:

```text
Directory not found
```

These operators are very common in DevOps automation.

---

# 21. `case`

`case` is useful when there are multiple possible choices.

Example:

```bash
case "$1" in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        echo "Restarting service..."
        ;;
    status)
        echo "Checking service status..."
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
```

Run:

```bash
./service.sh start
```

```text
Starting service...
```

Run:

```bash
./service.sh stop
```

```text
Stopping service...
```

Run:

```bash
./service.sh restart
```

```text
Restarting service...
```

Run:

```bash
./service.sh status
```

```text
Checking service status...
```

The `*` case handles anything that doesn't match the defined choices.

---

# 22. `for` Loops

A `for` loop repeats commands for each item in a list.

Example:

```bash
for item in Linux Python Docker Kubernetes
do
    echo "Learning: $item"
done
```

Output:

```text
Learning: Linux
Learning: Python
Learning: Docker
Learning: Kubernetes
```

Conceptually:

```text
item = Linux
       ↓
run commands

item = Python
       ↓
run commands

item = Docker
       ↓
run commands

item = Kubernetes
       ↓
run commands
```

---

# 23. `while` Loops

A `while` loop continues while a condition is true.

Example:

```bash
count=1

while [ $count -le 5 ]
do
    echo "Count: $count"
    count=$((count + 1))
done
```

Output:

```text
Count: 1
Count: 2
Count: 3
Count: 4
Count: 5
```

The variable must change:

```bash
count=$((count + 1))
```

Otherwise the condition could remain true forever, creating an infinite loop.

---

# 24. Checking Commands with `command -v`

A practical Bash script can check whether required commands are available.

Example:

```bash
for command in bash python3 ssh
do
    if command -v "$command" > /dev/null 2>&1; then
        echo "$command: available"
    else
        echo "$command: NOT FOUND"
    fi
done
```

This checks whether:

```text
bash
python3
ssh
```

can be found through the current `PATH`.

---

# 25. Practical Project: Server Check

The Bash project created during this lesson combines variables, loops, conditions, and command detection.

```bash
#!/bin/bash

echo "===== SERVER CHECK ====="

echo "Hostname: $HOSTNAME"
echo "User: $USER"

echo
echo "Checking required commands..."

for command in bash python3 ssh
do
    if command -v "$command" > /dev/null 2>&1; then
        echo "$command: available"
    else
        echo "$command: NOT FOUND"
    fi
done

echo
echo "===== CHECK COMPLETE ====="
```

Example output:

```text
===== SERVER CHECK =====
Hostname: smarty
User: pri

Checking required commands...
bash: available
python3: available
ssh: available

===== CHECK COMPLETE =====
```

This is a simple example of the type of automation Bash can perform in DevOps.

---

# 26. Bash Scripts Created

The practical Bash scripts from this section are stored in:

```text
linux-bootcamp/projects/bash-scripting/
```

They include:

```text
arguments.sh
check-number.sh
check-role.sh
counter.sh
loop.sh
server-check.sh
service.sh
user-info.sh
validate.sh
```

---

# 27. Key Concepts Learned

```text
Bash
│
├── Scripts
│   ├── shebang
│   ├── chmod +x
│   └── ./script.sh
│
├── Variables
│   ├── local shell variables
│   └── export
│
├── Environment
│   ├── $USER
│   ├── $HOME
│   ├── $SHELL
│   ├── $PATH
│   ├── $PWD
│   └── $HOSTNAME
│
├── Functions
│   ├── $1
│   ├── $2
│   ├── $#
│   └── $@
│
├── Decisions
│   ├── if
│   ├── elif
│   ├── else
│   └── case
│
├── Comparisons
│   ├── -eq
│   ├── -gt
│   ├── -lt
│   └── =
│
├── Command chaining
│   ├── &&
│   └── ||
│
├── Loops
│   ├── for
│   └── while
│
└── Automation
    ├── command -v
    └── exit status
```

---

# 28. DevOps Relevance

Bash is heavily used for:

* Linux administration
* server automation
* deployment scripts
* CI/CD pipelines
* system checks
* backups
* log processing
* installing/configuring software
* managing services
* troubleshooting
* cloud automation

The goal is not to memorize Bash syntax. The goal is to be able to look at a Linux task and think:

```text
Can I automate this?
        ↓
What inputs do I need?
        ↓
What conditions can occur?
        ↓
What commands perform the task?
        ↓
How do I detect success/failure?
        ↓
Can I repeat the task safely?
```

That is the mindset we will carry into DevOps automation.
