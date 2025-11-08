#!/bin/bash

# Fiber Ops Dashboard - Installation Script
# For Ubuntu Server 22.04+

set -e

echo "========================================"
echo "Fiber Ops Dashboard - Automated Installer"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "Please don't run as root. Run as regular user with sudo privileges."
   exit 1
fi

# Update system
echo "[1/6] Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "[2/6] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker installed successfully"
else
    echo "Docker already installed"
fi

# Install Docker Compose
echo "[3/6] Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose installed successfully"
else
    echo "Docker Compose already installed"
fi

# Create necessary directories
echo "[4/6] Creating directories..."
mkdir -p data credentials

# Copy environment file
echo "[5/6] Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from example"
    echo "⚠️  IMPORTANT: Edit .env file with your configuration!"
else
    echo ".env file already exists"
fi

# Instructions for credentials
echo "[6/6] Final setup instructions..."
echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Google Sheet ID and other settings"
echo "2. Place your Google credentials.json in the credentials/ directory"
echo "3. Run: docker-compose build"
echo "4. Run: docker-compose up -d"
echo "5. Access dashboard at http://localhost:5000"
echo ""
echo "For detailed instructions, see docs/INSTALLATION.md"
echo ""
