# Linux Notes 01 - Linux Fundamentals

> Topic: Linux Fundamentals  
> Purpose: Build the foundation needed before Linux administration, Bash scripting, cloud, and DevOps.

---

## 1. What Is Linux?

Linux is an operating-system family built around the **Linux kernel**.

A simple model:

```text
Computer
   |
   +-- Hardware
   |
   +-- Linux Kernel
   |
   +-- System libraries/tools
   |
   +-- Shell
   |
   +-- Applications
```

The **kernel** is the core part that manages CPU, memory, devices, processes, networking, and other system resources.

A **Linux distribution** combines the Linux kernel with system tools, libraries, package management, and applications.

Examples include Ubuntu, Debian, Fedora, Arch Linux, and Zorin OS.

---

## 2. Terminal and Shell

The **terminal** is the application/window where commands are entered.

The **shell** interprets those commands. The shell used throughout this journey is Bash.

```text
Terminal
   |
   v
 Bash
   |
   v
Commands
   |
   v
Linux system
```

Check the current shell:

```bash
echo $SHELL
```

Typical output:

```text
/bin/bash
```

---

## 3. Basic Command Structure

A common command structure is:

```bash
command options arguments
```

Example:

```bash
ls -l /home
```

- `ls` = command
- `-l` = option
- `/home` = argument

Not every command needs all three.

```bash
pwd
```

is already a complete command.

---

## 4. Current Directory

Linux always has a current working directory.

Check it:

```bash
pwd
```

`pwd` means **print working directory**.

Example:

```text
/home/pri
```

---

## 5. Listing Files

```bash
ls
```

Detailed listing:

```bash
ls -l
```

Human-readable sizes:

```bash
ls -lh
```

Include hidden files:

```bash
ls -la
```

A commonly useful combination:

```bash
ls -lah
```

---

## 6. Linux Filesystem

Linux uses one hierarchical filesystem whose top is:

```text
/
```

Simplified structure:

```text
/
├── bin
├── boot
├── dev
├── etc
├── home
│   └── pri
├── lib
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── sbin
├── tmp
├── usr
└── var
```

Important directories:

| Directory | Purpose |
|---|---|
| `/` | Filesystem root |
| `/home` | Normal users' home directories |
| `/root` | Root user's home |
| `/etc` | System configuration |
| `/var` | Variable data, especially logs |
| `/tmp` | Temporary files |
| `/usr` | User-space programs and libraries |
| `/dev` | Device files |
| `/proc` | Kernel/process information |
| `/run` | Runtime system information |

---

## 7. Paths

An **absolute path** starts from `/`.

```text
/home/pri/Documents
```

A **relative path** starts from the current directory.

```text
Documents
```

Important symbols:

```text
.   current directory
..  parent directory
~   current user's home
/   filesystem root
```

---

## 8. Changing Directories

```bash
cd Documents
```

Parent directory:

```bash
cd ..
```

Home directory:

```bash
cd ~
```

Filesystem root:

```bash
cd /
```

Previous directory:

```bash
cd -
```

---

## 9. Creating Directories

```bash
mkdir test
```

Nested directories:

```bash
mkdir -p project/src/scripts
```

`-p` creates missing parent directories.

---

## 10. Creating Files

```bash
touch notes.txt
```

Multiple files:

```bash
touch one.txt two.txt three.txt
```

---

## 11. Reading Files

```bash
cat notes.txt
```

For larger files:

```bash
less notes.txt
```

Exit `less` with:

```text
q
```

---

## 12. Writing and Appending

Print text:

```bash
echo "Hello Linux"
```

Write to a file:

```bash
echo "Hello Linux" > hello.txt
```

`>` redirects output and **overwrites** the destination.

Append:

```bash
echo "Another line" >> hello.txt
```

`>>` adds to the end.

---

## 13. Copying

Copy a file:

```bash
cp hello.txt backup.txt
```

Copy a directory recursively:

```bash
cp -r project project-backup
```

---

## 14. Moving and Renaming

Move:

```bash
mv file.txt Documents/
```

Rename:

```bash
mv old.txt new.txt
```

Linux uses the same `mv` command for both.

---

## 15. Removing

Remove a file:

```bash
rm file.txt
```

Remove an empty directory:

```bash
rmdir directory
```

Remove a directory recursively:

```bash
rm -r directory
```

Be extremely careful with:

```bash
rm -rf
```

because it can recursively and forcefully delete data.

---

## 16. Hidden Files

A filename beginning with `.` is hidden.

Examples:

```text
.bashrc
.profile
.gitconfig
```

Show hidden files:

```bash
ls -la
```

---

## 17. Help and Documentation

Built-in help:

```bash
ls --help
```

Manual:

```bash
man ls
```

Locate an executable:

```bash
which ls
```

---

## 18. Environment Variables

Current user:

```bash
echo $USER
```

Home directory:

```bash
echo $HOME
```

Shell:

```bash
echo $SHELL
```

Current directory:

```bash
echo $PWD
```

Hostname:

```bash
echo $HOSTNAME
```

View environment variables:

```bash
env
```

---

## 19. User Identity

```bash
whoami
```

Detailed identity:

```bash
id
```

These become important when learning permissions, users, groups, SSH, and administration.

---

## 20. System Information

Hostname:

```bash
hostname
```

Kernel information:

```bash
uname -a
```

Distribution information:

```bash
cat /etc/os-release
```

---

## 21. Command History

```bash
history
```

Interactive history search:

```text
Ctrl + R
```

---

## 22. Exit Status

Every command returns an exit status.

```bash
echo $?
```

Convention:

```text
0      success
non-0  failure/error
```

Example:

```bash
true
echo $?
```

Output:

```text
0
```

Example:

```bash
false
echo $?
```

Output:

```text
1
```

Exit codes are extremely important in Bash scripting and CI/CD.

---

## 23. Standard Streams

Linux programs normally have three standard streams:

```text
0 = stdin
1 = stdout
2 = stderr
```

Conceptually:

```text
Keyboard ---> stdin ---> Program ---> stdout ---> Terminal
                              |
                              +----> stderr ---> Terminal
```

---

## 24. Pipes

The pipe sends one command's output to another command:

```bash
ls | wc -l
```

Flow:

```text
ls
 |
 v
wc -l
```

A common troubleshooting pattern:

```bash
ps aux | grep ssh
```

---

## 25. Command Chaining

Run the second command only after success:

```bash
command1 && command2
```

Example:

```bash
mkdir project && cd project
```

Run the second command when the first fails:

```bash
command1 || command2
```

Example:

```bash
cd missing || echo "Directory not found"
```

Run sequentially regardless of status:

```bash
command1 ; command2
```

---

## 26. Why This Matters for DevOps

Linux is underneath many DevOps environments:

- AWS EC2
- Docker containers
- Kubernetes nodes
- SSH servers
- CI/CD runners
- Jenkins agents
- Web servers
- Monitoring systems
- Automation systems

A DevOps engineer should be comfortable working from the terminal.

---

## Quick Revision

| Command | Purpose |
|---|---|
| `pwd` | Current directory |
| `ls` | List files |
| `cd` | Change directory |
| `mkdir` | Create directory |
| `touch` | Create file |
| `cat` | Display file |
| `less` | Read large file |
| `cp` | Copy |
| `mv` | Move/rename |
| `rm` | Remove |
| `echo` | Print text |
| `which` | Locate executable |
| `man` | Manual |
| `whoami` | Current user |
| `id` | User/group information |
| `hostname` | Hostname |
| `uname` | Kernel information |
| `history` | Command history |
| `env` | Environment variables |

---

## Key Takeaways

- Linux is built around the Linux kernel.
- Bash interprets shell commands.
- `/` is the filesystem root.
- `~` represents the current user's home.
- Absolute paths start from `/`.
- Relative paths start from the current directory.
- `pwd` tells you where you are.
- `ls` shows what is there.
- `cd` moves you around.
- `mkdir` creates directories.
- `touch` creates files.
- `cp` copies.
- `mv` moves or renames.
- `rm` removes.
- `>` overwrites.
- `>>` appends.
- `|` connects commands.
- `$?` contains the previous command's exit status.
- Exit status `0` conventionally means success.
