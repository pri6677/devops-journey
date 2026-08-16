ports = (22, 80, 443)

print("Allowed ports:")

for port in ports:
    print(port)

server_ips = [
    "10.0.0.1",
    "10.0.0.2",
    "10.0.0.1",
    "10.0.0.3"
]

unique_ips = set(server_ips)

print("Unique IP addresses:")
for ip in unique_ips:
    print(ip)