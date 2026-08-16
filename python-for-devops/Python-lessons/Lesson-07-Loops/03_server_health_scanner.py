servers = ["web-01", "web-02", "web-03"]

cpu_usage = [45, 87, 62]

for i in range(len(servers)):
    server = servers[i]
    cpu = cpu_usage[i]

    print(f"{server}: CPU {cpu}%")

    if cpu > 80:
        print("  WARNING: High CPU usage")
    else:
        print("  CPU usage is normal")