servers = [
    "web-01",
    "web-02",
    "web-03",
    "db-01"
]

print("========== SERVER INVENTORY ==========")

for server in servers:
    print(f"Server: {server}")

print("--------------------------------------")
print(f"Total servers: {len(servers)}")

if "db-01" in servers:
    print("Database server found")

if "web-05" not in servers:
    print("web-05 is not in the inventory")

print("======================================")