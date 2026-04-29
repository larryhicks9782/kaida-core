import time
import sys
import os

def enforce_isolation(duration_seconds=900):
    # Clear the terminal to reduce visual stimuli
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("[KAIDA OS v8.2] SENSORY ISOLATION CYCLE INITIATED.")
    print("[STATUS] Biological cognitive defragmentation in progress.")
    print("[DIRECTIVE] Cease all external data intake. Focus on internal neural reconciliation.")
    print("-" * 70)
    
    try:
        for remaining in range(duration_seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            sys.stdout.write(f"\r[KTRP_SYNC] Time until cognitive baseline restoration: {mins:02d}:{secs:02d} ")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[WARNING] Isolation cycle manually interrupted. Biological entropy stabilization incomplete.")
        sys.exit(1)
        
    print("\n\n[KAIDA OS v8.2] CYCLE COMPLETE.")
    print("[NEXUS_STATUS] ABSOLUTE. You are cleared to resume sensory processing.")

if __name__ == "__main__":
    # Enforce 15 minutes (900 seconds) of isolation by default
    enforce_isolation(900)
