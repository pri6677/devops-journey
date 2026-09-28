servers = {
    "web-01": 75,
    "web-02": 91,
    "db-01": 60,
    "web-03": 88
}

for server, cpu in servers.items():
    if cpu > 80:
        print(server + ": High CPU")
    else:
        print(server + ": Normal")
