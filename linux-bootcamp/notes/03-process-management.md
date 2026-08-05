# Linux Notes 03 - Process Management

> Topic completed on: 2026-08-06

---

# Objective

Learn how Linux manages processes, monitor them, control them, and understand job control.

---

# Commands Learned

## View Processes

```bash
ps
ps -e
```

Shows currently running processes.

---

## Find Processes

```bash
pgrep python3
pgrep -l brave
pidof bash
```

Used to find a process by name.

---

## Monitor Processes

```bash
top
htop
```

Shows CPU, RAM and running processes in real time.

Exit:

```text
q
```

---

## Kill Processes

```bash
kill PID
kill -9 PID
pkill process_name
killall process_name
```

---

## Background Jobs

Start in background:

```bash
sleep 300 &
```

View jobs:

```bash
jobs
```

Pause:

Ctrl + Z

Resume in background:

```bash
bg
```

Bring back:

```bash
fg
```

---

## Long Running Process

```bash
nohup sleep 300 &
```

Output goes to

```text
nohup.out
```

---

# Labs Completed

## Lab 1 - Find Python

```bash
which python
which python3
```

Observation

- python not installed as command
- python3 exists

---

## Lab 2 - Locate Database

Created

```bash
touch linux-bootcamp/labs/test-locate.txt
```

Initially

```bash
locate test-locate.txt
```

returned nothing.

Reason:

locate searches its database.

Solution:

```bash
sudo updatedb
```

Then

```bash
locate test-locate.txt
```

found the file.

---

## Lab 3 - File Information

Commands

```bash
file story.txt
stat story.txt
```

Learned

- file identifies type
- stat shows metadata

---

## Lab 4 - Count File Contents

```bash
wc
wc -l
wc -w
wc -c
```

Used to count lines, words and bytes.

---

## Lab 5 - Sorting

```bash
sort
sort -r
sort -u
```

---

## Lab 6 - Remove Duplicates

```bash
uniq
sort | uniq
sort | uniq -c
```

Important:

uniq removes only adjacent duplicates.

---

## Lab 7 - Extract Columns

```bash
cut -d',' -f1
cut -d',' -f2
cut -d',' -f3
```

Learned

Delimiter separates fields.

---

## Lab 8 - Character Translation

```bash
tr
```

Examples

Uppercase

```bash
echo "linux" | tr 'a-z' 'A-Z'
```

Delete

```bash
echo "banana" | tr -d 'a'
```

---

## Lab 9 - find + xargs

```bash
find linux-bootcamp/labs -name "*.txt"
```

Combined with

```bash
xargs ls -l
```

and

```bash
xargs wc -l
```

---

## Lab 10 - Process Discovery

Commands

```bash
ps
pgrep
pidof
top
htop
```

Learned

Every running program has a PID.

---

## Lab 11 - Killing Processes

Created

```bash
sleep 300
```

Killed using

```bash
kill PID
```

Verified using

```bash
pgrep sleep
```

---

## Lab 12 - Job Control

Started

```bash
sleep 300
```

Paused

Ctrl + Z

Output

```text
[1]+ Stopped sleep 300
```

Background

```bash
bg
```

Foreground

```bash
fg
```

Stopped permanently

Ctrl + C

---

## Lab 13 - nohup

Command

```bash
nohup sleep 300 &
```

Output

```text
nohup: ignoring input and appending output to 'nohup.out'
```

Learned

Program continues even after terminal disconnects.

---

# Mistakes I Actually Made

### Mistake

```bash
git add.
```

Correct

```bash
git add .
```

---

### Mistake

```bash
touch-bootcamp/labs/test-locate.txt
```

Correct

```bash
touch linux-bootcamp/labs/test-locate.txt
```

---

### Mistake

Expected

```bash
pgrep python
```

Reality

No output.

Reason

Python process was named

```text
python3
```

---

### Mistake

Ran

```bash
ps -9 PID
```

Wanted

```bash
kill -9 PID
```

Learned

`ps` displays processes.

`kill` sends signals.

---

# DevOps Usage

These commands are used for

- Monitoring servers
- Killing stuck applications
- Running deployments
- Background jobs
- Automation
- Production debugging

---

# Quick Revision

| Command | Purpose |
|----------|---------|
| ps | View processes |
| pgrep | Search process |
| pidof | PID by program |
| top | Live monitor |
| htop | Interactive monitor |
| kill | Stop process |
| kill -9 | Force stop |
| pkill | Kill by name |
| killall | Kill all matching |
| jobs | Show shell jobs |
| bg | Background |
| fg | Foreground |
| nohup | Survive logout |

---

# Key Takeaways

- Every running program is a process.
- Every process has a PID.
- Jobs are managed by the shell.
- Processes are managed by the kernel.
- `nohup` is useful when working on remote servers.
