cpu_usage = 87
cpu_threshold = 80

print("CPU:", cpu_usage)
print("Threshold:", cpu_threshold)

print("CPU high:", cpu_usage > cpu_threshold)

remaining = 100 - cpu_usage
print("Remaining capacity:", remaining)