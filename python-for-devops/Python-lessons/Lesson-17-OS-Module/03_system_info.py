import os

print("===== SYSTEM INFORMATION =====")

print(f"Operating system: {os.name}")
print(f"Current directory: {os.getcwd()}")
print(f"Current user: {os.getenv('USER')}")
print(f"Home directory: {os.getenv('HOME')}")

print("\n===== DIRECTORY CONTENTS =====")

for item in os.listdir():
    print(item)