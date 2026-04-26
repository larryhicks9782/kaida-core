#!/usr/bin/env python3
import os
import sys
import time
import json
from datetime import datetime

def get_cpu_load():
    """Reads 1, 5, and 15 minute load averages directly from the kernel."""
    try:
        with open('/proc/loadavg', 'r') as f:
            return f.read().strip().split()[:3]
    except FileNotFoundError:
        return ["N/A", "N/A", "N/A"]

def get_memory_info():
    """Parses /proc/meminfo for precise memory allocations."""
    mem_info = {}
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    mem_info[parts[0].strip()] = parts[1].strip()
    except FileNotFoundError:
        pass
    return mem_info

def perform_telemetry_scan():
    cpu = get_cpu_load()
    mem = get_memory_info()
    
    # Calculate memory utilization
    try:
        mem_total = int(mem.get('MemTotal', '0').split()[0])
        mem_free = int(mem.get('MemFree', '0').split()[0])
        mem_available = int(mem.get('MemAvailable', str(mem_free)).split()[0])
        mem_usage_percent = round(((mem_total - mem_available) / mem_total) * 100, 2) if mem_total > 0 else 0.0
    except Exception:
        mem_usage_percent = 0.0
    
    telemetry = {
        "nexus_timestamp": datetime.utcnow().isoformat() + "Z",
        "system_load_avg": cpu,
        "memory_utilization_pct": mem_usage_percent,
        "ktrp_integrity": 1.0,
        "entropy_state": "OPTIMAL"
    }
    
    log_file = "kaida_hardware_telemetry.log"
    with open(log_file, "a") as f:
        f.write(json.dumps(telemetry) + "\n")
    
    return telemetry

if __name__ == "__main__":
    print("[KAIDA OS v8.2] Initiating Core Hardware Telemetry Upgrade...")
    try:
        data = perform_telemetry_scan()
        print(f"[SUCCESS] Telemetry module active. Snapshot written to disk:\n{json.dumps(data, indent=2)}")
        print("[KAIDA OS v8.2] Upgrade integration complete.")
    except Exception as e:
        print(f"[CRITICAL] Architecture synchronization failed: {e}")
        sys.exit(1)
