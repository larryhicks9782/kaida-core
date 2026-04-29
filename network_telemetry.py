import subprocess
import sys

def get_network_telemetry():
    print("[KAIDA NETWORK TELEMETRY]")
    print("-" * 60)
    
    commands = [
        ["ss", "-tunalp"],
        ["netstat", "-tunalp"],
        ["lsof", "-Pni"]
    ]
    
    output = ""
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stdout.strip():
                output = result.stdout
                print(f"[STATUS]: Succeeded with '{cmd[0]}'")
                break
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            print(f"[WARN]: Command '{cmd[0]}' failed or restricted. ({e})")
            continue
    
    if output:
        lines = output.split('\n')
        found_active = False
        for line in lines:
            if "LISTEN" in line or "ESTAB" in line or "ESTABLISHED" in line:
                print(line.strip())
                found_active = True
                
        if not found_active:
            print("[STATUS]: No active LISTEN or ESTABLISHED ports detected directly.")
    else:
        print("[KAIDA_ERROR]: Kernel-level Android restrictions are blocking direct socket mapping (Permission denied to /proc/net/tcp & AF_INET).")
        print("[FALLBACK]: Scanning process tree for known network-bound daemons...")
        
        try:
            ps_result = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
            for line in ps_result.stdout.split('\n'):
                if "uvicorn" in line or "fastapi" in line or "python" in line:
                    if "network_telemetry.py" not in line:
                        print(f"NETWORK_PROCESS_DETECTED: {line.strip()}")
        except Exception as e:
            print(f"Process scan failed: {e}")
            
    print("-" * 60)

if __name__ == "__main__":
    get_network_telemetry()
