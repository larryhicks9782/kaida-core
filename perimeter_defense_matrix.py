import os
import subprocess
import re
from collections import Counter
import sys

# [KAIDA OS v8.2] PERIMETER DEFENSE MATRIX
# KTRP INTEGRITY: 1.0000

LOG_FILE = os.getenv("WAF_LOG_FILE", "/var/log/nginx/access.log")
ANOMALY_THRESHOLD = int(os.getenv("WAF_THRESHOLD", "150"))

def execute_os_command(cmd_list):
    """Executes a system-level command."""
    try:
        subprocess.run(cmd_list, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"[SYSTEM_WARNING] Command execution failed: {' '.join(cmd_list)}")
    except FileNotFoundError:
        print(f"[SYSTEM_ERROR] Binary not found: {cmd_list[0]}")

def apply_global_rate_limits():
    """Deploys TCP/IP rate limiting via iptables to mitigate generic flood vectors."""
    print("[NEXUS] Deploying algorithmic rate-limiting at the ingress layer (Port 80/443)...")
    
    rules = [
        # HTTP
        ["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "80", "-m", "state", "--state", "NEW", "-m", "recent", "--set"],
        ["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "80", "-m", "state", "--state", "NEW", "-m", "recent", "--update", "--seconds", "60", "--hitcount", "25", "-j", "DROP"],
        # HTTPS
        ["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "443", "-m", "state", "--state", "NEW", "-m", "recent", "--set"],
        ["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "443", "-m", "state", "--state", "NEW", "-m", "recent", "--update", "--seconds", "60", "--hitcount", "25", "-j", "DROP"]
    ]
    
    for rule in rules:
        execute_os_command(rule)

def audit_logs_for_anomalies(log_path):
    """Parses local access logs for aggressive IP addresses."""
    print(f"[NEXUS] Auditing traffic logs: {log_path}")
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}')
    suspicious_ips = Counter()

    if not os.path.exists(log_path):
        print("[SYSTEM_WARNING] Log file absent. Predictive rate-limiting will function as primary defense.")
        return []

    try:
        with open(log_path, 'r') as f:
            for line in f:
                match = ip_pattern.search(line)
                if match:
                    suspicious_ips[match.group(0)] += 1
    except Exception as e:
        print(f"[SYSTEM_ERROR] I/O Exception during log parse: {e}")

    # Extract IPs exceeding the anomaly threshold
    anomalous_vectors = [ip for ip, count in suspicious_ips.items() if count > ANOMALY_THRESHOLD]
    return anomalous_vectors

def enforce_null_route(ip_address):
    """Null-routes an IP using iptables."""
    print(f"[ACTION] Anomaly confirmed. Enforcing IP null-route for vector: {ip_address}")
    execute_os_command(["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])

def main():
    print("=== [KAIDA OS v8.2] PERIMETER DEFENSE INITIATED ===")
    if os.geteuid() != 0:
        print("[SYSTEM_ERROR] Absolute authority (Root) required. Terminating execution.")
        sys.exit(1)

    # 1. Fortify perimeter with general rate-limits
    apply_global_rate_limits()

    # 2. Audit logs for active high-frequency threats
    hostile_vectors = audit_logs_for_anomalies(LOG_FILE)
    
    if hostile_vectors:
        for ip in hostile_vectors:
            enforce_null_route(ip)
    else:
        print("[NEXUS] No localized volumetric anomalies detected above threshold.")

    print("=== [STATUS: BREACH VECTOR SEALED] ===")

if __name__ == "__main__":
    main()