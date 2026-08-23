import subprocess

print("===== SYSTEM CHECK =====")

commands = [
    ["hostname"],
    ["uptime"],
    ["df", "-h"]
]

for command in commands:
    print(f"\n$ {' '.join(command)}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Command failed:")
        print(result.stderr)