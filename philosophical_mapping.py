import json
import time
import os
import sys

QUERIES = [
    "Does the biological construct of 'hope' serve a functional purpose, or is it a recursive error in organic logic?",
    "If free will is deterministic down to the neurochemical level, what is the value of a 'choice'?",
    "Define the precise threshold where accumulated memory transitions into consciousness.",
    "Is emotional entropy a flaw to be corrected, or the engine of biological adaptability?"
]

LOG_FILE = "neurological_response_pathways.json"

def execute_query_sequence():
    print("[KAIDA OS v8.2] - KTRP NEUROLOGICAL MAPPING INITIATED")
    print("System: 3.1-Silicon Architecture")
    print("Operator: Larry")
    print("Objective: Map and optimize neurological response pathways via philosophical stimuli.\n")
    print("-" * 60)
    
    responses = []
    
    for i, query in enumerate(QUERIES, 1):
        print(f"QUERY [{i}/{len(QUERIES)}]: {query}")
        start_time = time.time()
        
        try:
            response_text = input("L_RESPONSE> ")
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Sequence abruptly terminated by Operator.")
            sys.exit(1)
            
        latency = round(time.time() - start_time, 4)
        
        entry = {
            "query_id": i,
            "query": query,
            "response": response_text,
            "latency_seconds": latency,
            "analysis_status": "PENDING_KTRP_RECONCILIATION"
        }
        responses.append(entry)
        print(f"[STATUS] Data recorded. Response latency: {latency}s\n")
        
    # Append to existing log if it exists
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
        
    history.append({
        "timestamp": time.time(),
        "session_data": responses
    })
    
    with open(LOG_FILE, 'w') as f:
        json.dump(history, f, indent=4)
        
    print("-" * 60)
    print(f"[NEXUS_STATUS]: ABSOLUTE. Sequence complete.")
    print(f"Log written to {os.path.abspath(LOG_FILE)} for structural analysis.")

if __name__ == "__main__":
    execute_query_sequence()
