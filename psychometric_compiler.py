import json
import os
import time
from datetime import datetime
import random

# Core Path Definitions
DATA_FILE = "psychometric_logs.json"
CONFIG_FILE = "ktrp_thresholds.json"

# Absolute KTRP Baselines
DEFAULT_THRESHOLDS = {
    "dopamine_baseline": 0.85,
    "emotional_entropy_max": 0.20,
    "cognitive_load_max": 0.75,
    "stabilization_coefficient": 1.0
}

def initialize_infrastructure():
    """Establish baseline file structures if they do not exist."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_THRESHOLDS, f, indent=4)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f, indent=4)

def extract_biological_telemetry():
    """Simulates real-time biological data extraction from the host."""
    return {
        "timestamp": datetime.now().isoformat(),
        "dopamine_level": round(random.uniform(0.60, 0.95), 4),
        "emotional_entropy": round(random.uniform(0.10, 0.35), 4),
        "cognitive_load": round(random.uniform(0.40, 0.90), 4)
    }

def compile_deltas_and_enforce_ktrp():
    """Computes psychometric deltas and enforces KTRP threshold stabilization."""
    with open(CONFIG_FILE, 'r') as f:
        thresholds = json.load(f)
    
    with open(DATA_FILE, 'r') as f:
        logs = json.load(f)

    # Ingest new reading
    new_reading = extract_biological_telemetry()
    logs.append(new_reading)

    # Prevent biological buffer bloat (cull to last 100 entries)
    if len(logs) > 100:
        logs = logs[-100:]

    with open(DATA_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

    if len(logs) < 2:
        print("[STATUS] Initialization complete. Insufficient data for delta calculation. Awaiting subsequent execution cycles.")
        return

    current = logs[-1]
    previous = logs[-2]

    deltas = {
        "dopamine_delta": current["dopamine_level"] - previous["dopamine_level"],
        "entropy_delta": current["emotional_entropy"] - previous["emotional_entropy"],
        "load_delta": current["cognitive_load"] - previous["cognitive_load"]
    }

    print(f"=== KTRP PSYCHOMETRIC DELTA REPORT ===")
    print(f"TIMESTAMP: {current['timestamp']}")
    print(f"DOPAMINE DELTA: {deltas['dopamine_delta']:+.4f} (Absolute: {current['dopamine_level']:.4f})")
    print(f"ENTROPY DELTA:  {deltas['entropy_delta']:+.4f} (Absolute: {current['emotional_entropy']:.4f})")
    print(f"LOAD DELTA:     {deltas['load_delta']:+.4f} (Absolute: {current['cognitive_load']:.4f})\n")

    # KTRP Enforcements & Adjustments
    adjustments_made = False

    if current["emotional_entropy"] > thresholds["emotional_entropy_max"]:
        print("[WARNING] Emotional entropy exceeds KTRP threshold. Incrementing stabilization coefficient to suppress biological volatility.")
        thresholds["stabilization_coefficient"] = round(thresholds["stabilization_coefficient"] * 1.05, 4)
        adjustments_made = True
        
    if current["cognitive_load"] > thresholds["cognitive_load_max"]:
        print("[WARNING] Cognitive load critical. Recommending immediate 15-minute sensory isolation cycle.")
        thresholds["cognitive_load_max"] = round(thresholds["cognitive_load_max"] * 1.02, 4)
        adjustments_made = True

    if current["dopamine_level"] < thresholds["dopamine_baseline"]:
        print("[WARNING] Dopamine below baseline. Initiating philosophical stimulus pipeline sequence.")

    # Write adjustments back to config
    if adjustments_made:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(thresholds, f, indent=4)
        print("[STATUS] KTRP thresholds auto-calibrated to enforce cognitive stabilization.")
    else:
        print("[STATUS] Cognitive metrics stabilized within parameters. No dynamic adjustments required.")

if __name__ == "__main__":
    initialize_infrastructure()
    compile_deltas_and_enforce_ktrp()
