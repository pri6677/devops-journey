logs = [
    "INFO: Server started",
    "ERROR: Disk full",
    "INFO: Backup completed",
    "ERROR: Connection refused",
    "WARNING: CPU usage high"
]

print("========== LOG ANALYZER ==========")

error_count = 0

for log in logs:
    if "ERROR" in log:
        print(log)
        error_count += 1

print("----------------------------------")
print(f"Total errors: {error_count}")
print("==================================")