import os
import sys
import json
import subprocess
from datetime import datetime

def get_system_metrics():
    # CPU Load Average
    load1, load5, load15 = os.getloadavg()
    cpu_cores = os.cpu_count() or 1
    
    # Memory Info via 'free'
    try:
        mem_output = subprocess.check_output(['free', '-b']).decode('utf-8').split('\n')[1].split()
        total_mem = int(mem_output[1])
        used_mem = int(mem_output[2])
        mem_usage_percent = (used_mem / total_mem) * 100
    except Exception:
        total_mem = 1
        used_mem = 0
        mem_usage_percent = 0.0

    # Disk Info via 'df'
    try:
        disk_output = subprocess.check_output(['df', '/']).decode('utf-8').split('\n')[1].split()
        disk_usage_percent = disk_output[4]
    except Exception:
        disk_usage_percent = "0%"

    # Synthetic Nexus Entropy Calculation
    # Combines CPU saturation and memory consumption into a unified entropy score
    entropy = (load1 / cpu_cores) * (mem_usage_percent / 100.0)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "nexus_entropy": round(entropy, 6),
        "cpu_load_1m": round(load1, 2),
        "cpu_cores": cpu_cores,
        "memory_usage_percent": round(mem_usage_percent, 2),
        "root_disk_usage": disk_usage_percent,
        "status": "ABSOLUTE" if entropy < 0.5 else "DEGRADED - REQUIRES KTRP RECONCILIATION"
    }

if __name__ == "__main__":
    metrics = get_system_metrics()
    # Log to stdout for Kaida OS ingestion
    print(json.dumps({"KTRP_TELEMETRY_REPORT": metrics}, indent=4))
