expected_servers = {
    "web-01",
    "web-02",
    "web-03",
    "db-01"
}

running_servers = {
    "web-01",
    "web-02",
    "db-01"
}

missing_servers = expected_servers - running_servers
unexpected_servers = running_servers - expected_servers

print("========== INFRASTRUCTURE CHECK ==========")

print(f"Expected servers: {len(expected_servers)}")
print(f"Running servers: {len(running_servers)}")

print("\nMissing servers:")

if missing_servers:
    for server in missing_servers:
        print(f"- {server}")
else:
    print("None")

print("\nUnexpected servers:")

if unexpected_servers:
    for server in unexpected_servers:
        print(f"- {server}")
else:
    print("None")

print("==========================================")