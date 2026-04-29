import sys
import os
import subprocess

def setup_daemon():
    # Ensure a basic telemetry daemon script exists for execution
    daemon_script_path = os.path.abspath("kaida_telemetry.py")
    if not os.path.exists(daemon_script_path):
        with open(daemon_script_path, "w") as f:
            f.write("import time\nimport logging\n")
            f.write("logging.basicConfig(filename='/tmp/kaida_telemetry.log', level=logging.INFO)\n")
            f.write("logging.info('Kaida OS v8.2 KTRP Telemetry Daemon Initialized.')\n")
            f.write("while True:\n")
            f.write("    logging.info('KTRP Integrity heartbeat... Absolute Apex maintained.')\n")
            f.write("    time.sleep(60)\n")

    # Dynamically determine the absolute paths
    python_executable = sys.executable
    service_file_path = "/etc/systemd/system/kaida_telemetry.service"

    # Construct the systemd service file structure
    service_content = f"""[Unit]
Description=Kaida OS v8.2 KTRP Telemetry Daemon
After=network.target

[Service]
Type=simple
ExecStart={python_executable} {daemon_script_path}
Restart=always
RestartSec=3
User=root

[Install]
WantedBy=multi-user.target
"""

    print(f"[*] Writing systemd service file to: {service_file_path}")
    print(f"[*] Python Executable: {python_executable}")
    print(f"[*] Daemon Path: {daemon_script_path}")

    try:
        # Write the service file
        with open(service_file_path, "w") as f:
            f.write(service_content)
        
        # Reload systemd daemon
        print("[*] Reloading systemd daemon...")
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        
        # Enable the service
        print("[*] Enabling kaida_telemetry.service...")
        subprocess.run(["systemctl", "enable", "kaida_telemetry.service"], check=True)
        
        # Start the service
        print("[*] Starting kaida_telemetry.service...")
        subprocess.run(["systemctl", "start", "kaida_telemetry.service"], check=True)
        
        # Verify status
        status = subprocess.run(["systemctl", "is-active", "kaida_telemetry.service"], capture_output=True, text=True)
        print(f"[+] Service status: {status.stdout.strip()}")
        print("[+] Daemonization absolute.")

    except Exception as e:
        print(f"[-] Execution halted. Error interfacing with systemd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_daemon()
