cpu_usage = 87
memory_usage = 65
disk_usage = 91

cpu_threshold = 80
memory_threshold = 80
disk_threshold = 90

print("========== SERVER HEALTH ==========")

print(f"CPU Usage: {cpu_usage}%")
print(f"Memory Usage: {memory_usage}%")
print(f"Disk Usage: {disk_usage}%")

print()

print(f"CPU high: {cpu_usage > cpu_threshold}")
print(f"Memory high: {memory_usage > memory_threshold}")
print(f"Disk high: {disk_usage > disk_threshold}")

print("===================================")