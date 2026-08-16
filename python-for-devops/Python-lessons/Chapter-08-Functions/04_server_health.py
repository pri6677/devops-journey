def check_cpu(cpu_usage):
    if cpu_usage >= 80:
        return "WARNING: High CPU usage"
    return "CPU usage is normal"


def check_memory(memory_usage):
    if memory_usage >= 80:
        return "WARNING: High memory usage"
    return "Memory usage is normal"


def check_disk(disk_usage):
    if disk_usage >= 90:
        return "CRITICAL: Disk usage is very high"
    elif disk_usage >= 80:
        return "WARNING: Disk usage is high"
    return "Disk usage is normal"


print("========== SERVER HEALTH ==========")

print(check_cpu(87))
print(check_memory(65))
print(check_disk(91))

print("===================================")