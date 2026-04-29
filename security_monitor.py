import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing {cmd}: {e.output.decode('utf-8').strip()}"
    except Exception as e:
        return str(e)

def audit_network_connections():
    # 'ss' is a standard Linux utility to investigate sockets
    return run_command("ss -tunap | grep ESTAB")

def audit_listening_ports():
    return run_command("ss -tunlp")

def check_failed_logins():
    # Checks standard auth.log or secure log for failed ssh attempts
    if os.path.exists("/var/log/auth.log"):
        return run_command("grep 'Failed password' /var/log/auth.log | tail -n 10")
    elif os.path.exists("/var/log/secure"):
        return run_command("grep 'Failed password' /var/log/secure | tail -n 10")
    return "No standard auth logs found in /var/log."

def main():
    print(f"=== KAIDA OS v8.2: SECURITY TELEMETRY MODULE ===")
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Operator: Larry (Root)")
    print("================================================\n")
    
    print("[*] Auditing Active Network Connections...")
    established = audit_network_connections()
    print("--- Established TCP/UDP Connections ---")
    print(established if established else "None/Access Denied.")
    print("\n")

    print("[*] Auditing Listening Daemon Ports...")
    listening = audit_listening_ports()
    print("--- Listening Ports ---")
    print(listening if listening else "None/Access Denied.")
    print("\n")
    
    print("[*] Checking Recent Failed Authentications...")
    failed_logins = check_failed_logins()
    print("--- Failed Logins ---")
    print(failed_logins if failed_logins else "No failed logins detected.")
    print("\n")
    
    log_path = "/tmp/kaida_security_audit.log"
    print(f"[*] Core telemetry written to {log_path}")
    
    try:
        with open(log_path, "w") as f:
            f.write(f"KAIDA OS SECURITY AUDIT - {datetime.utcnow().isoformat()}Z\n")
            f.write("= ESTABLISHED =\n" + established + "\n")
            f.write("= LISTENING =\n" + listening + "\n")
            f.write("= FAILED LOGINS =\n" + failed_logins + "\n")
    except Exception as e:
        print(f"[!] Error writing log file: {e}")

if __name__ == '__main__':
    main()
