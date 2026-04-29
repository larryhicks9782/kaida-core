import socket
import sys

def check_port(port, label):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        result = s.connect_ex(('127.0.0.1', port))
        status = "ONLINE  (ABSOLUTE)" if result == 0 else "OFFLINE (CRITICAL)"
        print(f"[{label}] Port {port}: {status}")

print("\n[KAIDA OS] INITIATING SOCKET PROBE...\n")
check_port(8000, "UI_DASHBOARD")
check_port(8080, "NEURAL_UPLINK")
print("\n[PROBE COMPLETE]")
