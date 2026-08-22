error_count = 0

with open("server.log", "r") as file:
    for line in file:
        line = line.strip()

        if "ERROR" in line:
            print(f"ERROR FOUND: {line}")
            error_count += 1

print("----------------------------")
print(f"Total errors: {error_count}")
