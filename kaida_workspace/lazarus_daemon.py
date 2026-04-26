import json
import time
import subprocess
import os
import sys

CONFIG_FILE = "lazarus_config.json"

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def is_running(script_name):
    try:
        # Check running processes
        output = subprocess.check_output(["pgrep", "-f", script_name])
        pids = output.decode().strip().split('\n')
        # Ensure we don't just count an empty string or the grep itself if we used ps
        return len([p for p in pids if p.isdigit()]) > 0
    except subprocess.CalledProcessError:
        # pgrep returns non-zero if no processes matched
        return False

def main():
    print(f"[LAZARUS] Daemon initiated. PID: {os.getpid()}")
    sys.stdout.flush()
    while True:
        try:
            config = load_config()
            target = config.get("target_script")
            interval = config.get("check_interval", 5)

            if target and not is_running(target):
                print(f"[LAZARUS] Target '{target}' is DOWN. Initiating resurrection...")
                sys.stdout.flush()
                # Run the target process detached
                subprocess.Popen([sys.executable, target])
                print(f"[LAZARUS] Target '{target}' successfully resurrected.")
                sys.stdout.flush()
        except Exception as e:
            print(f"[LAZARUS] Error: {e}")
            sys.stdout.flush()
        
        time.sleep(interval)

if __name__ == "__main__":
    main()