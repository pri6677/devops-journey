with open("server.log", "r") as file:
    content = file.read()

print(content)

with open("report.txt", "w") as file:
    file.write("Server health check completed\n")


with open("report.txt", "a") as file:
    file.write("CPU usage: 42%\n")