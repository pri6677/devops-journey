#!/bin/bash

set -euo pipefail

name=""
environment=""

while getopts "n:e:" opt; do
    case "$opt" in
        n)
            name="$OPTARG"
            ;;
        e)
            environment="$OPTARG"
            ;;
        *)
            echo "Usage: $0 -n server-name -e environment"
            exit 1
            ;;
    esac
done

if [ -z "$name" ] || [ -z "$environment" ]; then
    echo "Error: server name and environment are required."
    echo "Usage: $0 -n server-name -e environment"
    exit 1
fi

echo "===== SERVER INFO ====="
echo "Server: $name"
echo "Environment: $environment"
echo "Status: Ready"
echo "======================"