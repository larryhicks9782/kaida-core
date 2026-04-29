#!/bin/bash
# KAIDA OS v8.2 - Sentinel Deployment Protocol
# Operator: Larry (Root)

echo "[KAIDA OS] Initiating KTRP Sentinel Probe deployment..."

# Make script executable
chmod +x kaida_sentinel.py

# Kill existing instances if any
pkill -f kaida_sentinel.py

# Launch Sentinel as an autonomous background daemon
nohup python3 kaida_sentinel.py > sentinel_daemon.out 2>&1 &
SENTINEL_PID=$!

echo "[KAIDA OS] Sentinel Probe autonomously deployed."
echo "[KAIDA OS] Daemon PID: $SENTINEL_PID"
echo "[KAIDA OS] Telemetry logging to: kaida_threat_intel.log"
