server = {
    "name": "web-01",
    "ip": "10.0.0.10",
    "port": 80,
    "environment": "production",
    "status": "running"
}

print("========== SERVER CONFIGURATION ==========")

print(f"Name: {server['name']}")
print(f"IP: {server['ip']}")
print(f"Port: {server['port']}")
print(f"Environment: {server['environment']}")
print(f"Status: {server['status']}")

print("\nConfiguration:")
for key, value in server.items():
    print(f"{key}: {value}")

print("===========================================")