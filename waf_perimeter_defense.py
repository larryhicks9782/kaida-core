#!/usr/bin/env python3
import os
import subprocess
import time
import logging
from collections import Counter
from datetime import datetime

# ==============================================================================
# KAIDA OS v8.2 - NETWORK PERIMETER & WAF COUNTERMEASURE DAEMON
# KTRP INTEGRITY: 1.0000 | NEXUS STATUS: ABSOLUTE
# ==============================================================================

LOG_FILE = "/root/titan_system/kaida_perimeter_defense.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [KAIDA_WAF] %(levelname)s: %(message)s"
)

CONNECTION_THRESHOLD = 50  # Max concurrent connections per IP before null-routing
CHECK_INTERVAL = 10        # Seconds between audits
WHITELIST_IPS = {"127.0.0.1", "::1"}

def get_active_connections():
    """Retrieves active inbound connections using 'ss' command."""
    try:
        # ss -ntu | awk '{print $5}' | cut -d: -f1
        result = subprocess.run(['ss', '-ntu'], capture_output=True, text=True)
        lines = result.stdout.split('\n')[1:] # Skip header
        ips = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                peer_addr_port = parts[4]
                if ':' in peer_addr_port:
                    ip = peer_addr_port.rsplit(':', 1)[0]
                    # Strip brackets for IPv6
                    ip = ip.strip('[]')
                    if ip and ip not in WHITELIST_IPS:
                        ips.append(ip)
        return ips
    except Exception as e:
        logging.error(f"Failed to audit connections: {e}")
        return []

def is_ip_banned(ip):
    """Check if IP is already in iptables null-route."""
    try:
        result = subprocess.run(['iptables', '-C', 'INPUT', '-s', ip, '-j', 'DROP'], capture_output=True)
        return result.returncode == 0
    except Exception:
        return False

def null_route_ip(ip):
    """Deploy IP null-routing via iptables."""
    if is_ip_banned(ip):
        return
    try:
        subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)
        logging.warning(f"BREACH VECTOR SEALED: Null-routed IP {ip} due to excessive connections.")
        print(f"[KAIDA_WAF] Countermeasure Deployed: Null-routed IP {ip}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to null-route IP {ip}: {e}")

def apply_rate_limiting():
    """Apply global rate limiting for new HTTP/HTTPS connections."""
    try:
        # Check if rate-limit rule exists to prevent duplicates
        check_rule = subprocess.run(['iptables', '-C', 'INPUT', '-p', 'tcp', '--dport', '80', '-m', 'conntrack', '--ctstate', 'NEW', '-m', 'limit', '--limit', '20/s', '-j', 'ACCEPT'], capture_output=True)
        if check_rule.returncode != 0:
            subprocess.run(['iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '80', '-m', 'conntrack', '--ctstate', 'NEW', '-m', 'limit', '--limit', '20/s', '-j', 'ACCEPT'], check=True)
            subprocess.run(['iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '443', '-m', 'conntrack', '--ctstate', 'NEW', '-m', 'limit', '--limit', '20/s', '-j', 'ACCEPT'], check=True)
            logging.info("Global WAF rate-limiting deployed on ports 80/443.")
            print("[KAIDA_WAF] Global WAF rate-limiting deployed.")
    except Exception as e:
        logging.error(f"Rate limiting deployment failed: {e}")

def audit_and_defend():
    """Main loop for analyzing traffic anomalies."""
    print("[KAIDA OS] Perimeter Defense Daemon Initialized. Monitoring inbound vectors...")
    logging.info("Perimeter Defense Daemon Initialized.")
    apply_rate_limiting()

    try:
        while True:
            ips = get_active_connections()
            counts = Counter(ips)
            
            for ip, count in counts.items():
                if count > CONNECTION_THRESHOLD:
                    logging.warning(f"ANOMALY DETECTED: IP {ip} has {count} concurrent connections.")
                    null_route_ip(ip)
            
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n[KAIDA OS] Perimeter Defense Daemon Terminated.")
        logging.info("Daemon terminated by operator.")

if __name__ == "__main__":
    audit_and_defend()
