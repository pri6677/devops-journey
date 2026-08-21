#!/bin/bash

echo "===== SERVER CHECK ====="

echo "Hostname: $HOSTNAME"
echo "User: $USER"

echo
echo "Checking required commands..."

for command in bash python3 ssh
do
    if command -v "$command" > /dev/null 2>&1; then
        echo "$command: available"
    else
        echo "$command: NOT FOUND"
    fi
done

echo
echo "===== CHECK COMPLETE ====="
