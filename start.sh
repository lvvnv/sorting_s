#!/bin/bash
# start.sh
# Script to start the application with Docker

echo "Starting the waste sorting application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "Error: docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Build and start the services
echo "Building and starting services..."
docker-compose up --build -d

# Wait a moment for services to start
sleep 10

# Check if services are running
if docker ps | grep -q "sorting_s_backend_1"; then
    echo "Backend service is running on http://localhost:8000"
else
    echo "Warning: Backend service may not be running properly"
fi

if docker ps | grep -q "sorting_s_frontend_1"; then
    echo "Frontend service is running on http://localhost:3000"
else
    echo "Warning: Frontend service may not be running properly"
fi

echo "You can access the application at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000/api/"

echo ""
echo "To stop the services, run: docker-compose down"