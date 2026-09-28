
servers = {
    "web-01" : {
        "status": "running",
        "cpu": 45,
        "memory": 60
    },
    "web-02" : {
        "status": "running",
        "cpu": 75,
        "memory": 90
    },
    "db-01" : {
        "status": "running",
        "cpu": 60,
        "memory": 90
    },

    }
def check_server(server_name, server_info):
    status = server_info["status"]
    cpu = server_info["cpu"]
    memory = server_info["memory"]

    if status != "running":
        health = "Server down"
    elif cpu > 80:
        health = "High CPU"
    elif memory > 90:
        health = "Low memory"
    else:
        health = "healthy"

    print(server_name)
    print("Status:", status)
    print("CPU:", cpu)
    print("Memory:", memory)
    print("Health:", health)
    print()


print("========== Server Health ==========")
print()

for server_name, server_info in servers.items():
    check_server(server_name, server_info)