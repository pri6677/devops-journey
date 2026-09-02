import os

environment = os.getenv("DEVOPS_ENV", "development")
server_name = os.getenv("SERVER_NAME", "localhost")
server_port = int(os.getenv("SERVER_PORT", "8080"))

print("===== ENVIRONMENT CONFIGURATION =====")
print("Environment:", environment)
print("Server:", server_name)
print("Port:", server_port)

if environment == "production":
    print("WARNING: Production environment")
else:
    print("Safe development/test environment")