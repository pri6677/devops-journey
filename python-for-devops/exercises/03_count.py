servers ={
    "web-01": "running",
    "web-02": "stopped",
    "db-01": "running",
}   


count = 0
for server in servers:
    if servers[server] == "running":
        count += 1

print(count)