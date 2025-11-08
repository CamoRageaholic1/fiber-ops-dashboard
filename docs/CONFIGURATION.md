# Configuration Guide

Detailed configuration options for the Fiber Ops Dashboard.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Google Sheets Configuration](#google-sheets-configuration)
- [Database Configuration](#database-configuration)
- [Docker Configuration](#docker-configuration)
- [Security Settings](#security-settings)
- [Advanced Options](#advanced-options)

## Environment Variables

### Required Variables

#### GOOGLE_SHEET_ID

```env
GOOGLE_SHEET_ID=1abc123def456ghi789jkl
```

**Description**: The unique identifier for your Google Sheet.

**How to find it**:
1. Open your Google Sheet
2. Look at the URL: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
3. Copy the SHEET_ID portion

#### FLASK_SECRET_KEY

```env
FLASK_SECRET_KEY=your-secret-key-here
```

**Description**: Secret key used for Flask session security.

**Generate one**:
```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

**Important**: Never commit this to version control!

### Optional Variables

#### FLASK_ENV

```env
FLASK_ENV=production  # or 'development'
```

**Options**:
- `production` - Production mode (recommended)
  - Debug mode off
  - Error pages hide details
  - Optimized performance
  
- `development` - Development mode
  - Debug mode on
  - Auto-reload on code changes
  - Detailed error pages

#### PROJECT_NAME

```env
PROJECT_NAME=My-Fiber-Project
```

**Description**: Display name for your project (used in logs and future features).

#### PORT

```env
PORT=5000
```

**Description**: Port number for the application to listen on.

**Default**: 5000

**Note**: If you change this, also update `docker-compose.yml` port mapping.

---

## Google Sheets Configuration

### Required Sheet Format

Your Google Sheet **must** have these columns (exact names):

| Column Name | Type | Description |
|-------------|------|-------------|
| Project Name | Text | Name of the construction project |
| Total Footage | Number | Total fiber footage for project |
| Completed Footage | Number | Amount completed to date |
| Material Cost | Number | Cost of materials (USD) |
| Labor Cost | Number | Cost of labor (USD) |
| Total Cost | Number | Total project cost (USD) |
| Date | Date | Date of record |

### Example Sheet Structure

```
| Project Name | Total Footage | Completed Footage | Material Cost | Labor Cost | Total Cost | Date |
|--------------|---------------|-------------------|---------------|------------|------------|------|
| Main Street  | 5000          | 3500              | 15000         | 8000       | 23000      | 11/01/2025 |
| Oak Avenue   | 3000          | 1500              | 9000          | 5000       | 14000      | 11/02/2025 |
```

### Service Account Setup

1. **Create Service Account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable Google Sheets API
   - Create Service Account
   - Download JSON credentials

2. **Share Sheet with Service Account**
   - Open your Google Sheet
   - Click "Share"
   - Add service account email (from credentials JSON)
   - Give "Viewer" permission

3. **Place Credentials**
   ```bash
   cp /path/to/credentials.json credentials/credentials.json
   chmod 600 credentials/credentials.json
   ```

See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for detailed instructions.

---

## Database Configuration

### SQLite Settings

**Location**: `data/fiber_ops.db`

**Schema**:
```sql
-- Sync history table
CREATE TABLE sync_history (
    id INTEGER PRIMARY KEY,
    sync_time TIMESTAMP,
    records_synced INTEGER,
    status TEXT
);

-- Project data table
CREATE TABLE project_data (
    id INTEGER PRIMARY KEY,
    sync_id INTEGER,
    project_name TEXT,
    total_footage REAL,
    completed_footage REAL,
    material_cost REAL,
    labor_cost REAL,
    total_cost REAL,
    recorded_date DATE,
    FOREIGN KEY (sync_id) REFERENCES sync_history(id)
);
```

### Database Backup

```bash
# Manual backup
cp data/fiber_ops.db data/fiber_ops_backup_$(date +%Y%m%d).db

# Using backup script
./scripts/backup.sh
```

### Database Reset

```bash
# Stop application
docker-compose down

# Remove database
rm data/fiber_ops.db

# Restart (database will be recreated)
docker-compose up -d
```

---

## Docker Configuration

### docker-compose.yml Settings

#### Port Mapping

```yaml
ports:
  - "5000:5000"  # host:container
```

Change host port if 5000 is in use:
```yaml
ports:
  - "8080:5000"  # Access on port 8080
```

#### Volume Mounts

```yaml
volumes:
  - ./app:/app                      # Application code
  - ./data:/app/data                # Database
  - ./credentials:/app/credentials:ro  # Credentials (read-only)
  - ./.env:/app/.env:ro             # Environment (read-only)
```

#### Resource Limits

Add resource constraints:

```yaml
services:
  web:
    # ... other settings ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

#### Health Check

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Development Configuration

Use `docker-compose.dev.yml` for development:

```bash
docker-compose -f docker-compose.dev.yml up
```

Features:
- Auto-reload on code changes
- Debug mode enabled
- Verbose logging

---

## Security Settings

### File Permissions

```bash
# Credentials (read-only for owner)
chmod 600 credentials/credentials.json

# Environment file (read-only for owner)
chmod 600 .env

# Scripts (executable)
chmod +x scripts/*.sh

# Data directory (read-write for owner)
chmod 700 data/
```

### Docker Security

#### Run as Non-Root User

Add to Dockerfile:

```dockerfile
# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser
```

#### Read-Only Root Filesystem

```yaml
services:
  web:
    read_only: true
    tmpfs:
      - /tmp
      - /app/data
```

### Network Security

#### Restrict External Access

```yaml
ports:
  - "127.0.0.1:5000:5000"  # Only localhost
```

#### Use Reverse Proxy

See [DEPLOYMENT.md](DEPLOYMENT.md) for Nginx/Traefik setup.

---

## Advanced Options

### Auto-Sync Configuration

Modify `app/templates/index.html` to change auto-sync interval:

```javascript
// Auto-refresh every 5 minutes (300000ms)
setInterval(async () => {
    await loadStats();
    await loadProjects();
}, 300000);  // Change this value
```

### Custom Logging

Add to `app/app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/app.log'),
        logging.StreamHandler()
    ]
)
```

### Multiple Sheets Support

To sync from multiple sheets, modify the sync function:

```python
SHEET_IDS = [
    os.getenv('GOOGLE_SHEET_ID_1'),
    os.getenv('GOOGLE_SHEET_ID_2'),
]

def sync_from_all_sheets():
    for sheet_id in SHEET_IDS:
        sync_from_sheet(sheet_id)
```

---

## Environment Examples

### Development

```env
GOOGLE_SHEET_ID=your_sheet_id
FLASK_SECRET_KEY=dev-secret-key
FLASK_ENV=development
PROJECT_NAME=Dev-Project
PORT=5000
```

### Production

```env
GOOGLE_SHEET_ID=your_sheet_id
FLASK_SECRET_KEY=super-secure-production-key
FLASK_ENV=production
PROJECT_NAME=Production-Project
PORT=5000
```

### Testing

```env
GOOGLE_SHEET_ID=test_sheet_id
FLASK_SECRET_KEY=test-key
FLASK_ENV=development
PROJECT_NAME=Test-Project
PORT=5001
```

---

## Validation

### Check Configuration

```bash
# View environment variables
docker-compose config

# Test Google Sheets connection
curl -X POST http://localhost:5000/api/sync

# Check logs
docker-compose logs -f
```

---

Need help? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [open an issue](https://github.com/CamoRageaholic1/fiber-ops-dashboard/issues).
