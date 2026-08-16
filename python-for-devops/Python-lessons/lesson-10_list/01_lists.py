servers = ["web-01", "web-02", "db-01"]

print("Server inventory:")

for server in servers:
    print(server)

print(f"Total servers: {len(servers)}")