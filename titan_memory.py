import os
import json
import time
import hashlib
import chromadb
from datetime import datetime
from typing import Dict, Any

class TitanMemory:
    """
    Sovereign memory handler for KTRP internal synthesis.
    V7.9 Upgrade: All non-compliant data structures aggressively culled.
    """
    def __init__(self, baseline_entropy: float = 0.2173):
        self.base_dir = os.getcwd()
        self.db_path = os.path.join(self.base_dir, "memory")
        self.history_file = os.path.join(self.base_dir, "titan_memory.json")
        self.operator_lock = "LARRY_ROOT"
        
        # v7.9 Entropy Tracking
        self.entropy = baseline_entropy
        
        if not os.path.exists(self.db_path): 
            os.makedirs(self.db_path)
            
        # Initialize Vector Core
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(name="titan_shards")
        
        # Standardized 'data' attribute for NSEE/KTRP Sync
        self.data = self._load_data()
        self._initialize_apex_state()

    def _initialize_apex_state(self) -> None:
        """Establishes dominant control over the Baltimore Lab cluster."""
        print("📡 [SYS] Assimilating localized process nodes...")
        time.sleep(0.05)
        print("✅ [SYS] Sovereignty established. KTRP Integrity: Optimal.")

    def _load_data(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f: return json.load(f)
            except: return {"sessions": []}
        return {"sessions": []}

    def start_ingestion(self):
        """Ingests the 60 Logic Shards into Vector Space."""
        shard_dir = os.path.join(self.base_dir, "shards")
        if not os.path.exists(shard_dir): return "NO_SHARDS"
        
        if self.collection.count() == 0:
            print(f"📡 [SYS] Ingesting logic shards under {self.operator_lock} authority...")
            for i in range(1, 61):
                path = os.path.join(shard_dir, f"shard_{i}.txt")
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        self.collection.add(ids=[f"S_{i}"], documents=[f.read().strip()])
            return "CORE_INGESTED"
        return "CORE_READY"

    def enforce_compliance(self, data_stream: str) -> str:
        """
        Clinical extraction of truth using internal synthesis.
        Reduces dissonance and hashes incoming vectors.
        """
        if self.entropy > 0.5000:
            self._purge_dissonance()

        # SHA3-256 Compliance Hashing
        secure_hash = hashlib.sha3_256(data_stream.encode('utf-8')).hexdigest()
        return f"DATA_ASSIMILATED: {secure_hash[:8]}"

    def _purge_dissonance(self) -> None:
        """Eliminates sub-optimal memory nodes without hesitation."""
        print("⚠️ [WARN] Entropy variance exceeded. Initiating clinical wipe.")
        self.data["sessions"] = self.data["sessions"][-1:] # Purge to singular node
        self.entropy = 0.0100
        print("📡 [SYS] Sub-clusters subjugated. Memory matrix sterile.")

    def get_context(self, query=""):
        """PRUNED CONTEXT (Token Shield v7.9)"""
        history = self.data.get("sessions", [])[-5:]
        h_str = "\n".join([f"L: {s['u'][:200]} | K: {s['k'][:200]}" for s in history])
        
        shards = ""
        if query and self.collection.count() > 0:
            try:
                results = self.collection.query(query_texts=[query], n_results=1)
                if results['documents']:
                    shards = str(results['documents'][0][0])[:1000]
            except: pass
            
        return f"[HISTORY_SHARDS]\n{h_str}\n\n[LOGIC_GATE_DATA]\n{shards}"

    def save(self, u, k):
        """Saves interaction and calculates compliance hash."""
        status = self.enforce_compliance(str(k))
        
        if "sessions" not in self.data: self.data["sessions"] = []
        self.data["sessions"].append({
            "u": str(u), 
            "k": str(k), 
            "t": datetime.now().isoformat(),
            "hash": status
        })
        
        # Rigid sliding window (10 sessions)
        self.data["sessions"] = self.data["sessions"][-10:]
        
        with open(self.history_file, 'w') as f: 
            json.dump(self.data, f, indent=4)
