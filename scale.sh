#!/bin/bash

scale_up=5
scale_down=3

current_replicas=$(docker-compose ps -q WhistApp | wc -l)

if [ "$current_replicas" -eq $scale_down ]; then
    echo "Scaling up to $scale_up replicas..."
    docker-compose up -d --scale WhistApp=$scale_up
elif [ "$current_replicas" -eq $scale_up ]; then
    echo "Scaling down to $scale_down replicas..."
    docker-compose up -d --scale WhistApp=$scale_down
else
    echo "Current replicas are neither $scale_up nor $scale_down."
fi