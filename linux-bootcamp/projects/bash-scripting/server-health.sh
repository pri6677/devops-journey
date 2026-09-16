#!/bin/bash

set -euo pipefail

LOG_FILE="server-health.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

cleanup() {
    log "Script finished"
}

trap cleanup EXIT

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

environment="$1"

if [ "$environment" != "production" ] && [ "$environment" != "development" ]; then
    echo "Error: environment must be production or development"
    exit 1
fi

log "Starting server health check"
log "Environment: $environment"

log "Hostname: $(hostname)"
log "Current user: $(whoami)"

log "Checking disk usage"

if df -h / | tee -a "$LOG_FILE"; then
    log "Disk check completed"
else
    log "Disk check failed"
    exit 1
fi

log "Checking memory"

if free -h | tee -a "$LOG_FILE"; then
    log "Memory check completed"
else
    log "Memory check failed"
    exit 1
fi

log "Server health check completed successfully"