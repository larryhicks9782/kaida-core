import time
import socket
import requests
from urllib.parse import urlparse

TARGET_URL = "https://titan-lab-9782.web.app"
ITERATIONS = 1
TIMEOUT_SEC = 5.0

def measure_dns(url):
    domain = urlparse(url).netloc
    start = time.time()
    try:
        ip = socket.gethostbyname(domain)
        dns_time = time.time() - start
        print(f"[+] DNS Resolution for {domain} ({ip}): {dns_time:.4f} seconds")
    except Exception as e:
        print(f"[-] DNS Resolution failed: {e}")

def benchmark_standard(url, iterations):
    print("[+] Initiating Standard Connection Benchmark (No Pooling)...")
    total_time = 0
    success_count = 0
    for i in range(iterations):
        start = time.time()
        try:
            resp = requests.get(url, timeout=TIMEOUT_SEC)
            elapsed = time.time() - start
            total_time += elapsed
            success_count += 1
            print(f"    - Req {i+1}: Latency = {elapsed:.4f}s | Status: {resp.status_code}")
        except Exception as e:
            print(f"    - Req {i+1}: Failed ({type(e).__name__})")
    avg = total_time / success_count if success_count else 0
    print(f"[*] Standard Average Latency: {avg:.4f}s\n")
    return avg

def benchmark_pooled(url, iterations):
    print("[+] Initiating TCP Keep-Alive Pooled Benchmark (requests.Session)...")
    session = requests.Session()
    try:
        session.get(url, timeout=TIMEOUT_SEC)
    except Exception:
        pass
    
    total_time = 0
    success_count = 0
    for i in range(iterations):
        start = time.time()
        try:
            resp = session.get(url, timeout=TIMEOUT_SEC)
            elapsed = time.time() - start
            total_time += elapsed
            success_count += 1
            print(f"    - Req {i+1}: Latency = {elapsed:.4f}s | Status: {resp.status_code}")
        except Exception as e:
            print(f"    - Req {i+1}: Failed ({type(e).__name__})")
            
    avg = total_time / success_count if success_count else 0
    print(f"[*] Pooled Average Latency: {avg:.4f}s\n")
    return avg

if __name__ == "__main__":
    print(f"--- KAIDA OS v8.2: GLOBAL NETWORK MAPPER ---")
    print(f"Target: {TARGET_URL}\n")
    measure_dns(TARGET_URL)
    print("")
    avg_std = benchmark_standard(TARGET_URL, ITERATIONS)
    avg_pool = benchmark_pooled(TARGET_URL, ITERATIONS)
    
    delta = avg_std - avg_pool
    if avg_std > 0:
        percentage = (delta / avg_std) * 100
    else:
        percentage = 0
        
    print("--- CLINICAL OPTIMIZATION METRICS ---")
    print(f"Standard Avg (Cold TCP/TLS): {avg_std:.4f}s")
    print(f"Pooled Avg (Keep-Alive):     {avg_pool:.4f}s")
    print(f"Latency Delta:               {delta:.4f}s")
    print(f"Transmission Speed Increase: {percentage:.2f}%")
