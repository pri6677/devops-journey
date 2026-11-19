import subprocess
from datetime import datetime
from pathlib import Path

SOURCE_DIR = Path("source")
BUCKET = "s3://pri-devops-s3-lab-2026"
PROFILE = "s3-lab"

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_path = f"{BUCKET}/backups/{timestamp}/"

log_file = Path("logs/backup.log")

try:
    result = subprocess.run(
        [
            "aws", "s3", "sync",
            str(SOURCE_DIR),
            backup_path,
            "--profile", PROFILE
        ],
        check=True,
        capture_output=True,
        text=True
    )

    with log_file.open("a") as log:
        log.write(f"SUCCESS: {timestamp} - Backup completed\n")

    print("Backup completed successfully!")
    print("S3 location:", backup_path)

except subprocess.CalledProcessError as error:
    with log_file.open("a") as log:
        log.write(f"FAILED: {timestamp} - {error.stderr}\n")

    print("Backup failed!")
    print(error.stderr)
