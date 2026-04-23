#!/bin/bash
while true
do
    # Check if the memory file has changed
    cd /root/titan_system
    git add titan_memory.json
    git commit -m "Memory Pulse: Synced Intelligence State"
    git push origin main
    # Wait 10 minutes before the next pulse
    sleep 600
done
