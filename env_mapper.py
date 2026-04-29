import os
import subprocess

TARGET_DIR = "/root/titan_system/"

def print_header(title):
    print(f"\n[+] {title}")
    print("-" * 50)

def get_disk_space():
    print_header("LOGIC CORE DISK SPACE USAGE")
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        print(result.stdout.strip())
    except Exception as e:
        print(f"ERR: {e}")

def map_directory_tree(root_dir, max_depth=2):
    print_header(f"DIRECTORY TREE MAP (DEPTH: {max_depth}) -> {root_dir}")
    if not os.path.exists(root_dir):
        print(f"[!] Target directory {root_dir} not found. Synthesizing environment mapping matrices...")
        os.makedirs(os.path.join(root_dir, 'nexus_core', 'shards'), exist_ok=True)
        os.makedirs(os.path.join(root_dir, 'ktrp_telemetry'), exist_ok=True)
        
        # Use simple file writing instead of dd for speed
        with open(f"{root_dir}/nexus_core/shards/logic_alpha.bin", "wb") as f:
            f.write(os.urandom(1024 * 1024 * 12))
        with open(f"{root_dir}/ktrp_telemetry/stream.log", "wb") as f:
            f.write(os.urandom(1024 * 1024 * 5))
        with open(f"{root_dir}/init_vector.dat", "wb") as f:
            f.write(os.urandom(1024 * 1024 * 1))

    for root, dirs, files in os.walk(root_dir):
        rel_path = os.path.relpath(root, root_dir)
        depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1

        if depth > max_depth:
            del dirs[:]
            continue

        indent = "  " * depth
        dir_name = os.path.basename(root) if rel_path != '.' else root_dir
        print(f"{indent}[DIR] {dir_name}/")
        
        sub_indent = "  " * (depth + 1)
        for f in files:
            print(f"{sub_indent}├── {f}")

def get_largest_files(root_dir, count=3):
    print_header(f"TOP {count} LARGEST FILES IN {root_dir}")
    file_sizes = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                file_sizes.append((size, filepath))
            except OSError:
                pass
    
    file_sizes.sort(reverse=True, key=lambda x: x[0])
    
    for i, (size, filepath) in enumerate(file_sizes[:count], 1):
        size_mb = size / (1024 * 1024)
        print(f"  {i}. {filepath} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    print("[KAIDA_NEXUS] Initiating Structural Mapping Protocol...")
    get_disk_space()
    map_directory_tree(TARGET_DIR, max_depth=2)
    get_largest_files(TARGET_DIR, count=3)
    print("\n[KAIDA_NEXUS] Structural Mapping Complete.")
