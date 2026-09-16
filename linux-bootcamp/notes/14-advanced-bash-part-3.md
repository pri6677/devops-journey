```markdown
# Advanced Bash – Part 3

## Linux for Cloud & DevOps

---

# 1. Standard Input, Output and Error

Linux programs communicate using three standard streams.

| File Descriptor | Name | Meaning |
|---|---|---|
| `0` | stdin | Standard input |
| `1` | stdout | Standard output |
| `2` | stderr | Standard error |

### Simple example

```bash
echo "Hello"
```

The output goes to:

```text
stdout
```

If a command produces an error:

```bash
ls /does-not-exist
```

The error goes to:

```text
stderr
```

---

# 2. Output Redirection

## `>`

Redirect stdout to a file.

```bash
echo "Hello" > output.txt
```

This creates `output.txt`.

If the file already exists, its contents are **overwritten**.

### Example

```bash
echo "Server started" > server.log
```

---

# 3. Append Output

## `>>`

Append stdout to the end of a file.

```bash
echo "Server started" >> server.log
```

Unlike `>`:

```text
>   overwrite
>>  append
```

This is very useful for logs.

---

# 4. Redirect Errors

## `2>`

The number `2` represents stderr.

```bash
ls /wrong-path 2> error.log
```

The error is written into:

```text
error.log
```

Normal output is still displayed normally.

---

# 5. Append Errors

## `2>>`

Append errors instead of overwriting.

```bash
ls /wrong-path 2>> error.log
```

---

# 6. Redirect stdout and stderr Separately

```bash
command > output.log 2> error.log
```

Example:

```bash
ls /etc /wrong-path > output.log 2> error.log
```

Now:

```text
output.log → normal output
error.log  → errors
```

This is useful in automation because successful output and errors can be investigated separately.

---

# 7. Redirect stderr to stdout

## `2>&1`

This means:

```text
Send stderr to the same place as stdout.
```

Example:

```bash
command > output.log 2>&1
```

Both stdout and stderr go into:

```text
output.log
```

### Important

The order matters.

Correct:

```bash
command > output.log 2>&1
```

This means:

1. stdout → `output.log`
2. stderr → wherever stdout currently goes → `output.log`

---

# 8. `&>` Shortcut

Bash provides:

```bash
&>
```

to redirect both stdout and stderr.

Example:

```bash
command &> output.log
```

Equivalent to:

```bash
command > output.log 2>&1
```

---

# 9. `/dev/null`

`/dev/null` is like a Linux **black hole**.

Anything sent there is discarded.

Example:

```bash
echo "hello" > /dev/null
```

Nothing is displayed.

You can also discard errors:

```bash
command 2> /dev/null
```

Discard everything:

```bash
command &> /dev/null
```

### DevOps example

Sometimes a script only cares whether a command succeeds:

```bash
systemctl is-active --quiet ssh
```

The `--quiet` option suppresses normal output.

---

# 10. The `tee` Command

Normally:

```bash
command > file.txt
```

sends output to the file.

But sometimes we want:

```text
terminal + file
```

This is where `tee` is useful.

```bash
command | tee file.txt
```

The output is:

```text
command
   |
   v
 tee
 / \
v   v
terminal  file
```

Example:

```bash
df -h | tee disk.log
```

You can see the disk information on the terminal **and** save it into:

```text
disk.log
```

---

# 11. Append with `tee`

Normal:

```bash
command | tee file.txt
```

Overwrites the file.

Append:

```bash
command | tee -a file.txt
```

The `-a` means:

```text
append
```

Example:

```bash
free -h | tee -a system.log
```

This is very useful for system-health scripts.

---

# 12. Signals

Linux processes can receive signals.

A signal is a message sent to a process asking it to perform an action.

Common signals:

| Signal | Number | Meaning |
|---|---:|---|
| `SIGINT` | 2 | Interrupt |
| `SIGTERM` | 15 | Ask process to terminate |
| `SIGKILL` | 9 | Force kill |
| `SIGHUP` | 1 | Hangup |
| `SIGQUIT` | 3 | Quit |

---

# 13. SIGINT

When you press:

```text
Ctrl + C
```

the terminal normally sends:

```text
SIGINT
```

to the running process.

Example:

```bash
sleep 100
```

Press:

```text
Ctrl + C
```

The process stops.

---

# 14. SIGTERM

`SIGTERM` politely asks a process to terminate.

Example:

```bash
kill -TERM PID
```

or:

```bash
kill PID
```

By default, `kill PID` sends `SIGTERM`.

A program can catch SIGTERM and perform cleanup.

---

# 15. SIGKILL

```bash
kill -9 PID
```

sends:

```text
SIGKILL
```

SIGKILL immediately terminates the process.

The process cannot catch or ignore SIGKILL.

### Important

Do not use `kill -9` as the first choice.

Normally try:

```bash
kill PID
```

first.

Use:

```bash
kill -9 PID
```

when a process refuses to terminate normally.

---

# 16. The `trap` Command

`trap` allows a Bash script to react when it receives a signal or exits.

Basic syntax:

```bash
trap 'commands' SIGNAL
```

Example:

```bash
trap 'echo "Interrupted!"' INT
```

Now when the script receives `SIGINT`:

```text
Interrupted!
```

is printed.

---

# 17. Cleanup with `trap`

A very useful pattern is:

```bash
trap cleanup EXIT
```

This tells Bash:

```text
When the script exits, run cleanup.
```

Example:

```bash
cleanup() {
    echo "Cleaning temporary files..."
}

trap cleanup EXIT
```

This is useful because cleanup happens even when the script finishes normally.

---

# 18. Temporary Files with `mktemp`

Temporary files are often needed by automation scripts.

Instead of manually choosing a filename:

```bash
temp.txt
```

use:

```bash
mktemp
```

Example:

```bash
TEMP_FILE=$(mktemp)
```

Now Bash stores the generated temporary filename in:

```text
$TEMP_FILE
```

Example:

```bash
echo "temporary data" > "$TEMP_FILE"
cat "$TEMP_FILE"
```

---

# 19. Temporary Directories

Use:

```bash
mktemp -d
```

Example:

```bash
TEMP_DIR=$(mktemp -d)
```

Now `$TEMP_DIR` contains a newly created temporary directory.

---

# 20. Cleanup Temporary Files

Example:

```bash
TEMP_FILE=$(mktemp)

cleanup() {
    rm -f "$TEMP_FILE"
}

trap cleanup EXIT
```

When the script exits:

```text
temporary file → deleted
```

This prevents temporary files from being left behind.

---

# 21. Logging in Bash

Automation scripts should often create logs.

A useful pattern is a logging function.

```bash
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}
```

Now:

```bash
log "Server check started"
```

could produce:

```text
[2026-08-01 10:30:15] Server check started
```

---

# 22. Why Timestamps Matter

Compare:

```text
Server started
Disk checked
Backup completed
```

with:

```text
[2026-08-01 10:30:15] Server started
[2026-08-01 10:30:18] Disk checked
[2026-08-01 10:30:21] Backup completed
```

Timestamps make troubleshooting much easier.

---

# 23. Functions and Return Values

A Bash function can return a status code.

Example:

```bash
check_server() {
    return 0
}
```

Then:

```bash
check_server

echo $?
```

Output:

```text
0
```

Remember:

```text
0 → success
non-zero → failure
```

---

# 24. Returning Data from Functions

Bash functions normally return an exit status.

If you want to produce data, use:

```bash
echo
```

Example:

```bash
get_hostname() {
    hostname
}

SERVER=$(get_hostname)

echo "$SERVER"
```

Here:

```text
hostname
   ↓
function
   ↓
echo/output
   ↓
SERVER variable
```

---

# 25. Argument Validation

A reliable script should validate its arguments.

`$#` tells us how many positional arguments were supplied.

Example:

```bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <server-name>"
    exit 1
fi
```

Meaning:

```text
$#       → number of arguments
-ne      → not equal
1        → expected number
$0       → script name
exit 1   → failure
```

---

# 26. Checking an Argument's Value

Example:

```bash
if [ "$1" != "production" ]; then
    echo "Only production is allowed"
    exit 1
fi
```

This checks whether the first argument is exactly:

```text
production
```

---

# 27. Combining Argument Validation

Example:

```bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

if [ "$1" != "production" ]; then
    echo "Invalid environment"
    exit 1
fi
```

This is safer than assuming the user will always provide correct input.

---

# 28. Mini Project – `server-health.sh`

We combine the concepts learned in Advanced Bash Part 3.

The script will:

- use strict Bash mode
- create a log
- use timestamps
- use `trap`
- create a temporary file
- validate arguments
- check hostname
- check current user
- check disk usage
- check memory
- display and save output

---

# 29. Complete Script

```bash
#!/bin/bash

set -euo pipefail

LOG_FILE="server-health.log"
TEMP_FILE=$(mktemp)

cleanup() {
    rm -f "$TEMP_FILE"
    echo "Cleanup completed."
}

trap cleanup EXIT

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

ENVIRONMENT="$1"

if [ "$ENVIRONMENT" != "production" ] && \
   [ "$ENVIRONMENT" != "staging" ] && \
   [ "$ENVIRONMENT" != "development" ]; then
    echo "Invalid environment."
    exit 1
fi

log "Server health check started."
log "Environment: $ENVIRONMENT"

log "Hostname: $(hostname)"
log "Current user: $(whoami)"

log "Disk usage:"
df -h / | tee -a "$LOG_FILE"

log "Memory usage:"
free -h | tee -a "$LOG_FILE"

log "Server health check completed."
```

---

# 30. Understanding the Project

## Strict mode

```bash
set -euo pipefail
```

Makes the script safer.

It enables:

```text
-e → stop on errors
-u → detect unset variables
pipefail → detect failures inside pipelines
```

---

## Temporary file

```bash
TEMP_FILE=$(mktemp)
```

Creates a temporary file.

---

## Cleanup

```bash
cleanup() {
    rm -f "$TEMP_FILE"
}
```

Deletes the temporary file.

---

## EXIT trap

```bash
trap cleanup EXIT
```

Runs cleanup when the script exits.

---

## Logging

```bash
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}
```

This:

1. creates a timestamp
2. adds the message
3. displays it
4. appends it to the log

---

## Argument count

```bash
if [ "$#" -ne 1 ]; then
```

Requires exactly one argument.

Example:

```bash
./server-health.sh production
```

---

# 31. Running the Project

Make it executable:

```bash
chmod +x server-health.sh
```

Run:

```bash
./server-health.sh production
```

Possible output:

```text
[2026-08-01 10:30:15] Server health check started.
[2026-08-01 10:30:15] Environment: production
[2026-08-01 10:30:15] Hostname: smarty
[2026-08-01 10:30:15] Current user: pri
[2026-08-01 10:30:15] Disk usage:
Filesystem      Size  Used Avail Use% Mounted on
/dev/...         50G   20G   28G  42% /
[2026-08-01 10:30:16] Memory usage:
               total        used        free
Mem:            ...
[2026-08-01 10:30:16] Server health check completed.
Cleanup completed.
```

Actual disk and memory values will depend on the machine.

---

# 32. Check the Log

After running:

```bash
cat server-health.log
```

You should see the recorded information.

You can also use:

```bash
less server-health.log
```

---

# 33. Test Invalid Arguments

Run:

```bash
./server-health.sh
```

Expected:

```text
Usage: ./server-health.sh <environment>
```

Run:

```bash
./server-health.sh testing
```

Expected:

```text
Invalid environment.
```

Run correctly:

```bash
./server-health.sh production
```

---

# 34. Why This Matters in DevOps

These Bash concepts are directly useful in DevOps.

### Logging

Used for:

```text
deployment logs
server logs
backup logs
monitoring scripts
CI/CD jobs
```

### Exit codes

Used by:

```text
Jenkins
GitHub Actions
GitLab CI
cron jobs
automation systems
```

### `trap`

Used for:

```text
cleanup
temporary files
graceful shutdown
resource management
```

### Redirection

Used for:

```text
saving command output
capturing errors
creating logs
debugging automation
```

### `tee`

Useful when you want:

```text
terminal output + log file
```

### `mktemp`

Useful for:

```text
temporary data
temporary reports
intermediate files
automation
```

---

# 35. Important Commands Cheat Sheet

## Output

```bash
command > file
```

Overwrite stdout.

```bash
command >> file
```

Append stdout.

```bash
command 2> file
```

Overwrite stderr.

```bash
command 2>> file
```

Append stderr.

```bash
command > file 2>&1
```

stdout + stderr.

```bash
command &> file
```

stdout + stderr.

```bash
command > /dev/null
```

Discard stdout.

```bash
command 2> /dev/null
```

Discard stderr.

```bash
command &> /dev/null
```

Discard everything.

---

## `tee`

```bash
command | tee file
```

Display + overwrite file.

```bash
command | tee -a file
```

Display + append file.

---

## Signals

```bash
kill PID
```

Send SIGTERM.

```bash
kill -15 PID
```

Send SIGTERM explicitly.

```bash
kill -9 PID
```

Send SIGKILL.

---

## Trap

```bash
trap 'command' EXIT
```

Run command when script exits.

```bash
trap 'command' INT
```

React to Ctrl+C / SIGINT.

---

## Temporary files

```bash
mktemp
```

Create temporary file.

```bash
mktemp -d
```

Create temporary directory.

---

## Logging

```bash
date '+%Y-%m-%d %H:%M:%S'
```

Create a readable timestamp.

---

# 36. Common Mistakes

## Mistake 1: Using `>` when you wanted append

Wrong:

```bash
echo "new log" > server.log
```

This can overwrite previous logs.

Use:

```bash
echo "new log" >> server.log
```

---

## Mistake 2: Forgetting stderr

This:

```bash
command > output.log
```

does not automatically capture errors.

Use:

```bash
command > output.log 2>&1
```

if you need both.

---

## Mistake 3: Using `kill -9` immediately

Prefer:

```bash
kill PID
```

first.

Then use:

```bash
kill -9 PID
```

if necessary.

---

## Mistake 4: Forgetting cleanup

If a script creates temporary files but never removes them, the system can accumulate unnecessary files.

Use:

```bash
trap cleanup EXIT
```

---

## Mistake 5: Not validating arguments

Do not assume the user will always execute:

```bash
./script.sh correct-input
```

Validate input.

---

# 37. Debugging Checklist

When a Bash automation script fails:

### Step 1 – Check syntax

```bash
bash -n script.sh
```

### Step 2 – Run with tracing

```bash
bash -x script.sh
```

### Step 3 – Check exit status

```bash
echo $?
```

### Step 4 – Check logs

```bash
cat server-health.log
```

### Step 5 – Check permissions

```bash
ls -l script.sh
```

### Step 6 – Check temporary resources

Make sure cleanup is working.

---

# 38. DevOps Mental Model

Think of a Bash automation script like a small DevOps worker:

```text
INPUT
  |
  v
Validate arguments
  |
  v
Run commands
  |
  +-------> stdout
  |
  +-------> stderr
  |
  v
Log results
  |
  v
Handle errors
  |
  v
Cleanup
  |
  v
EXIT STATUS
```

This pattern appears repeatedly in real DevOps automation.

---

# 39. What You Should Remember

The most important ideas from Advanced Bash Part 3 are:

```text
stdin   → 0
stdout  → 1
stderr  → 2
```

```text
>       → overwrite
>>      → append
2>      → stderr
2>&1    → stderr → stdout destination
&>      → stdout + stderr
```

```text
/dev/null → discard output
tee       → display + save output
trap      → react to signals/exits
mktemp    → create temporary resources
```

And:

```text
0     → success
non-0 → failure
```

A robust automation script should:

```text
validate
    ↓
execute
    ↓
log
    ↓
handle errors
    ↓
cleanup
    ↓
return correct exit status
```

---

# 40. Advanced Bash Part 3 Complete

You have now covered:

- Standard input/output/error
- File descriptors
- Output redirection
- Error redirection
- Combined redirection
- `/dev/null`
- `tee`
- Signals
- `trap`
- Cleanup
- Temporary files
- Temporary directories
- Logging
- Function return values
- Argument validation
- Robust Bash automation
- Server health automation project

## Next Linux Topic

# Linux Automation

The next stage will move from writing Bash automation scripts to **automating Linux tasks on a schedule**, including tools such as:

```text
cron
crontab
systemd timers
automated backups
scheduled maintenance
log cleanup
```
``` 

This is the **`14-advanced-bash-part-3.md`** file.