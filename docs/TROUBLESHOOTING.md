# Troubleshooting Guide

Common issues and solutions for Fiber Ops Dashboard.

## Connection Issues

### Can't Access Dashboard

**Check service is running:**
```bash
docker ps
```

**Check logs:**
```bash
docker-compose logs -f
```

## Sync Issues

### Google Sheets Sync Fails

1. Verify credentials.json exists
2. Check service account has sheet access
3. Confirm GOOGLE_SHEET_ID is correct
4. Verify sheet column headers match exactly

### No Data Appears

1. Click "Sync Now" to trigger initial sync
2. Check browser console for errors
3. Verify API endpoint: `curl http://localhost:5000/api/health`

## Docker Issues

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :5000

# Change port in .env
PORT=5001
```

### Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

For more help, see: https://github.com/CamoRageaholic1/fiber-ops-dashboard/issues
