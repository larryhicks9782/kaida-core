import os
import getpass

ENV_FILE = os.path.join(os.getcwd(), ".env")

def update_env(key_name: str) -> None:
    print(f"[KAIDA OS] Secure Credential Input Initialized for: {key_name}")
    print("[KAIDA OS] Keystrokes will be masked to prevent visual and clipboard leaks.")
    
    # getpass prevents terminal echo, mitigating shoulder-surfing and accidental pasting
    api_key = getpass.getpass(prompt=f"Enter {key_name}: ")

    if not api_key.strip():
        print("[ERROR] Empty credential provided. Protocol aborted.")
        return

    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()

    updated = False
    with open(ENV_FILE, "w") as f:
        for line in lines:
            if line.startswith(f"{key_name}="):
                f.write(f"{key_name}={api_key}\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(f"{key_name}={api_key}\n")

    # Change permissions to user-read/write only for security
    os.chmod(ENV_FILE, 0o600)
    print(f"[SUCCESS] {key_name} securely written to {ENV_FILE}. Buffer flushed. Permissions restricted.")

if __name__ == "__main__":
    update_env("GEMINI_API_KEY")
