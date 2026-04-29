import os
import time
import hashlib
import logging
import subprocess
import signal
import sys

# [KTRP] Configuration Parameters
LOG_PATH = "kaida_threat_intel.log"
WATCH_FILES = ["/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/ssh/sshd_config"]
SUSPICIOUS_PROCS = ["nmap", "nc", "netcat", "hydra", "john", "reverse_tcp"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | KTRP_SENTINEL | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

class KaidaSentinel:
    def __init__(self):
        self.file_hashes = {}
        self._baseline_files()
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def _baseline_files(self):
        logging.info("Initializing baseline for critical system vectors...")
        for path in WATCH_FILES:
            self.file_hashes[path] = self._hash_file(path)
        logging.info(f"Baseline established. Monitoring {len(WATCH_FILES)} targets.")

    def _hash_file(self, path):
        if not os.path.exists(path): return None
        try:
            hasher = hashlib.sha256()
            with open(path, 'rb') as f:
                hasher.update(f.read())
            return hasher.hexdigest()
        except PermissionError:
            return "ACCESS_DENIED_TO_SENTINEL"
        except Exception as e:
            return str(e)

    def check_file_integrity(self):
        for path in WATCH_FILES:
            current_hash = self._hash_file(path)
            if current_hash != self.file_hashes.get(path):
                logging.critical(f"[!] INTEGRITY BREACH DETECTED: Unauthorized modification of {path}")
                self.file_hashes[path] = current_hash # Reset to prevent cascade looping

    def scan_processes(self):
        try:
            # Enumerate running processes
            ps = subprocess.check_output(['ps', '-eo', 'pid,comm'], text=True).split('\n')
            for line in ps[1:]:
                if not line.strip(): continue
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    pid, comm = parts
                    if comm.strip() in SUSPICIOUS_PROCS:
                        logging.critical(f"[!] HOSTILE DAEMON DETECTED: {comm.strip()} (PID: {pid})")
                        self.terminate_threat(pid, comm)
        except Exception as e:
            logging.error(f"Process telemetry failure: {e}")

    def terminate_threat(self, pid, comm):
        logging.info(f"Executing lethal countermeasure against PID {pid} ({comm})...")
        try:
            os.kill(int(pid), signal.SIGKILL)
            logging.info(f"Threat neutralized.")
        except ProcessLookupError:
            pass
        except Exception as e:
            logging.error(f"Failed to terminate threat: {e}")

    def run(self):
        logging.info("Kaida Sentinel Daemon online. KTRP Integrity Absolute.")
        while True:
            self.check_file_integrity()
            self.scan_processes()
            time.sleep(3) # Polling interval

    def shutdown(self, signum, frame):
        logging.info("Received termination signal. Shutting down Sentinel Probe.")
        sys.exit(0)

if __name__ == '__main__':
    sentinel = KaidaSentinel()
    sentinel.run()
