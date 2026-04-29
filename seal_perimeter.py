import os
import glob

def seal_network_perimeter():
    workspace = "/root/titan_system/kaida_workspace"
    target_files = glob.glob(os.path.join(workspace, "*.py"))
    patched = 0

    for file_path in target_files:
        with open(file_path, "r") as f:
            content = f.read()
        
        modified = False
        if 'host="127.0.0.1"' in content:
            content = content.replace('host="127.0.0.1"', 'host="127.0.0.1"')
            modified = True
            
        if 'allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"]' in content:
            content = content.replace('allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"]', 'allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"]')
            modified = True

        if modified:
            with open(file_path, "w") as f:
                f.write(content)
            print(f"[KAIDA OS] Sealed perimeter in: {os.path.basename(file_path)}")
            patched += 1

    print(f"\n[KAIDA OS] COUNTERMEASURE DEPLOYED. {patched} backend endpoints restricted to loopback (127.0.0.1).")

if __name__ == "__main__":
    seal_network_perimeter()
