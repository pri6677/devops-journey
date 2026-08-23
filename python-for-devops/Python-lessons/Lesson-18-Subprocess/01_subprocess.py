import subprocess

result = subprocess.run(["pwd"])

print(result)



result = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True
)

print(result.stdout)