#!/bin/bash

# Constants
DOCKER_COMPOSE_FILE="docker/docker-compose.dev.yml"
WEB_APP_CONTAINER_NAME="web_app_container"

# Step 1: Clean Docker
echo "Running Docker cleanup script..."
sudo scripts/clean_docker.sh sh

# Step 2: Start Docker Compose
echo "Starting Docker containers with docker-compose..."
docker compose -f $DOCKER_COMPOSE_FILE up -d
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Docker containers."
    exit 1
fi

# Step 3: Execute setup commands in the container
echo "Running setup commands inside the web application container..."
sudo docker exec -i $WEB_APP_CONTAINER_NAME bash -c "
    apt update && \
    apt install -y chromium && \
    curl -o google-chrome-stable.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable.deb || apt-get -f install -y && \
    apt-get update && \
    apt-get install -y chromium-driver
"

if [ $? -ne 0 ]; then
    echo "Error: Failed to execute setup commands in the container."
    exit 1
fi

echo "Setup completed successfully!"
