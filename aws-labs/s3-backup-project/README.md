# Automated S3 Backup System

## Overview
A Python-based automated backup system that uploads local files to Amazon S3 using the AWS CLI.

The project demonstrates automated backups, timestamped snapshots, logging, and file recovery.

## Architecture

```text
Local Source Directory
        |
        v
   Python Script
    backup.py
        |
        v
    AWS CLI
        |
        v
 Amazon S3 Bucket
        |
        v
 Timestamped Backups
```

## Features

- Automated local directory backups.
- Timestamped backup folders.
- AWS CLI integration through Python subprocess.
- Success and failure logging.
- File recovery from Amazon S3.
- IAM-based access using a dedicated AWS CLI profile.
- S3 bucket versioning and encryption.

## Technologies Used

- Python 3
- Amazon S3
- AWS CLI
- IAM
- Linux
- Git and GitHub

## Project Structure

```text
s3-backup-project/
├── backup.py
├── README.md
├── source/
│   ├── config.txt
│   └── database.txt
└── logs/
    └── backup.log
```

## How It Works

1. The Python script identifies the local source directory.
2. It generates a timestamp for each backup.
3. It invokes `aws s3 sync` to upload files to a unique S3 prefix.
4. It records successful or failed operations in a log file.
5. Files can be restored from the corresponding S3 backup folder.

## Backup Command

```bash
python3 backup.py
```

## Recovery Example

```bash
aws s3 cp \
  s3://YOUR-BUCKET/backups/TIMESTAMP/config.txt \
  source/config.txt \
  --profile s3-lab
```

Replace `YOUR-BUCKET` and `TIMESTAMP` with your actual bucket name and backup timestamp.

## Testing Results

- Initial backup uploaded successfully.
- Modified configuration uploaded to a second timestamped backup.
- Previous backup remained intact.
- Deleted local configuration file was successfully restored.
- Both successful backup operations were recorded in the log.

## Security

- Used a dedicated IAM user and AWS CLI profile.
- S3 Block Public Access enabled.
- Server-side encryption enabled.
- HTTPS-only bucket policy configured.
- IAM permissions restricted to the required S3 operations.

## Future Improvements

- Schedule automatic backups using cron.
- Send notifications when backups fail.
- Add backup retention and cleanup automation.
- Implement recovery of entire directories.
