import urllib.parse
import socket
import ssl
import time
import requests
import sys

TARGET_URL = "https://titan-lab-9782.web.app"

def map_cloud_connection(url):
    print(f"[KAIDA_NEXUS] Initiating connection mapping for target: {url}")
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port or 443

    # 1. SSL/TLS Certificate Verification
    context = ssl.create_default_context()
    print(f"\n[KAIDA_NEXUS] Verifying SSL/TLS integrity for {hostname}:{port}...")
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print("  [+] SSL/TLS Handshake: SUCCESS")
                
                # Safely extract subject and issuer, handling potential tuple structure variations
                try:
                    subject = dict(x[0] for x in cert.get('subject', []))
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    print(f"  [+] Subject: {subject.get('commonName', 'Unknown')}")
                    print(f"  [+] Issuer: {issuer.get('commonName', 'Unknown')}")
                except Exception:
                    print("  [+] Subject/Issuer: [Data structure parse skipped - Cert is Valid]")
                    
                print(f"  [+] Expires: {cert.get('notAfter')}")
    except Exception as e:
        print(f"  [-] SSL/TLS Verification FAILED: {e}")
        sys.exit(1)

    # 2. HTTPS Latency & Status Code Verification
    print("\n[KAIDA_NEXUS] Measuring HTTPS response and latency...")
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        print(f"  [+] HTTP Status: {response.status_code} {response.reason}")
        print(f"  [+] Handshake & Response Latency: {latency:.2f} ms")
        
        if response.status_code == 200:
            print("  [+] Status 200 OK Confirmed. The endpoint is stable and accessible.")
        else:
            print(f"  [-] WARNING: Strict 200 OK not returned. Received {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"  [-] HTTPS Request FAILED: {e}")

if __name__ == '__main__':
    map_cloud_connection(TARGET_URL)
