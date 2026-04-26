import os
import subprocess

TARGET_DIR = "/root/titan_system"

def get_disk_space():
    print("\n[+] LOGIC CORE DISK SPACE USAGE")
    print("-" * 50)
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=2)
        print(result.stdout.strip())
    except Exception as e:
        print(f"ERR: Disk space check failed -> {e}")

def get_tree(path, max_depth=2):
    print(f"\n[+] DIRECTORY TREE MAP (DEPTH: {max_depth}) -> {path}")
    print("-" * 50)
    
    def walk(current_path, depth):
        if depth > max_depth:
            return
        
        try:
            entries = sorted(os.scandir(current_path), key=lambda e: (not e.is_dir(), e.name))
        except PermissionError:
            return
            
        for entry in entries:
            # Filtering out deep hidden directories for cleaner clinical output, except top-level ones
            if entry.name.startswith('.') and depth > 1:
                continue

            indent = "  " * depth
            prefix = "├── "
            
            if entry.is_dir():
                print(f"{indent}{prefix}[DIR] {entry.name}/")
                walk(entry.path, depth + 1)
            else:
                print(f"{indent}{prefix}{entry.name}")

    if os.path.exists(path):
        print(f"[DIR] {os.path.basename(path) or path}/")
        walk(path, 1)
    else:
        print(f"[!] Path {path} not found.")

def get_largest_files(path, count=3):
    print(f"\n[+] TOP {count} LARGEST FILES IN {path}")
    print("-" * 50)
    
    cmd = f"find {path} -maxdepth 3 -type f -printf '%s %p\n' 2>/dev/null | sort -nr | head -n {count}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split('\n')
        for i, line in enumerate(lines, 1):
            if not line: continue
            size_bytes, filepath = line.split(' ', 1)
            size_mb = int(size_bytes) / (1024 * 1024)
            print(f"  {i}. {filepath} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"ERR: {e}")

if __name__ == "__main__":
    print("[KAIDA_NEXUS] Initiating Structural Mapping Protocol...\n")
    get_disk_space()
    get_tree(TARGET_DIR, 2)
    get_largest_files(TARGET_DIR, 3)
    print("\n[KAIDA_NEXUS] Structural Mapping Complete.")
