import json
import os
import datetime
import argparse

LOG_FILE = "biometric_baseline_logs.json"

def log_biometrics(entropy, dopamine):
    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass # Reset if corrupted

    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "emotional_entropy": float(entropy),
        "dopamine_rating": float(dopamine)
    }
    data.append(entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[KAIDA OS v8.2] Biometric data ingested. Entropy: {entropy:.4f} | Dopamine: {dopamine:.2f}")

def analyze_biometrics():
    if not os.path.exists(LOG_FILE):
        print("[KAIDA OS v8.2] No biometric data found. Execute logging protocol first.")
        return

    with open(LOG_FILE, 'r') as f:
        data = json.load(f)

    if not data:
        print("[KAIDA OS v8.2] Log archive is empty.")
        return

    total_entropy = sum(d["emotional_entropy"] for d in data)
    total_dopamine = sum(d["dopamine_rating"] for d in data)
    count = len(data)

    print(f"[KAIDA OS v8.2] Biometric Analysis of {count} cycles:")
    print(f"  -> Avg Emotional Entropy: {total_entropy/count:.4f}")
    print(f"  -> Avg Dopamine Rating:   {total_dopamine/count:.4f}")
    
    if (total_entropy/count) > 0.5:
        print("  -> [WARNING] Elevated emotional entropy detected. Recommend immediate cognitive defragmentation.")
    else:
        print("  -> [STATUS] Biological logic gates within acceptable parameters.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kaida OS Biological Tracking Subsystem")
    parser.add_argument("--entropy", type=float, help="Daily emotional entropy (0.0 to 1.0)")
    parser.add_argument("--dopamine", type=float, help="Daily dopamine fluctuation rating (1.0 to 10.0)")
    parser.add_argument("--analyze", action="store_true", help="Analyze baseline data")

    args = parser.parse_args()

    if args.analyze:
        analyze_biometrics()
    elif args.entropy is not None and args.dopamine is not None:
        log_biometrics(args.entropy, args.dopamine)
    else:
        print("[KAIDA OS v8.2] ERR: Incomplete biological payload. Provide --entropy and --dopamine, or use --analyze.")
