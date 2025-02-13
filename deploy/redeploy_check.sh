#!/bin/bash

# Default values
ALERT_TOKEN=""
MEMCACHED_HOST=""

# Check for arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -a|--alert-token)
            ALERT_TOKEN="$2"
            shift 2
            ;;
        -m|--memcached-host)
            MEMCACHED_HOST="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

echo "ALERTS"

echo "ALERT_TOKEN: $ALERT_TOKEN"
echo "MEMCACHED_HOST: $MEMCACHED_HOST"


# Updating the Git repo
echo "Updating Git repo..."
#cd /path/to/your/git/repo
git pull

# Moving to the deployment directory
echo "Moving to deployment directory..."
cd check

# Building Docker image
echo "Building Docker image..."
docker build -t map_check -f DockerfileCheck .

# Stopping and removing the old container (if exists)
echo "Stopping and removing old container..."
docker stop map_check || true
docker rm map_check || true

# Deploying the new container
echo "Deploying new container..."
docker run --name map_check --restart unless-stopped -d --env MEMCACHED_HOST="$MEMCACHED_HOST" map_check

echo "Container deployed successfully!"

