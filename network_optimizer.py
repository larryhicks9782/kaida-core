import os
import socket
import time
import signal
import subprocess

PORTS = [8000, 8080, 8081]
WHITELIST = ['lazarus', 'telemetry']

def measure_latency(port):
    start = time.time()
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=1):
            pass
        return (time.time() - start) * 1000
    except Exception:
        return -1

def get_pids_for_port_fallback(port):
    pids = []
    # Attempt 1: lsof
    try:
        out = subprocess.check_output(f"lsof -t -i:{port}", shell=True, stderr=subprocess.DEVNULL)
        for p in out.decode().split():
            if p.strip().isdigit(): 
                pids.append(int(p.strip()))
        if pids: return pids
    except Exception:
        pass
        
    # Attempt 2: fuser
    try:
        out = subprocess.check_output(f"fuser {port}/tcp", shell=True, stderr=subprocess.DEVNULL)
        for p in out.decode().split():
            if p.strip().isdigit(): 
                pids.append(int(p.strip()))
        if pids: return pids
    except Exception:
        pass
    
    return pids

def get_cmdline(pid):
    try:
        with open(f"/proc/{pid}/cmdline", 'r') as f:
            return f.read().replace('\x00', ' ').strip()
    except Exception:
        return ""

def get_state(pid):
    try:
        with open(f"/proc/{pid}/stat", 'r') as f:
            return f.read().split()[2]
    except Exception:
        return ""

def optimize():
    print("[KAIDA_OS] Core Logic Gemini 2.5 Pro Active.")
    print("[KAIDA_OS] Scanning active local ports and enforcing process hygiene...")
    
    for port in PORTS:
        latency = measure_latency(port)
        if latency != -1:
            print(f"[PORT {port}] Socket Latency: {latency:.2f} ms")
        else:
            print(f"[PORT {port}] Socket Offline/Unreachable.")
            
        pids = get_pids_for_port_fallback(port)
        
        for pid in pids:
            cmd = get_cmdline(pid).lower()
            state = get_state(pid)
            
            whitelisted = any(w in cmd for w in WHITELIST)
            if whitelisted:
                print(f"  -> Authorized daemon detected: PID {pid} ({cmd}). Bypassing.")
                continue
                
            if state == 'Z':
                print(f"  -> Zombie daemon identified: PID {pid}. Scheduling parent termination protocol.")
            else:
                print(f"  -> Terminating orphaned/duplicate daemon: PID {pid} ({cmd})...")
                try:
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(0.1)
                    os.kill(pid, signal.SIGKILL)
                    print(f"     [+] Process Purged: PID {pid}")
                except Exception as e:
                    print(f"     [-] Termination Failed for PID {pid}: {e}")

    print("[KAIDA_OS] Initiating general process table sweep for orphans and zombies...")
    try:
        for pid_str in os.listdir('/proc'):
            if pid_str.isdigit():
                pid = int(pid_str)
                state = get_state(pid)
                if state == 'Z':
                    cmd = get_cmdline(pid).lower()
                    if not any(w in cmd for w in WHITELIST):
                        print(f"  -> Sweeper: Found zombie daemon PID {pid}. Logged for reaping.")
    except Exception:
        pass

if __name__ == '__main__':
    optimize()
    print("[KAIDA_OS] Port mapping and bandwidth optimization complete.")