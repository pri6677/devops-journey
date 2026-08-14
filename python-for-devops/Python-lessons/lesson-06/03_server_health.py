cpu_usage = 87
memory_usage = 65
disk_usage = 91

print("========== SERVER HEALTH ==========")

if cpu_usage > 80:
    print("WARNING: High CPU usage")
else:
    print("CPU usage is normal")

if memory_usage > 80:
    print("WARNING: High memory usage")
else:
    print("Memory usage is normal")

if disk_usage >= 90:
    print("CRITICAL: Disk usage is very high")
elif disk_usage >= 80:
    print("WARNING: Disk usage is high")
else:
    print("Disk usage is normal")

print("===================================")