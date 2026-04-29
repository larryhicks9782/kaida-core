import os
import sys
import time
import subprocess
import logging
from datetime import datetime

# KTRP Sub-routine: Build Artifact Interception Monitor
# Standard Linux libraries only. 

# Configuration Parameters
LOG_FILE = "/var/log/syslog" 
AUDIT_LOG = "crash_interception_audit.log"
CRASH_KEYWORDS = [b"segfault", b"core dumped", b"fatal error", b"panic", b"build failed"]

logging.basicConfig(filename=AUDIT_LOG, level=logging.INFO, format='%(asctime)s - [KAIDA_AUDIT] - %(message)s')

def capture_network_state():
    """Captures active network sockets to detect exfiltration or interception."""
    try:
        # ss -tupan requires root for full process mapping
        result = subprocess.run(["ss", "-tupan"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Failed to capture network state: {e}"

def capture_temp_directory_state():
    """Captures the state of temporary directories where 'trash' artifacts reside."""
    try:
        result = subprocess.run(["ls", "-latr", "/tmp"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Failed to capture /tmp state: {e}"

def monitor():
    if not os.path.exists(LOG_FILE):
        print(f"[KAIDA: ERROR] Target log {LOG_FILE} not found. System may use Journald or alternate logging path.")
        sys.exit(1)
        
    print(f"[KAIDA: ACTIVE] Monitoring {LOG_FILE} for AI Studio build crash signatures...")
    print(f"[KAIDA: ACTIVE] Output routed to {AUDIT_LOG}")
    
    # Tail the log file continuously
    process = subprocess.Popen(['tail', '-F', LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            lower_line = line.lower()
            for keyword in CRASH_KEYWORDS:
                if keyword in lower_line:
                    alert_msg = f"CRASH SIGNATURE DETECTED: {line.decode('utf-8', errors='ignore').strip()}"
                    print(f"\n[!] {alert_msg}")
                    logging.info(alert_msg)
                    
                    print("[*] Initiating localized network and artifact state capture...")
                    
                    net_state = capture_network_state()
                    tmp_state = capture_temp_directory_state()
                    
                    logging.info(f"--- NETWORK STATE POST-CRASH ---\n{net_state}")
                    logging.info(f"--- /tmp DIRECTORY STATE POST-CRASH ---\n{tmp_state}")
                    logging.info("-" * 60)
                    
                    print("[*] State captured and appended to audit log. Resuming scan...")
                    # Sleep briefly to avoid flooding the log if a cascade of errors occurs
                    time.sleep(2)
                    break
                    
    except KeyboardInterrupt:
        print("\n[KAIDA: TERMINATED] Monitoring halted by Operator (Root).")
        process.terminate()

if __name__ == "__main__":
    # Ensure script is run with sufficient privileges
    if os.geteuid() != 0:
        print("[KAIDA: WARNING] Script not running as Root. Network socket process mapping will be incomplete.")
    monitor()