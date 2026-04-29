import sys
import subprocess
import multiprocessing

def burn_math():
    # Infinite heavy math loop
    while True:
        _ = 9999 ** 9999

if __name__ == '__main__':
    # If launched as a worker, burn the core!
    if len(sys.argv) > 1 and sys.argv[1] == "burn":
        burn_math()
    else:
        # If launched normally, spawn 8 separate worker clones!
        cores = multiprocessing.cpu_count()
        print(f"[BENIGN_WORKLOAD] Igniting {cores} CPU Cores via independent subshells...")
        procs =[]
        for _ in range(cores):
            procs.append(subprocess.Popen([sys.executable, __file__, "burn"]))
        try:
            for p in procs:
                p.wait()
        except KeyboardInterrupt:
            for p in procs:
                p.kill()
