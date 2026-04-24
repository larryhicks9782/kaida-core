#!/bin/bash
echo "🚀 Initializing Titan Cloud Uplink..."

# Check if rclone is installed
if ! command -v rclone &> /dev/null; then
    echo "⚠️ rclone not found. Installing..."
    apt update && apt install -y rclone
fi

# The Sync Command
# Note: 'baltimore-node' must be configured in rclone
rclone sync ~/titan_system baltimore-node:titan_backup --progress \
    --exclude "**/__pycache__/**" \
    --exclude "titan_venv/**"

echo "✅ Backup Complete: Baltimore Node is in sync."
