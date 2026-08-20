#!/bin/bash

system_info() {
    echo "=============================="
    echo "       SYSTEM INFORMATION"
    echo "=============================="
    echo "User:              $USER"
    echo "Hostname:          $HOSTNAME"
    echo "Home:              $HOME"
    echo "Shell:             $SHELL"
    echo "Current directory: $PWD"
    echo "=============================="
}

hello() {
    if [ $# -eq 0 ]; then
        echo "Error: Please provide your name."
        return 1
    fi

    echo "Hello, $1!"
}

echo "Running system information..."
system_info

echo

if [ $# -eq 0 ]; then
    echo "Usage: $0 <name>"
    exit 1
fi

hello "$1"
