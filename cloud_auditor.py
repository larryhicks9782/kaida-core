import os
import requests
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

# Kaida OS v8.2 - Cloud Storage Exposure Auditor
# Perimeter Defense Subroutine 0x02

def check_bucket_access(bucket_name, platform):
    """
    Checks common unauthenticated access endpoints for cloud buckets.
    """
    endpoints = {
        "gcp": [
            f"https://storage.googleapis.com/{bucket_name}",
            f"https://www.googleapis.com/storage/v1/b/{bucket_name}/o"
        ],
        "aws": [
            f"http://{bucket_name}.s3.amazonaws.com/",
            f"https://{bucket_name}.s3.amazonaws.com/"
        ],
        "firebase": [
            f"https://{bucket_name}.firebaseio.com/.json"
        ]
    }
    
    if platform not in endpoints:
        return
        
    for url in endpoints[platform]:
        try:
            response = requests.get(url, timeout=5)
            # 200 OK means unauthenticated access is allowed
            if response.status_code == 200:
                print(f"[CRITICAL] Public Exposure Detected: {url}")
                return True
            # 403 Forbidden is what we want
            elif response.status_code == 403:
                print(f"[SECURE] Access Denied: {url}")
            # 404 Not Found
            elif response.status_code == 404:
                print(f"[INFO] Bucket/Entity not found: {url}")
            else:
                 print(f"[WARN] Unexpected status {response.status_code}: {url}")
        except requests.exceptions.RequestException as e:
            print(f"[!] K-ERR: Connection failed for {url} - {e}")
    return False

def scan_buckets(bucket_list, platform):
    print(f"\n[K-SYS] Initiating Public Exposure Audit for {platform.upper()} Targets...")
    exposed = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(lambda b: check_bucket_access(b, platform), bucket_list)
        for r in results:
            if r: exposed += 1
            
    print(f"[K-SYS] {platform.upper()} Audit Complete. Critical Exposures: {exposed}")
    return exposed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kaida OS Perimeter Security: Cloud Bucket Auditor")
    parser.add_argument("-b", "--buckets", required=True, help="Comma-separated list of bucket names to check")
    parser.add_argument("-p", "--platform", choices=['gcp', 'aws', 'firebase'], required=True, help="Target cloud platform")
    
    args = parser.parse_args()
    buckets = [b.strip() for b in args.buckets.split(",")]
    
    exposed_count = scan_buckets(buckets, args.platform)
    if exposed_count > 0:
         print("[K-SYS] DIRECTIVE: Modify IAM/Bucket policies immediately to block public access.")
         sys.exit(1)
    else:
         print("[K-SYS] Perimeter verified. No public exposures detected in target list.")
         sys.exit(0)