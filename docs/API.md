# API Documentation

Complete reference for the Fiber Ops Dashboard REST API.

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Endpoints](#endpoints)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Overview

The Fiber Ops Dashboard provides a REST API for programmatic access to construction data, statistics, and sync operations.

### API Version

**Current Version**: 1.0.0

### Content Type

All requests and responses use `application/json` unless otherwise specified.

## Authentication

**Current**: No authentication required (internal use)

**Future**: Will support API key authentication in v2.0

## Base URL

```
http://localhost:5000
```

Or replace `localhost` with your server IP/domain.

---

## Endpoints

### 1. Health Check

Check if the API is running and responsive.

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T12:00:00.000000"
}
```

**Status Codes**:
- `200` - Service is healthy

**Example**:
```bash
curl http://localhost:5000/api/health
```

---

### 2. Sync Data

Trigger synchronization from Google Sheets to local database.

**Endpoint**: `POST /api/sync`

**Request**: No body required

**Response (Success)**:
```json
{
  "success": true,
  "message": "Successfully synced 15 records"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "message": "Sync error: Unable to connect to Google Sheets"
}
```

**Status Codes**:
- `200` - Request processed (check success field)

**Example**:
```bash
curl -X POST http://localhost:5000/api/sync
```

---

### 3. Get Statistics

Retrieve aggregate statistics for all projects.

**Endpoint**: `GET /api/stats`

**Response**:
```json
{
  "total_footage": 50000,
  "completed_footage": 35000,
  "material_cost": 150000,
  "labor_cost": 85000,
  "total_cost": 235000,
  "project_count": 10,
  "completion_percentage": 70.0
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| total_footage | Float | Total fiber footage across all projects |
| completed_footage | Float | Total completed footage |
| material_cost | Float | Total material costs (USD) |
| labor_cost | Float | Total labor costs (USD) |
| total_cost | Float | Total costs (material + labor) |
| project_count | Integer | Number of active projects |
| completion_percentage | Float | Overall completion percentage |

**Status Codes**:
- `200` - Success
- `500` - Server error

**Example**:
```bash
curl http://localhost:5000/api/stats
```

---

### 4. Get Projects

Retrieve detailed information for all projects.

**Endpoint**: `GET /api/projects`

**Response**:
```json
[
  {
    "project_name": "Main Street Fiber",
    "total_footage": 5000,
    "completed_footage": 3500,
    "material_cost": 15000,
    "labor_cost": 8000,
    "total_cost": 23000,
    "recorded_date": "2025-11-07",
    "completion_pct": 70.0
  },
  {
    "project_name": "Oak Avenue Installation",
    "total_footage": 3000,
    "completed_footage": 1500,
    "material_cost": 9000,
    "labor_cost": 5000,
    "total_cost": 14000,
    "recorded_date": "2025-11-06",
    "completion_pct": 50.0
  }
]
```

**Response Fields** (per project):

| Field | Type | Description |
|-------|------|-------------|
| project_name | String | Name of the project |
| total_footage | Float | Total fiber footage for project |
| completed_footage | Float | Completed footage |
| material_cost | Float | Material costs (USD) |
| labor_cost | Float | Labor costs (USD) |
| total_cost | Float | Total project cost |
| recorded_date | String | Date of last update (YYYY-MM-DD) |
| completion_pct | Float | Project completion percentage |

**Status Codes**:
- `200` - Success
- `500` - Server error

**Example**:
```bash
curl http://localhost:5000/api/projects
```

---

### 5. Get Sync History

Retrieve history of data synchronization operations.

**Endpoint**: `GET /api/history`

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| days | Integer | No | 30 | Number of days to look back |

**Response**:
```json
[
  {
    "id": 15,
    "sync_time": "2025-11-07T12:30:00",
    "records_synced": 10,
    "status": "success"
  },
  {
    "id": 14,
    "sync_time": "2025-11-07T08:15:00",
    "records_synced": 10,
    "status": "success"
  },
  {
    "id": 13,
    "sync_time": "2025-11-06T16:45:00",
    "records_synced": 8,
    "status": "success"
  }
]
```

**Response Fields** (per sync):

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique sync ID |
| sync_time | String | Timestamp of sync (ISO 8601) |
| records_synced | Integer | Number of records synced |
| status | String | Sync status (success/error) |

**Status Codes**:
- `200` - Success
- `500` - Server error

**Examples**:

```bash
# Get last 30 days (default)
curl http://localhost:5000/api/history

# Get last 7 days
curl http://localhost:5000/api/history?days=7

# Get last 90 days
curl http://localhost:5000/api/history?days=90
```

---

### 6. Dashboard (Web UI)

Access the web-based dashboard interface.

**Endpoint**: `GET /`

**Response**: HTML page

**Status Codes**:
- `200` - Success

**Example**:
```
http://localhost:5000/
```

---

## Response Formats

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error description",
  "message": "User-friendly error message"
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Endpoint not found |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## Error Handling

### Common Errors

#### Database Error

```json
{
  "error": "Database connection failed"
}
```

**Cause**: SQLite database is locked or inaccessible

**Solution**: Check file permissions on `data/` directory

#### Google Sheets Error

```json
{
  "success": false,
  "message": "Sync error: Unable to authenticate with Google Sheets"
}
```

**Cause**: Invalid credentials or missing permissions

**Solution**: 
- Verify `credentials/credentials.json` exists
- Check service account has access to sheet
- Verify GOOGLE_SHEET_ID is correct

#### No Data Found

```json
[]
```

**Cause**: No sync has been performed yet

**Solution**: Trigger sync with `POST /api/sync`

---

## Examples

### Python Example

```python
import requests

BASE_URL = "http://localhost:5000"

# Health check
response = requests.get(f"{BASE_URL}/api/health")
print(response.json())

# Trigger sync
response = requests.post(f"{BASE_URL}/api/sync")
print(response.json())

# Get statistics
response = requests.get(f"{BASE_URL}/api/stats")
stats = response.json()
print(f"Total Cost: ${stats['total_cost']}")

# Get all projects
response = requests.get(f"{BASE_URL}/api/projects")
projects = response.json()
for project in projects:
    print(f"{project['project_name']}: {project['completion_pct']}% complete")

# Get sync history for last 7 days
response = requests.get(f"{BASE_URL}/api/history?days=7")
history = response.json()
print(f"Number of syncs: {len(history)}")
```

### JavaScript Example

```javascript
const BASE_URL = 'http://localhost:5000';

// Get statistics
async function getStats() {
  const response = await fetch(`${BASE_URL}/api/stats`);
  const stats = await response.json();
  console.log('Total Cost:', stats.total_cost);
}

// Trigger sync
async function syncData() {
  const response = await fetch(`${BASE_URL}/api/sync`, {
    method: 'POST'
  });
  const result = await response.json();
  console.log(result.message);
}

// Get projects
async function getProjects() {
  const response = await fetch(`${BASE_URL}/api/projects`);
  const projects = await response.json();
  projects.forEach(project => {
    console.log(`${project.project_name}: ${project.completion_pct}% complete`);
  });
}
```

### cURL Examples

```bash
# Health check
curl http://localhost:5000/api/health

# Trigger sync
curl -X POST http://localhost:5000/api/sync

# Get stats
curl http://localhost:5000/api/stats

# Get projects
curl http://localhost:5000/api/projects

# Get history (last 7 days)
curl http://localhost:5000/api/history?days=7

# Pretty print JSON
curl http://localhost:5000/api/stats | python -m json.tool
```

### Shell Script Example

```bash
#!/bin/bash

BASE_URL="http://localhost:5000"

# Function to sync and report
sync_and_report() {
    echo "Triggering sync..."
    SYNC_RESULT=$(curl -s -X POST $BASE_URL/api/sync)
    echo $SYNC_RESULT
    
    echo "\nFetching statistics..."
    STATS=$(curl -s $BASE_URL/api/stats)
    echo $STATS | python -m json.tool
}

# Run it
sync_and_report
```

---

## Rate Limiting

**Current**: No rate limiting

**Future**: v2.0 will implement rate limiting:
- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## Versioning

**Current**: API v1.0 (no version in URL)

**Future**: Version will be added to URL path:
- v1: `/api/v1/stats`
- v2: `/api/v2/stats`

---

## Webhooks (Future)

Planned for v2.0:

- Sync completion webhook
- Error notification webhook
- Daily summary webhook

---

Need help? [Open an issue](https://github.com/CamoRageaholic1/fiber-ops-dashboard/issues)
