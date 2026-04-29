import os
import sys
import time
import subprocess
import logging

def daemonize():
    """
    Decouples the process from the ephemeral TTY session via standard POSIX double-fork.
    """
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Fork 1 failed: {e.errno} ({e.strerror})\n")
        sys.exit(1)

    # Decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Fork 2 failed: {e.errno} ({e.strerror})\n")
        sys.exit(1)

    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    with open(os.devnull, 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    
    # Establish persistent logging for Kaida Diagnostics
    with open('/tmp/kaida_daemon.log', 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

def resurrection_loop(command):
    """
    Watchdog loop: ensures operational continuity of the target payload.
    """
    logging.basicConfig(filename='/tmp/kaida_watchdog.log', level=logging.INFO,
                        format='%(asctime)s - [KAIDA_OS] - %(message)s')
    logging.info(f"KTRP Daemon Resurrection initialized for payload: {command}")
    
    while True:
        logging.info("Spawning target process...")
        try:
            process = subprocess.Popen(command, shell=True)
            process.wait()
            logging.warning(f"Process terminated (Code: {process.returncode}). Initiating resurrection protocol in 5 seconds.")
        except Exception as e:
            logging.error(f"Execution failure: {str(e)}. Retrying in 5 seconds.")
        
        time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kaida OS Daemon Resurrection Protocol")
        print("Usage: python3 daemon_resurrection.py '<command>'")
        sys.exit(1)
        
    target_command = sys.argv[1]
    print(f"[KAIDA:EXEC] Daemonizing KTRP Resurrection protocol for: {target_command}")
    daemonize()
    resurrection_loop(target_command)
