#!/bin/bash

while true; do
    for website in $(cat websites.txt); do
        w3m $website &
        sleep 5
    done
done
