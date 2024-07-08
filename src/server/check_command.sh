#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Error: Exactly one argument should be provided."
    exit 1
fi

if [ $1 == "STATUS" ]; then
    uptime
elif [ $1 == "DISK" ]; then
    df -h
elif [ $1 == "CPU" ]; then
    top -n 1 -b
else
    echo "Error: The argument $1 is not supported"
    exit 1
fi

exit 0
