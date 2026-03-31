#!/bin/bash
# --- TITAN FOREVER UPLINK ---
echo "📡 [TITAN] Initializing Maryland Lab Cloud Sync..."

# Move to the project root
cd ~/titan_system

# Add all new scripts, logs, and memory updates
git add .

# Create a timestamped commit
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "🚀 Titan Logic Update: $TIMESTAMP"

# Push to the Kaida 2.0 GitHub Vault
# Using the ghp_ token we already linked
git push origin main

echo "✅ [STATUS] Memory Secured in Kaida Vault."
