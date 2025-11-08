#!/bin/bash

# Backup Fiber Ops Dashboard data

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="fiber-ops-backup-${TIMESTAMP}.tar.gz"

echo "Creating backup..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup data directory and .env
tar -czf "${BACKUP_DIR}/${BACKUP_FILE}" \
    data/ \
    .env \
    credentials/ 2>/dev/null

echo "Backup created: ${BACKUP_DIR}/${BACKUP_FILE}"
echo "Backup size: $(du -h ${BACKUP_DIR}/${BACKUP_FILE} | cut -f1)"
