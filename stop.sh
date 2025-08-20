#!/bin/bash
# stop.sh
# Script to stop the application

echo "Stopping the waste sorting application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Error: Docker is not installed."
    exit 1
fi

# Stop the services
echo "Stopping services..."
docker-compose down

echo "Services have been stopped."