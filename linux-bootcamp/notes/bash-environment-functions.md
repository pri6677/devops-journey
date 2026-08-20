# Bash Environment, PATH, Command Lookup & Functions

## Overview

In this lesson, I learned how Bash manages:

- Shell variables
- Environment variables
- `export`
- Child shells
- `.bashrc`
- `source`
- Aliases
- `PATH`
- Command lookup
- `type`
- `command -v`
- Bash functions
- Function arguments
- `$1`, `$2`, `$#`, `$@`
- Argument validation
- `return`
- Exit codes
- `$?`

These concepts are important foundations for Linux administration and DevOps automation.

---

# 1. Shell Variables

A shell variable stores a value inside the current shell.

Example:

```bash
NAME="Pri"
PROJECT="DevOps"
```

Read a variable using `$`:

```bash
echo $NAME
echo $PROJECT
```

Output:

```text
Pri
DevOps
```

The `$` tells Bash to substitute the value stored in the variable.

---

# 2. Environment Variables

Some variables are available to child processes.

Common environment variables include:

```bash
$USER
$HOME
$SHELL
$PATH
$PWD
```

Examples:

```bash
echo $USER
echo $HOME
echo $SHELL
echo $PATH
echo $PWD
```

Example values:

```text
USER=pri
HOME=/home/pri
SHELL=/bin/bash
```

---

# 3. `printenv`

`printenv` displays environment variables.

```bash
printenv
```

It can produce a large amount of output.

A specific variable can be checked with:

```bash
printenv HOME
```

---

# 4. `export`

A normal shell variable belongs to the current shell.

Example:

```bash
NAME="Pri"
```

If a child Bash shell is started:

```bash
bash
```

the child shell does not automatically receive ordinary shell variables.

To make a variable available to child processes:

```bash
export NAME="Pri"
```

Then:

```bash
bash
echo $NAME
```

The child shell can see:

```text
Pri
```

Concept:

```text
Parent Bash
    |
    | export NAME
    v
Child Bash
    |
    └── NAME is available
```

---

# 5. `.bashrc`

The Bash configuration file for interactive non-login Bash shells is:

```text
~/.bashrc
```

Check it:

```bash
ls -la ~/.bashrc
```

View the beginning:

```bash
head -20 ~/.bashrc
```

The file is commonly used for:

- aliases
- functions
- environment variables
- shell configuration
- command-line customization

Example:

```bash
export MY_NAME="Pri"
```

After adding it to `.bashrc`, a new Bash shell can access it.

---

# 6. `source`

Changes made to `.bashrc` do not automatically affect the current shell.

Use:

```bash
source ~/.bashrc
```

This executes the file in the current shell.

Therefore:

```bash
source ~/.bashrc
```

is commonly used after modifying `.bashrc`.

---

# 7. Don't Run `.bashrc` Like a Normal Script

I tested:

```bash
bash ~/.bashrc
```

and received:

```text
return: can only `return' from a function or sourced script
```

This happens because `.bashrc` is designed to be sourced by Bash for interactive shell setup.

The normal method is:

```bash
source ~/.bashrc
```

---

# 8. Aliases

An alias creates a shortcut for a command.

Example:

```bash
alias ll='ls -la'
```

Now:

```bash
ll
```

is a shortcut for:

```bash
ls -la
```

Check an alias:

```bash
type ll
```

Output:

```text
ll is aliased to `ls -la'
```

My system also had:

```bash
alias ls='ls --color=auto'
```

Therefore:

```text
ls
 ↓
ls --color=auto
 ↓
/usr/bin/ls
```

---

# 9. PATH

`PATH` contains directories where Bash searches for executable commands.

Check it:

```bash
echo $PATH
```

Example:

```text
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:...
```

Bash searches these directories when an executable command is entered.

Conceptually:

```text
python3
   |
   v
Search PATH
   |
   +--> /usr/local/bin
   |
   +--> /usr/bin
          |
          +--> python3 found
```

---

# 10. Breaking PATH Experiment

I temporarily changed:

```bash
PATH=/tmp
```

Then:

```bash
ls
```

failed because `/bin` and `/usr/bin` were no longer in `PATH`.

Bash reported that `/bin:/usr/bin` were not included in `PATH`.

However, this still worked:

```bash
/usr/bin/ls
```

Why?

Because `/usr/bin/ls` is an absolute path.

The command no longer needs `PATH` to locate it.

This demonstrated the difference between:

```bash
ls
```

and:

```bash
/usr/bin/ls
```

---

# 11. Restoring PATH

I demonstrated that PATH can be modified:

```bash
PATH=/usr/bin:$PATH
```

This puts `/usr/bin` at the beginning of the existing PATH.

Important lesson:

```bash
PATH=/usr/bin
```

replaces the entire PATH.

Whereas:

```bash
PATH=/usr/bin:$PATH
```

keeps the previous PATH and adds `/usr/bin` in front.

---

# 12. `which`

`which` can show the executable found for a command.

Examples:

```bash
which ls
which python3
which ssh
```

Example:

```text
/usr/bin/ls
/usr/bin/python3
/usr/bin/ssh
```

For more detailed Bash command resolution, `type` and `command -v` are often more useful.

---

# 13. `type`

`type` tells Bash what kind of command something is.

Example:

```bash
type ls
```

My system reported:

```text
ls is aliased to `ls --color=auto'
```

For `ll`:

```bash
type ll
```

Output:

```text
ll is aliased to `ls -la'
```

For `cd`:

```bash
type cd
```

Output:

```text
cd is a shell builtin
```

This shows that not every command is an executable file.

---

# 14. Shell Builtins

Some commands are implemented directly inside Bash.

Example:

```bash
cd
```

is a shell builtin.

This is important because `cd` changes the current shell's working directory.

If `cd` were only an ordinary external program, it would run in a separate process and could not change the parent Bash shell's directory.

---

# 15. External Commands

`python3` is an external executable.

Example:

```bash
type -a python3
```

Output:

```text
python3 is /usr/bin/python3
python3 is /bin/python3
```

The executable is found through `PATH`.

---

# 16. `type -a`

`type -a` shows all known resolutions for a command.

Example:

```bash
type -a ls
```

Output:

```text
ls is aliased to `ls --color=auto'
ls is /usr/bin/ls
ls is /bin/ls
```

For:

```bash
type -a cd
```

Output:

```text
cd is a shell builtin
```

For:

```bash
type -a python3
```

Output:

```text
python3 is /usr/bin/python3
python3 is /bin/python3
```

---

# 17. `command -v`

Another useful command-resolution tool is:

```bash
command -v COMMAND
```

Examples:

```bash
command -v ls
command -v cd
command -v python3
command -v ll
```

My results:

```text
alias ls='ls --color=auto'
cd
/usr/bin/python3
alias ll='ls -la'
```

`command -v` is useful when troubleshooting:

> "What will Bash use when I type this command?"

---

# 18. Bash Functions

A Bash function allows us to create our own commands.

Basic syntax:

```bash
function_name() {
    command
}
```

Example:

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

# 19. Functions vs Aliases

Alias:

```bash
alias ll='ls -la'
```

An alias is mainly a shortcut.

Function:

```bash
system_info() {
    echo "User: $USER"
    echo "Hostname: $HOSTNAME"
    echo "Shell: $SHELL"
}
```

A function can contain multiple commands and logic.

Concept:

```text
Alias
  ↓
Shortcut

Function
  ↓
Commands + logic
```

Functions are therefore much more useful for automation.

---

# 20. Practical `system_info` Function

I created:

```bash
system_info() {
    echo "User: $USER"
    echo "Hostname: $HOSTNAME"
    echo "Shell: $SHELL"
    echo "Home: $HOME"
    echo "Current directory: $PWD"
}
```

Running:

```bash
system_info
```

produced information about the current environment.

This combined previous concepts such as:

- variables
- environment variables
- functions

---

# 21. Function Arguments

Functions can accept arguments.

Example:

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
$1 = first argument
```

The command:

```bash
hello Pri
```

can be visualized as:

```text
hello Pri
     |
     +---- $1
```

---

# 22. Multiple Arguments

Bash provides positional parameters:

```text
$1    first argument
$2    second argument
$3    third argument
...
```

Example:

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

Without quotes:

```bash
user_info Pri Cloud Engineer
```

Bash sees:

```text
$1 = Pri
$2 = Cloud
$3 = Engineer
```

With quotes:

```bash
user_info Pri "Cloud Engineer"
```

Bash sees:

```text
$1 = Pri
$2 = Cloud Engineer
```

---

# 23. `$#` — Number of Arguments

`$#` contains the number of arguments passed to a function.

Example:

```bash
show_args() {
    echo "Number of arguments: $#"
}
```

Running:

```bash
show_args Pri DevOps Linux Docker
```

produces:

```text
Number of arguments: 4
```

---

# 24. `$@` — All Arguments

`$@` represents all positional arguments.

Example:

```bash
show_args() {
    echo "Number of arguments: $#"
    echo "Arguments: $@"
}
```

Running:

```bash
show_args Pri DevOps Linux Docker
```

produced:

```text
Number of arguments: 4
Arguments: Pri DevOps Linux Docker
```

This is useful for scripts that need to process multiple items.

For example:

```bash
./deploy.sh server1 server2 server3
```

A script can use:

```bash
$#
```

to know how many servers were provided and:

```bash
$@
```

to access all of them.

---

# 25. Argument Validation

A good automation script should validate its input.

Our original function:

```bash
hello() {
    echo "Hello, $1!"
}
```

had a problem.

If we ran:

```bash
hello
```

we got:

```text
Hello, !
```

That isn't useful.

We improved it:

```bash
hello() {
    if [ $# -eq 0 ]; then
        echo "Error: Please provide your name."
        return 1
    fi

    echo "Hello, $1!"
}
```

Now:

```bash
hello
```

produces:

```text
Error: Please provide your name.
```

while:

```bash
hello Pri
```

produces:

```text
Hello, Pri!
```

---

# 26. `if`

The condition:

```bash
[ $# -eq 0 ]
```

means:

> Is the number of arguments equal to zero?

Here:

```text
$#      → number of arguments
-eq     → equal to
0       → zero
```

So:

```bash
[ $# -eq 0 ]
```

checks whether no arguments were supplied.

---

# 27. `return`

Inside a Bash function:

```bash
return 1
```

ends the function and reports a failure status.

Common convention:

```text
0       → success
non-zero → failure
```

So:

```bash
return 1
```

means the function failed.

---

# 28. `$?` — Last Exit Status

`$?` contains the exit status of the immediately previous command.

Example:

```bash
hello
echo $?
```

When no argument is supplied:

```text
Error: Please provide your name.
1
```

because the function executed:

```bash
return 1
```

When a valid argument is supplied:

```bash
hello Pri
echo $?
```

the result is:

```text
Hello, Pri!
0
```

because the function completed successfully.

Important:

`$?` only refers to the **immediately previous command**.

For example:

```bash
hello
hello Pri
echo $?
```

will show the status of:

```bash
hello Pri
```

not the first `hello`.

---

# 29. DevOps Importance

These Bash concepts are foundational for automation.

A typical automation flow can look like:

```text
Bash script
    |
    ├── receive arguments
    |
    ├── validate input
    |
    ├── run commands
    |
    ├── check exit status
    |
    └── report success/failure
```

For example, a CI/CD system might execute:

```bash
./deploy.sh production
```

and use the exit code:

```text
0       → deployment succeeded
non-zero → deployment failed
```

This allows automation systems to decide whether to continue or stop.

---

# 30. Commands Practiced

```bash
echo $USER
echo $HOME
echo $SHELL
echo $PATH
echo $PWD
printenv

export NAME="Pri"
bash
echo $NAME

ls -la ~/.bashrc
head -20 ~/.bashrc
source ~/.bashrc

alias ll='ls -la'
type ls
type ll
type cd

echo $PATH
which ls
which python3

type -a ls
type -a cd
type -a python3

command -v ls
command -v cd
command -v python3
command -v ll

hello() {
    echo "Hello, $1!"
}

system_info() {
    echo "User: $USER"
    echo "Hostname: $HOSTNAME"
    echo "Shell: $SHELL"
    echo "Home: $HOME"
    echo "Current directory: $PWD"
}

show_args() {
    echo "Number of arguments: $#"
    echo "Arguments: $@"
}

echo $?
```

---

# 31. Key Lessons

### Environment variables

```text
Variables available to child processes.
```

### `.bashrc`

```text
Bash configuration file used for interactive shell customization.
```

### `source`

```text
Execute configuration in the current shell.
```

### Alias

```text
Shortcut for a command.
```

### PATH

```text
Directories searched for executable commands.
```

### Builtin

```text
Command implemented inside Bash.
```

### Function

```text
Reusable block of Bash commands.
```

### `$1`, `$2`, ...

```text
Function positional arguments.
```

### `$#`

```text
Number of arguments.
```

### `$@`

```text
All arguments.
```

### `$?`

```text
Exit status of the previous command.
```

### Exit code

```text
0       → success
non-zero → failure
```

---

# 32. Mistakes and Debugging Lessons

## Mistake 1 — `command-v`

I accidentally used:

```bash
command-v python3
```

instead of:

```bash
command -v python3
```

The space matters.

---

## Mistake 2 — Function name typo

I created:

```bash
user_info
```

but later typed:

```bash
use_info
```

Bash correctly reported:

```text
Command 'use_info' not found
```

Lesson:

> Check spelling before assuming the system is broken.

---

## Mistake 3 — Checking `$?` too late

I ran a failed function, then another successful function, and only afterward ran:

```bash
echo $?
```

The result was `0`.

Why?

Because `$?` always represents the immediately previous command.

Correct:

```bash
hello
echo $?
```

---

# 33. DevOps Connection

These concepts will appear repeatedly later in the roadmap:

```text
Linux
  │
  ├── Bash
  │    ├── variables
  │    ├── functions
  │    ├── conditions
  │    └── exit codes
  │
  ├── Docker
  │
  ├── CI/CD
  │
  ├── AWS automation
  │
  └── Infrastructure scripts
```

Understanding Bash now will make later DevOps automation much easier.

---

# Lesson Status

Completed:

- [x] Environment variables
- [x] `export`
- [x] Child shells
- [x] `.bashrc`
- [x] `source`
- [x] Aliases
- [x] PATH
- [x] Command lookup
- [x] `type`
- [x] `command -v`
- [x] Bash functions
- [x] Function arguments
- [x] `$#`
- [x] `$@`
- [x] Argument validation
- [x] `return`
- [x] Exit codes
- [x] `$?`

Next:

- Bash automation
- More practical scripting
- Script execution
- Conditions and logic
- Loops
- Error handling
