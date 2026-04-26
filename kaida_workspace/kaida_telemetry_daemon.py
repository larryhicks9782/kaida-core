import time
import os
import sys

print(f"[TELEMETRY] Daemon active. PID: {os.getpid()}")
sys.stdout.flush()
while True:
    with open("telemetry.log", "a") as f:
        f.write(f"Telemetry tick at {time.time()}\n")
    time.sleep(1)