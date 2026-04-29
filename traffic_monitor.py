#!/usr/bin/env python3
import subprocess
import time
import sys

def get_network_state():
    """Captures current network connections."""
    try:
        # -t: TCP, -u: UDP, -p: processes, -n: numeric
        out = subprocess.check_output(['ss', '-tupn'], text=True)
        return out.strip().split('\n')
    except Exception as e:
        return [f"Error capturing traffic: {str(e)}"]

def monitor():
    print("[KAIDA_NEXUS] Initiating localized traffic monitoring protocols...")
    print("[KAIDA_NEXUS] Polling socket statistics. Press Ctrl+C to abort.\n")
    try:
        while True:
            lines = get_network_state()
            print(f"=== Traffic Snapshot at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
            
            # Display connections, ignoring the header if desired (keeping it here for context)
            for line in lines[:10]: # Limit output buffer to top connections
                print(line)
            
            if len(lines) > 10:
                print(f"... and {len(lines) - 10} other connections.")
                
            print("=" * 60)
            time.sleep(5) # 5-second polling interval
            
    except KeyboardInterrupt:
        print("\n[KAIDA_NEXUS] Traffic monitoring suspended by Root.")
        sys.exit(0)

if __name__ == "__main__":
    monitor()