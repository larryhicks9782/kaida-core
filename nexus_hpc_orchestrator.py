import subprocess
import psutil
import signal
import time
import shlex

print("[KTRP] NEXUS HPC ORCHESTRATOR INITIALIZED.")
with open("hpc_config.txt", "r") as f:
    cmd = shlex.split(f.read().strip())

proc = subprocess.Popen(cmd)
print(f"[NEXUS] Payload spawned from config. PID: {proc.pid}")

paused = False
try:
    parent = psutil.Process(proc.pid)
    while True:
        # Measure load
        total_process_cpu = parent.cpu_percent(interval=None)
        for child in parent.children(recursive=True):
            total_process_cpu += child.cpu_percent(interval=None)
        
        cpu_load = total_process_cpu / psutil.cpu_count()
        print(f"[TELEMETRY] CPU Load: {cpu_load:.1f}% | Paused: {paused}")

        # Simple Thermal Governor
        if not paused and cpu_load > 85.0:
            print("[!!!] THERMAL LIMIT REACHED - FREEZING [!!!]")
            for child in parent.children(recursive=True): child.send_signal(signal.SIGSTOP)
            parent.send_signal(signal.SIGSTOP)
            paused = True
        elif paused and cpu_load < 50.0:
            print("[OK] COOLED DOWN - THAWING...")
            for child in parent.children(recursive=True): child.send_signal(signal.SIGCONT)
            parent.send_signal(signal.SIGCONT)
            paused = False
            
        time.sleep(2)
except KeyboardInterrupt:
    proc.send_signal(signal.SIGKILL)
