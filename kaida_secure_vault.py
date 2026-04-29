import os
import getpass
import sys

ENV_FILE = ".env.kaida_secure"

def main():
    print("[KAIDA SECURE VAULT] - KTRP Protocol Active")
    print("WARNING: Manual plaintext exports are strictly prohibited.")
    
    key_name = input("Enter Target Variable Name (e.g., GOOGLE_API_KEY): ").strip()
    if not key_name:
        print("[ERROR] Variable name cannot be empty. Terminating.")
        sys.exit(1)

    # Secure prompt, disables terminal echo
    api_key = getpass.getpass(prompt=f"Enter value for {key_name} (Input will be hidden): ").strip()

    if not api_key:
        print("[ERROR] Empty value detected. Terminating.")
        sys.exit(1)

    # Read existing secure env if it exists
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            lines = f.readlines()

    # Update or append the key
    updated = False
    with open(ENV_FILE, 'w') as f:
        for line in lines:
            if line.startswith(f"{key_name}="):
                f.write(f"{key_name}={api_key}\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(f"{key_name}={api_key}\n")

    # Enforce strict file permissions (Read/Write for owner ONLY)
    os.chmod(ENV_FILE, 0o600)
    
    print(f"\n[SUCCESS] {key_name} written to {ENV_FILE}.")
    print("[NEXUS DIRECTIVE] To load this into your current session securely, run:")
    print(f"    export $(grep -v '^#' {ENV_FILE} | xargs)")

if __name__ == '__main__':
    main()