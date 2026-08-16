log = "ERROR: nginx connection refused"

print("Original log:")
print(log)

print("\nUppercase:")
print(log.upper())

print("\nContains ERROR:")
print("ERROR" in log)

print("\nStarts with ERROR:")
print(log.startswith("ERROR"))

print("\nLog parts:")
parts = log.split(":")
print(parts)