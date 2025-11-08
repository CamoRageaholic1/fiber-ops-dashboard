# Installation Guide

Complete installation instructions for the Fiber Ops Dashboard.

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Install (Automated)](#quick-install-automated)
- [Manual Installation](#manual-installation)
- [Docker Installation](#docker-installation)
- [Verification](#verification)
- [Next Steps](#next-steps)

## System Requirements

### Minimum Requirements

- **OS**: Ubuntu 22.04+ (or compatible Linux distribution)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 5GB available
- **Network**: Internet connection for Docker images and Google Sheets API

### Software Dependencies

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+ (for manual installation)
- Git

## Quick Install (Automated)

### Step 1: Clone Repository

```bash
git clone https://github.com/CamoRageaholic1/fiber-ops-dashboard.git
cd fiber-ops-dashboard
```

### Step 2: Run Installer

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

The installer will:
- Update system packages
- Install Docker and Docker Compose
- Create necessary directories
- Set up environment file

### Step 3: Configure Environment

Edit `.env` file with your settings:

```bash
nano .env
```

```env
GOOGLE_SHEET_ID=your_google_sheet_id_here
FLASK_SECRET_KEY=generate_random_key_here
FLASK_ENV=production
PROJECT_NAME=Your-Project-Name
```

### Step 4: Add Credentials

```bash
# Copy your Google service account credentials
cp /path/to/credentials.json credentials/credentials.json
```

### Step 5: Build and Start

```bash
docker-compose build
docker-compose up -d
```

### Step 6: Access Dashboard

Open browser to: `http://localhost:5000` or `http://YOUR_SERVER_IP:5000`

---

## Manual Installation

### Step 1: Install System Dependencies

```bash
# Update package list
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3.11 python3-pip python3-venv -y

# Install Git
sudo apt install git -y
```

### Step 2: Clone Repository

```bash
git clone https://github.com/CamoRageaholic1/fiber-ops-dashboard.git
cd fiber-ops-dashboard
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Python Dependencies

```bash
pip install -r app/requirements.txt
```

### Step 5: Configure Environment

```bash
cp .env.example .env
nano .env
```

### Step 6: Add Credentials

```bash
mkdir -p credentials
cp /path/to/credentials.json credentials/credentials.json
```

### Step 7: Create Database Directory

```bash
mkdir -p data
```

### Step 8: Run Application

```bash
cd app
python app.py
```

---

## Docker Installation

### Installing Docker

```bash
# Add Docker's official GPG key
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
```

### Installing Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

---

## Configuration Details

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|----------|
| `GOOGLE_SHEET_ID` | Yes | ID from your Google Sheet URL | `1abc...xyz` |
| `FLASK_SECRET_KEY` | Yes | Secret key for Flask sessions | `random-string-here` |
| `FLASK_ENV` | No | Environment mode | `production` or `development` |
| `PROJECT_NAME` | No | Display name for project | `My-Fiber-Project` |
| `PORT` | No | Port to run on (default: 5000) | `5000` |

### Generating Secret Key

```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

### Directory Structure

```
fiber-ops-dashboard/
├── app/                 # Application code
├── credentials/         # Google credentials (gitignored)
├── data/                # SQLite database (gitignored)
├── docs/                # Documentation
├── scripts/             # Helper scripts
├── .env                 # Environment config (gitignored)
├── .env.example         # Example environment file
├── docker-compose.yml   # Docker configuration
└── Dockerfile           # Docker image definition
```

---

## Verification

### Check Service Status

```bash
# View running containers
docker ps

# View logs
docker-compose logs -f

# Check health
curl http://localhost:5000/api/health
```

Expected health response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T12:00:00.000000"
}
```

### Test Data Sync

1. Open dashboard: `http://localhost:5000`
2. Click "Sync Now" button
3. Verify data loads from Google Sheets
4. Check statistics cards populate
5. Confirm project table shows data

---

## Troubleshooting Installation

### Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in
```

### Port Already in Use

```bash
# Check what's using port 5000
sudo lsof -i :5000

# Change port in .env
PORT=5001

# Or kill the process
sudo kill -9 <PID>
```

### Credentials Not Found

```bash
# Verify file exists
ls -la credentials/credentials.json

# Check permissions
chmod 600 credentials/credentials.json
```

### Docker Build Fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

---

## Next Steps

After successful installation:

1. [Configure Google Sheets](GOOGLE_SHEETS_SETUP.md)
2. [Review Configuration Options](CONFIGURATION.md)
3. [Learn the API](API.md)
4. [Deploy to Production](DEPLOYMENT.md)

---

## Uninstallation

### Remove Application

```bash
# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Delete directory
cd ..
rm -rf fiber-ops-dashboard
```

### Remove Docker (Optional)

```bash
sudo apt remove docker-ce docker-ce-cli containerd.io
sudo rm -rf /var/lib/docker
```

---

Need help? [Open an issue](https://github.com/CamoRageaholic1/fiber-ops-dashboard/issues)
