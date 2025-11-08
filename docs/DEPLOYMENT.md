# Deployment Guide

Guide for deploying Fiber Ops Dashboard to production.

## Docker Deployment (Recommended)

```bash
# Clone repository
git clone https://github.com/CamoRageaholic1/fiber-ops-dashboard.git
cd fiber-ops-dashboard

# Configure environment
cp .env.example .env
nano .env

# Add credentials
cp /path/to/credentials.json credentials/

# Build and start
docker-compose up -d
```

## Access

Dashboard available at: `http://your-server-ip:5000`

## Security

- Use reverse proxy (Nginx/Traefik) for SSL
- Restrict port access with firewall
- Regular security updates
- Secure credentials storage
