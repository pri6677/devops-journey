import os

print("===== OS MODULE BASICS =====")

print("Operating system:", os.name)
print("Current directory:", os.getcwd())
print("Current user:", os.getenv("USER"))
print("Home directory:", os.getenv("HOME"))

print("\n===== DIRECTORY CONTENTS =====")

for item in os.listdir():
    print(item)