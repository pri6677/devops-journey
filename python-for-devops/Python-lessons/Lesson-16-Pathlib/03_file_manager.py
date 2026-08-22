from pathlib import Path

base_dir = Path("devops_files")

logs_dir = base_dir / "logs"
backups_dir = base_dir / "backups"

logs_dir.mkdir(parents=True, exist_ok=True)
backups_dir.mkdir(parents=True, exist_ok=True)

log_file = logs_dir / "server.log"

if not log_file.exists():
    log_file.write_text("INFO: Server started\n")

print("DevOps directory structure:")
print(base_dir)

for item in base_dir.rglob("*"):
    print(item)