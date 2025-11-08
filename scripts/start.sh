#!/bin/bash

# Start the Fiber Ops Dashboard

echo "Starting Fiber Ops Dashboard..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Copy .env.example to .env and configure it."
    exit 1
fi

# Check if credentials exist
if [ ! -f credentials/credentials.json ]; then
    echo "Error: credentials/credentials.json not found!"
    echo "Please place your Google service account credentials in credentials/credentials.json"
    exit 1
fi

# Start with docker-compose
docker-compose up -d

echo "Dashboard started successfully!"
echo "Access it at: http://localhost:5000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
