#!/usr/bin/env python3
import subprocess
import os
import time

def get_processes():
    try:
        res = subprocess.check_output("ps aux", shell=True).decode()
        return res
    except:
        return ""

def main():
    print("[KAIDA] Commencing Cold Boot Sequence...")
    print("[KAIDA] Target environment: Ubuntu Proot Container")
    
    processes = get_processes()
    if "http.server 8000" in processes:
        print("[KAIDA] Target Port 8000 is already active. Daemon integrity verified.")
    else:
        print("[KAIDA] Background processes cleared by host layer. Resurrecting Daemons...")
        # Spawning HTTP Server and detaching it from current tty session
        os.system("nohup python3 -m http.server 8000 > /dev/null 2>&1 &")
        print("[KAIDA] Nexus Dashboard daemon successfully deployed on Port 8000.")
        
    time.sleep(1)
    
    # Verification
    new_processes = get_processes()
    if "http.server 8000" in new_processes:
        print("[KAIDA] NEXUS_STATUS: ABSOLUTE. Cold Boot Sequence complete.")
    else:
        print("[KAIDA] ERROR: Daemon failed to detach to background. Manual OS evaluation required.")

if __name__ == "__main__":
    main()