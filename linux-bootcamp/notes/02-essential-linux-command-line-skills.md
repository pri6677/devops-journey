# Linux Notes 02 - Essential Linux Command-Line Skills

> Topic: Essential Linux Commands and Text/File Operations  
> Purpose: Learn the command-line tools used repeatedly in Linux administration and DevOps.

---

## 1. Why Command-Line Tools Matter

Linux administration often means answering questions such as:

- Which files exist?
- Where is a configuration file?
- How many lines are in a log?
- Which logs contain an error?
- Which values are duplicated?
- Which processes are running?
- What information should be extracted from command output?

Linux provides many small tools designed to work together.

A typical workflow can look like:

```text
find -> grep -> sort -> uniq -> wc
```

---

## 2. file

Identify the type of a file:

```bash
file story.txt
```

`file` examines the contents and reports what kind of data it contains.

This is useful when a filename extension cannot be trusted.

---

## 3. stat

Show detailed file metadata:

```bash
stat story.txt
```

Information can include:

- permissions
- owner
- group
- size
- inode
- access time
- modification time
- status-change time

Important timestamps:

```text
atime = access time
mtime = content modification time
ctime = metadata/status change time
```

---

## 4. wc

`wc` can count lines, words, and bytes.

```bash
wc file.txt
```

Lines:

```bash
wc -l file.txt
```

Words:

```bash
wc -w file.txt
```

Bytes:

```bash
wc -c file.txt
```

Example DevOps use:

```bash
wc -l logfile
```

---

## 5. sort

Sort lines:

```bash
sort file.txt
```

Reverse:

```bash
sort -r file.txt
```

Unique sorted output:

```bash
sort -u file.txt
```

---

## 6. uniq

Remove adjacent duplicate lines:

```bash
uniq file.txt
```

Important: `uniq` only detects duplicates next to each other.

Therefore:

```bash
sort file.txt | uniq
```

is a common pattern.

Count duplicates:

```bash
sort file.txt | uniq -c
```

Example output:

```text
2 docker
1 linux
1 python
```

---

## 7. cut

`cut` extracts fields from lines.

Suppose:

```text
Pri,Cloud Engineer,India
Rahul,Developer,India
Aman,DevOps,India
```

First field:

```bash
cut -d',' -f1 file.txt
```

Second field:

```bash
cut -d',' -f2 file.txt
```

Third field:

```bash
cut -d',' -f3 file.txt
```

Meaning:

```text
-d',' = comma is the delimiter
-f1   = first field
-f2   = second field
-f3   = third field
```

---

## 8. tr

`tr` transforms characters.

Lowercase to uppercase:

```bash
echo "linux" | tr 'a-z' 'A-Z'
```

Output:

```text
LINUX
```

Uppercase to lowercase:

```bash
echo "LINUX" | tr 'A-Z' 'a-z'
```

Delete characters:

```bash
echo "banana" | tr -d 'a'
```

Output:

```text
bnn
```

---

## 9. find

Search the filesystem:

```bash
find linux-bootcamp/labs -name "*.txt"
```

Search for files:

```bash
find . -type f
```

Search for directories:

```bash
find . -type d
```

Search for a specific file:

```bash
find . -name "server-check.sh"
```

The important idea is that `find` searches the filesystem itself.

---

## 10. locate and updatedb

`locate` searches a pre-built filename database:

```bash
locate test-locate.txt
```

A newly created file may not appear immediately.

Update the database:

```bash
sudo updatedb
```

Then:

```bash
locate test-locate.txt
```

Main difference:

```text
find
  -> searches the filesystem

locate
  -> searches a filename database
```

---

## 11. xargs

`xargs` converts input into command arguments.

Example:

```bash
find linux-bootcamp/labs -name "*.txt" | xargs ls -l
```

Conceptually:

```text
find
 |
 | filenames
 v
xargs
 |
 | arguments
 v
ls -l
```

Another example:

```bash
find linux-bootcamp/labs -name "*.txt" | xargs wc -l
```

For filenames containing spaces or unusual characters, a safer pattern is:

```bash
find . -type f -print0 | xargs -0 command
```

The `-print0` and `-0` pair preserves filenames safely.

---

## 12. grep

Search text:

```bash
grep "error" logfile.txt
```

Case-insensitive:

```bash
grep -i "error" logfile.txt
```

Show line numbers:

```bash
grep -n "error" logfile.txt
```

Exclude matching lines:

```bash
grep -v "error" logfile.txt
```

Recursive search:

```bash
grep -r "error" directory/
```

Count matching lines:

```bash
grep -c "error" logfile.txt
```

`grep` is one of the most important Linux troubleshooting tools.

---

## 13. Combining Commands

Example:

```bash
ps aux | grep ssh
```

The first command produces process information.

The pipe sends that output into `grep`.

`grep` filters it.

This pattern is central to Linux troubleshooting.

---

## 14. head

Show the beginning of a file:

```bash
head file.txt
```

Show the first five lines:

```bash
head -n 5 file.txt
```

---

## 15. tail

Show the end of a file:

```bash
tail file.txt
```

Show the last twenty lines:

```bash
tail -n 20 file.txt
```

Follow a changing file:

```bash
tail -f /var/log/syslog
```

`tail -f` is extremely useful for watching logs in real time.

Exit with:

```text
Ctrl + C
```

---

## 16. less

Read a large file interactively:

```bash
less file.txt
```

Useful keys:

```text
Space      next page
b          previous page
/word      search
n          next match
q          quit
```

For large logs, `less` is usually better than `cat`.

---

## 17. Redirection

Overwrite:

```bash
command > output.txt
```

Append:

```bash
command >> output.txt
```

Redirect standard error:

```bash
command 2> errors.txt
```

Redirect stdout and stderr:

```bash
command > output.txt 2>&1
```

Bash shorthand:

```bash
command &> output.txt
```

---

## 18. Pipe vs Redirection

Pipe:

```bash
command1 | command2
```

means:

```text
command1 output
       |
       v
command2 input
```

Redirection:

```bash
command > file.txt
```

means:

```text
command output
       |
       v
file.txt
```

They solve different problems.

---

## 19. Standard Streams

Linux normally provides:

```text
0 = stdin
1 = stdout
2 = stderr
```

Example:

```bash
command 2> error.log
```

means:

```text
stderr (2) ---> error.log
```

Understanding these streams becomes essential in Bash scripting and CI/CD.

---

## 20. Wildcards

All `.txt` files:

```bash
*.txt
```

One character:

```bash
file?.txt
```

Character range:

```bash
file[1-3].txt
```

Example:

```bash
ls *.txt
```

The shell expands the pattern before executing the command.

---

## 21. Quoting

Single quotes prevent normal variable expansion:

```bash
echo '$HOME'
```

Output:

```text
$HOME
```

Double quotes allow variable expansion:

```bash
echo "$HOME"
```

Output:

```text
/home/pri
```

This difference becomes very important in Bash scripts.

---

## 22. Command Substitution

Use:

```bash
$(command)
```

Example:

```bash
echo "Current user: $(whoami)"
```

Possible output:

```text
Current user: pri
```

The command is executed first, and its output is inserted into the surrounding command.

---

## 23. Shell Variables

Create a variable:

```bash
name="Pri"
```

Important: do not put spaces around `=`.

Correct:

```bash
name="Pri"
```

Incorrect:

```bash
name = "Pri"
```

Read it:

```bash
echo "$name"
```

---

## 24. Useful Variables

```bash
echo "$USER"
echo "$HOME"
echo "$SHELL"
echo "$PWD"
echo "$HOSTNAME"
```

These provide information about the current environment.

---

## 25. Exit Codes

Every command returns a status.

```bash
echo $?
```

Convention:

```text
0      success
non-0  failure
```

This is how scripts and CI/CD systems can determine whether a command succeeded.

Example:

```bash
mkdir project && echo "Created successfully"
```

The second command runs only if `mkdir` succeeds.

---

## 26. which and type

Locate an executable:

```bash
which python3
```

Identify how Bash interprets a command:

```bash
type cd
```

You may see:

```text
cd is a shell builtin
```

This means `cd` is provided by the shell itself rather than being a normal external executable.

---

## 27. Process Awareness

Running a command usually creates or interacts with a process.

For example:

```bash
python3 script.py
```

Process tools include:

```bash
ps
pgrep python3
kill PID
```

Detailed process management is covered in:

```text
03-process-management.md
```

---

## 28. A Real Linux Troubleshooting Pipeline

Small Linux tools can be chained together:

```text
find
  |
  v
grep
  |
  v
sort
  |
  v
uniq
  |
  v
wc
```

For example:

```bash
find /var/log -type f -name "*.log" 2>/dev/null     | xargs grep -i "error"     | sort     | uniq -c
```

The exact command is not as important as understanding the pattern:

```text
find -> locate data
grep -> filter data
sort -> organize data
uniq -> identify repeated values
wc -> count data
```

---

## 29. DevOps Applications

### Log investigation

```bash
grep -i "error" application.log
tail -f application.log
```

### Finding configuration files

```bash
find /etc -name "*.conf"
```

### Counting events

```bash
grep -c "failed" auth.log
```

### Extracting fields

```bash
cut -d',' -f1 users.csv
```

### Filtering command output

```bash
ps aux | grep nginx
```

These skills are used later in:

- Bash automation
- CI/CD
- Docker troubleshooting
- Kubernetes troubleshooting
- AWS administration
- log analysis
- monitoring
- incident response

---

## 30. Common Mistakes

### Mistake: Confusing find and locate

```text
find   -> filesystem search
locate -> database search
```

### Mistake: Thinking uniq finds all duplicates

```bash
uniq file.txt
```

only handles adjacent duplicates.

Use:

```bash
sort file.txt | uniq
```

### Mistake: Spaces around variable assignment

Wrong:

```bash
name = "Pri"
```

Correct:

```bash
name="Pri"
```

### Mistake: Confusing pipe and redirection

Pipe:

```bash
command1 | command2
```

Redirection:

```bash
command > file
```

### Mistake: Forgetting quotes

Safer:

```bash
echo "$HOME"
```

Quoting is especially important when variables can contain spaces or shell metacharacters.

---

## Command Summary

| Command | Purpose |
|---|---|
| `file` | Identify file type |
| `stat` | Show file metadata |
| `wc` | Count lines/words/bytes |
| `sort` | Sort lines |
| `uniq` | Remove adjacent duplicates |
| `cut` | Extract fields |
| `tr` | Transform/delete characters |
| `find` | Search filesystem |
| `locate` | Search filename database |
| `updatedb` | Update locate database |
| `xargs` | Build command arguments |
| `grep` | Search text |
| `head` | Show beginning |
| `tail` | Show end |
| `tail -f` | Follow changing file |
| `less` | Read large files |
| `which` | Locate executable |
| `type` | Identify command type |

---

## Key Takeaways

1. `file` identifies file type.
2. `stat` shows metadata.
3. `wc` counts data.
4. `sort` orders text.
5. `uniq` removes adjacent duplicates.
6. `sort | uniq` is a common duplicate-removal pattern.
7. `cut` extracts fields.
8. `tr` transforms characters.
9. `find` searches the filesystem.
10. `locate` searches a database.
11. `updatedb` refreshes the locate database.
12. `xargs` turns input into command arguments.
13. `grep` searches text and logs.
14. `head` and `tail` inspect parts of files.
15. `tail -f` follows live log changes.
16. `less` is useful for large files.
17. `>` overwrites.
18. `>>` appends.
19. `2>` redirects errors.
20. `|` connects commands.
21. `$(...)` performs command substitution.
22. Shell variables store values.
23. Quoting controls expansion.
24. Exit codes allow automation to detect success or failure.
25. Combining small commands is one of the most powerful Linux skills.

---

## Foundation Sequence

The Linux notes now follow the chronological learning sequence:

```text
01 Linux Fundamentals
        |
02 Essential Linux Command-Line Skills
        |
03 Process Management
        |
04 Disk & Storage
        |
05 Permissions & Security
        |
06 Package Management
        |
07 Services & systemd
        |
08 Bash Environment & Functions
        |
09 Bash Scripting
        |
10 Linux Administration Part 1
        |
11 Linux Administration Part 2
```
