# Disk & Storage Management

## Learning Objectives

- Understand disks, partitions, filesystems, and mount points
- Check disk usage
- Check directory sizes
- View block devices
- Check RAM usage
- View mounted filesystems

---

# 1. df (Disk Free)

Shows filesystem disk usage.

## Commands

```bash
df
df -h
df -h /
df -h ~
```

## Common Options

| Option | Meaning |
|---------|---------|
| -h | Human-readable sizes |

Example:

```bash
df -h
```

---

# 2. Mount Point

A mount point is a directory where a filesystem becomes accessible.

Example:

```
/dev/sda6
     │
     ▼
     /
```

Linux attaches filesystems to directories.

---

# 3. du (Disk Usage)

Shows directory and file sizes.

## Commands

```bash
du
du -h
du -sh linux-bootcamp
```

## Common Options

| Option | Meaning |
|---------|---------|
| -h | Human-readable |
| -s | Summary only |

---

# 4. Storage Units

| Unit | Meaning |
|------|---------|
| B | Byte |
| KB | Kilobyte (1000 Bytes) |
| KiB | Kibibyte (1024 Bytes) |
| MB | Megabyte |
| MiB | Mebibyte |
| GB | Gigabyte |
| GiB | Gibibyte |
| TB | Terabyte |

Linux usually displays KiB, MiB and GiB.

---

# 5. lsblk

Lists block devices.

## Commands

```bash
lsblk
lsblk -f
```

Example:

```
sda
├── sda1
├── sda2
└── sda6
```

Where:

- sda = Physical disk
- sda1, sda2 = Partitions

---

# 6. Filesystems

| Filesystem | Used For |
|------------|----------|
| ext4 | Linux |
| NTFS | Windows |
| FAT32 / vfat | EFI Partition, USB Drives |

---

# 7. UUID

UUID = Universally Unique Identifier

Each filesystem has a unique identifier.

Linux often uses UUIDs instead of device names because device names can change.

---

# 8. free

Shows RAM usage.

## Commands

```bash
free
free -h
```

Important columns:

| Column | Meaning |
|----------|---------|
| total | Total RAM |
| used | Used RAM |
| free | Completely unused RAM |
| buff/cache | RAM used as cache |
| available | RAM available for new programs |

Linux intentionally uses free RAM as cache to improve performance.

---

# 9. Storage vs RAM

Storage:

- Permanent
- SSD/HDD
- Checked using df and du

RAM:

- Temporary
- Running programs
- Checked using free

---

# 10. mount

Shows mounted filesystems.

```bash
mount
mount | head
```

Example:

```
/dev/sda6 on / type ext4
```

Meaning:

```
/dev/sda6
      │
      ▼
      /
```

---

# 11. findmnt

Displays mounted filesystems in a tree structure.

```bash
findmnt
```

Preferred over mount because the output is easier to read.

---

# Interview Questions

Q. Difference between df and du?

- df shows filesystem usage.
- du shows directory usage.

Q. Difference between Storage and RAM?

Storage is permanent.
RAM is temporary working memory.

Q. What is a mount point?

A directory where a filesystem is attached.

Q. What is ext4?

Default Linux filesystem.

Q. Why is available memory more important than free memory?

Because Linux uses unused RAM as cache and can reclaim it instantly.
