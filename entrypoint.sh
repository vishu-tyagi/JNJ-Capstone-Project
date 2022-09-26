#!/bin/bash

#Set DEBUG=true to debug container
DEBUG=false
if ${DEBUG}; then
    if [ -f "already_ran" ]; then
        echo "Already ran the Entrypoint once. Holding indefinitely for debugging."
        cat
    fi
    touch already_ran
fi

case $1 in
    fetch)
    callable="fetch"
    ;;
    *)
    echo "Invalid endpoint $1"
    exit 1
    ;;
esac

CMD="python3 -m capstone $callable"

exec $CMD