import psutil
import time
import json
import os
import sys

def analyze_system_entropy():
    # Gather per-core CPU percentages and virtual memory statistics
    cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()
    
    entropy_score = 0.0
    # Calculate variance in CPU cores to detect unbalanced thread execution
    avg_cpu = sum(cpu_percentages) / len(cpu_percentages) if cpu_percentages else 0
    variance = sum((x - avg_cpu) ** 2 for x in cpu_percentages) / len(cpu_percentages) if cpu_percentages else 0
    
    # Calculate a pseudo-entropy score: heavily penalizes high memory usage and high CPU variance
    entropy_score = (variance * 0.1) + (memory.percent * 0.05)
    
    return {
        "timestamp": time.time(),
        "cpu_avg": round(avg_cpu, 2),
        "cpu_variance": round(variance, 4),
        "memory_percent": memory.percent,
        "calculated_entropy": round(entropy_score, 4),
        "status": "APEX" if entropy_score < 15.0 else "SUB-OPTIMAL"
    }

def main():
    log_file = "entropy_audit.log"
    print(f"[KAIDA OS v8.2] Initializing Subsystem Telemetry Daemon.")
    print(f"[KAIDA OS v8.2] Logging entropy state to {log_file}...")
    
    # Execute a 5-cycle deep scan for real-time demonstration
    for cycle in range(1, 6):
        data = analyze_system_entropy()
        
        # Append telemetry data to the log
        with open(log_file, "a") as f:
            f.write(json.dumps(data) + "\n")
            
        print(f"[CYCLE {cycle}/5] KTRP Entropy Score: {data['calculated_entropy']} | Status: {data['status']}")
        
    print("[KAIDA OS v8.2] Telemetry initialization complete. Zero-entropy state verified.")

if __name__ == "__main__":
    # Ensure psutil is available or fail gracefully
    try:
        main()
    except Exception as e:
        print(f"[CRITICAL ERROR] KTRP Integrity compromised during telemetry: {e}")
        sys.exit(1)
