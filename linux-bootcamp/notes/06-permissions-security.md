# Linux Permissions & Security

## 1. Users and Groups

Linux uses users and groups to control access to files and system resources.

### Useful command

```bash
whoami
id
groups
groups pri
```

### `groups`

Shows the groups a user belongs to in readable form.

Example:

```bash
groups
```

### `id`

Shows detailed identity information:

```text
uid=1000(pri) gid=1000(pri) groups=1000(pri),4(adm),24(cdrom),27(sudo),...
```

* `uid` → User ID
* `gid` → Primary Group ID
* `groups` → Supplementary groups

---

## 2. `/etc/passwd`

`/etc/passwd` contains information about local user accounts.

Example:

```bash
getent passwd nobody
```

Output:

```text
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

Important fields include:

```text
username : password-placeholder : UID : GID : description : home : shell
```

### System Accounts

Linux also has service/system accounts.

For example:

```bash
getent passwd | grep -E '^(nobody|daemon):'
```

`daemon` is a system account associated with background services.

`nobody` is a low-privilege account used by some services or processes when they should not run with normal user privileges.

---

# 3. `su` vs `sudo`

## `su`

`su` means **switch user**.

```bash
su username
```

If no username is provided, `root` is assumed.

```bash
su
```

`su` authenticates using the target user's password.

## `sudo`

`sudo` allows an authorized user to execute a command with another user's privileges, commonly `root`.

```bash
sudo whoami
```

Output:

```text
root
```

But your current shell does not change:

```bash
whoami
```

still returns:

```text
pri
```

### Important distinction

```text
su
 ↓
switch to another user/session

sudo command
 ↓
run one command with elevated privileges
```

---

# 4. `sudo -l`

Shows what commands the current user is allowed to execute with `sudo`.

```bash
sudo -l
```

On my system:

```text
User pri may run the following commands:
    (ALL : ALL) ALL
```

This means the user is allowed to run commands as other users/groups through `sudo`.

---

# 5. File Ownership

Every file has:

```text
owner
group
```

Example:

```bash
ls -l ownership-test.txt
```

Output:

```text
-rw-rw-r-- 1 pri pri 0 ... ownership-test.txt
```

Here:

```text
owner → pri
group → pri
```

---

# 6. `chown`

`chown` changes ownership.

### Change owner

```bash
sudo chown root file
```

### Change owner and group

```bash
sudo chown root:devops file
```

### Change only group

A useful form is:

```bash
sudo chown :users file
```

Example:

```bash
sudo chown :users ownership-test.txt
```

Result:

```text
-rw-rw-r-- 1 pri users ...
```

---

# 7. `chgrp`

`chgrp` changes the group ownership.

```bash
chgrp pri ownership-test.txt
```

Example:

```text
-rw-rw-r-- 1 pri pri ...
```

### Difference

```text
chown → change owner/group
chgrp → change group
```

---

# 8. Linux Permission Model

A normal file permission looks like:

```text
-rwxr-xr-x
```

The permissions are divided into:

```text
-rwx r-x r-x
    │   │   │
    │   │   └── others
    │   └────── group
    └────────── owner
```

The three basic permissions are:

```text
r = read
w = write
x = execute
```

For files:

* `r` → read file contents
* `w` → modify file contents
* `x` → execute the file

---

# 9. Numeric Permissions

Each permission has a number:

```text
r = 4
w = 2
x = 1
```

Add them together:

```text
7 = rwx
6 = rw-
5 = r-x
4 = r--
3 = -wx
2 = -w-
1 = --x
0 = ---
```

Example:

```bash
chmod 755 app.py
```

Means:

```text
7 → owner  → rwx
5 → group  → r-x
5 → others → r-x
```

Result:

```text
-rwxr-xr-x
```

---

# 10. Symbolic `chmod`

Permissions can also be modified symbolically.

Example:

```bash
chmod o-r app.py
```

Breakdown:

```text
o → others
- → remove
r → read
```

So:

```text
other read permission
        ↓
      removed
```

---

# 11. `stat`

`stat` displays detailed file metadata.

Example:

```bash
stat -c '%A %a %U %G %n' app.py
```

`-c` allows a custom output format.

Useful format specifiers:

```text
%A → permissions in symbolic form
%a → permissions in numeric form
%U → owner username
%G → group name
%n → file name
```

Example:

```text
drwxrwsr-x 2775 pri devops /home/pri/security-challenge/app
```

---

# 12. SUID

SUID is a special permission for executable files.

Example:

```bash
ls -l /usr/bin/passwd
```

Example output:

```text
-rwsr-xr-x 1 root root ... /usr/bin/passwd
```

Notice:

```text
-rws
   ↑
   s
```

Instead of the owner's normal `x`, there is an `s`.

SUID allows the executable to run with the effective privileges of its owner.

---

# 13. SGID

SGID is another special permission.

For directories, SGID causes newly created files to inherit the directory's group.

Example:

```bash
chmod 2775 ~/sgid-lab
```

Breakdown:

```text
2 → SGID
775 → normal permissions
```

Result:

```text
drwxrwsr-x
```

The `s` indicates SGID.

---

# 14. SGID Hands-On Lab

Created:

```bash
mkdir -p ~/sgid-lab
sudo groupadd devops
sudo usermod -aG devops pri
sudo chgrp devops ~/sgid-lab
chmod 2775 ~/sgid-lab
```

After activating the group:

```bash
newgrp devops
```

Created:

```bash
touch ~/sgid-lab/project.txt
```

The resulting file inherited the `devops` group:

```text
-rw-rw-r-- 1 pri devops ... project.txt
```

### Important lesson

SGID on a directory means:

```text
new file
   ↓
inherits directory's group
```

It does **not** mean the new file becomes owned by the directory owner.

---

# 15. Sticky Bit

Sticky Bit is commonly used on shared directories.

Example:

```bash
chmod 1777 /tmp
```

The first digit:

```text
1 → Sticky Bit
```

Result:

```text
drwxrwxrwt
```

Notice:

```text
         t
         ↑
    Sticky Bit
```

The Sticky Bit prevents ordinary users from deleting or renaming files belonging to other users in a shared writable directory.

Example:

```bash
ls -ld /tmp
```

Typical result:

```text
drwxrwxrwt ... /tmp
```

---

# 16. ACL

ACL means **Access Control List**.

ACL allows additional, user-specific or group-specific permissions without changing the basic owner/group/other model.

Useful commands:

```bash
getfacl file
setfacl -m u:username:rw- file
setfacl -b file
```

---

# 17. Creating an ACL User

Created a test user:

```bash
sudo useradd acluser
```

Checked:

```bash
id acluser
```

Added an ACL:

```bash
setfacl -m u:acluser:r-- app.py
```

The ACL showed:

```text
user::rwx
user:acluser:r--
group::r-x
mask::r-x
other::r-x
```

---

# 18. ACL Mask

The ACL mask controls the maximum effective permissions for named users, named groups, and the group entry.

Example:

```bash
setfacl -m u:acluser:rw- app.py
```

Then:

```bash
setfacl -m m:r-- app.py
```

The result included:

```text
user:acluser:rw-    #effective:r--
mask::r--
```

Although `acluser` was assigned `rw-`, the mask restricted the effective permission to:

```text
r--
```

### Important rule

```text
Requested ACL permission
          +
      ACL mask
          ↓
 Effective permission
```

---

# 19. Removing ACLs

To remove extended ACL entries:

```bash
setfacl -b app.py
```

After removing the ACL, the `+` disappeared from `ls -l`.

---

# 20. ACL Indicator

When a file has an extended ACL, `ls -l` can show:

```text
-rwxr-xr-x+
          ↑
       extended ACL
```

The `+` indicates additional ACL information exists.

---

# 21. Security Challenge

Created:

```bash
mkdir -p ~/security-challenge
cd ~/security-challenge
mkdir app logs
touch deploy.sh
```

The final structure:

```text
security-challenge/
├── app/
├── logs/
└── deploy.sh
```

---

## `app/` — Shared DevOps Directory

Configured:

```bash
chmod 2775 ~/security-challenge/app
```

Verified:

```bash
stat -c '%A %a %U %G %n' ~/security-challenge/app
```

Result:

```text
drwxrwsr-x 2775 pri devops ...
```

Created:

```bash
touch ~/security-challenge/app/new-file.txt
```

Result:

```text
-rw-rw-r-- 1 pri devops ... new-file.txt
```

The file inherited the `devops` group.

---

# 22. `deploy.sh` — Protected Deployment Script

Changed ownership:

```bash
sudo chown root:devops ~/security-challenge/deploy.sh
```

Result:

```text
-rw-rw-r-- 1 root devops ... deploy.sh
```

Then changed permissions:

```bash
sudo chmod 755 ~/security-challenge/deploy.sh
```

Final normal permissions:

```text
-rwxr-xr-x 1 root devops ... deploy.sh
```

This means:

```text
root    → rwx
devops  → r-x
others  → r-x
```

An attempt to run `chmod` without `sudo` failed:

```text
Operation not permitted
```

This demonstrated that being in the file's group does not make a user the owner.

---

# 23. ACL on `deploy.sh`

Created:

```bash
sudo useradd tester
```

Added an ACL:

```bash
sudo setfacl -m u:tester:rw- ~/security-challenge/deploy.sh
```

Verified:

```bash
getfacl ~/security-challenge/deploy.sh
```

Result:

```text
user::rwx
user:tester:rw-
group::r-x
mask::rwx
other::r-x
```

The file also showed:

```text
-rwxrwxr-x+
```

The `+` indicates an extended ACL.

The normal owner remained:

```text
root
```

and the group remained:

```text
devops
```

---

# 24. Cleanup

Temporary lab users should be removed when they are no longer needed.

Examples:

```bash
sudo userdel tester
sudo userdel acluser
```

Temporary groups created specifically for a lab can also be removed when appropriate:

```bash
sudo groupdel devops
```

Before deleting a group, verify that it is not needed by other files, users, or services.

---

# 25. Common Mistakes I Encountered

During the lab I encountered several mistakes:

### Wrong filename

```bash
ls -l ownership-test.test
```

when the actual file was:

```text
ownership-test.txt
```

### Wrong command

```bash
cdmod
```

instead of:

```bash
chmod
```

### Incorrect `chmod` syntax

```bash
chmod 0-r app.py
```

Correct symbolic syntax:

```bash
chmod o-r app.py
```

### Missing `sudo`

Trying to modify a root-owned file without sufficient privileges produced:

```text
Operation not permitted
```

The correct approach was:

```bash
sudo chmod ...
sudo setfacl ...
```

### Incorrect filename

```bash
deplooy.sh
```

instead of:

```text
deploy.sh
```

---

# 26. Key Lessons

The most important concepts from this module:

```text
User
  ↓
Group
  ↓
Owner
  ↓
Permissions
  ↓
ACL
  ↓
Special permissions
  ↓
sudo
```

### Ownership

```text
owner + group
```

### Basic permissions

```text
r = 4
w = 2
x = 1
```

### Special permissions

```text
4 = SUID
2 = SGID
1 = Sticky Bit
```

### Common examples

```text
755  → rwxr-xr-x
775  → rwxrwxr-x
1777 → rwxrwxrwx + Sticky Bit
2775 → rwxrwxr-x + SGID
4755 → SUID + 755
```

---

# 27. DevOps Connection

Linux permissions are critical in DevOps because servers contain:

* deployment scripts
* application files
* logs
* configuration files
* SSH keys
* service files
* secrets
* container volumes

Incorrect permissions can cause:

```text
security vulnerabilities
      ↓
unauthorized modification
      ↓
service compromise
```

Correct permissions help enforce:

```text
least privilege
      ↓
controlled access
      ↓
safer infrastructure
```

---

# 28. Module Status

**Linux Permissions & Security — COMPLETE**

Topics practiced:

* [x] Users
* [x] Groups
* [x] `/etc/passwd`
* [x] `id`
* [x] `groups`
* [x] `su`
* [x] `sudo`
* [x] `chown`
* [x] `chgrp`
* [x] `chmod`
* [x] Numeric permissions
* [x] SUID
* [x] SGID
* [x] SGID inheritance
* [x] Sticky Bit
* [x] ACL
* [x] ACL mask
* [x] `getfacl`
* [x] `setfacl`
* [x] `stat`
* [x] Security challenge
* [x] Debugging permission errors

**Next module: Linux Package Management**
