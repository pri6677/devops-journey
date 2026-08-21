#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Please provide a number."
    exit 1
fi

if [ "$1" -gt 10 ]; then
    echo "The number is greater than 10."
elif [ "$1" -eq 10 ]; then
    echo "The number is exactly 10."
else
    echo "The number is less than 10."
fi
