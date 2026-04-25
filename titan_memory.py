import os
import json
import chromadb
from datetime import datetime

class TitanMemory:
    def __init__(self):
        self.base_dir = os.getcwd()
        self.db_path = os.path.join(self.base_dir, "memory")
        self.history_file = os.path.join(self.base_dir, "titan_memory.json")
        
        if not os.path.exists(self.db_path): 
            os.makedirs(self.db_path)
            
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(name="titan_shards")
        
        # Standardizing attribute name to 'data' for NSEE compatibility
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f: 
                    return json.load(f)
            except:
                return {"sessions": [], "key_attributes": {}}
        return {"sessions": [], "key_attributes": {}}

    def start_ingestion(self):
        """Ingest the 60 Logic Core Shards into Vector Space."""
        shard_dir = os.path.join(self.base_dir, "shards")
        if not os.path.exists(shard_dir): return "NO_SHARDS"
        
        if self.collection.count() == 0:
            for i in range(1, 61):
                path = os.path.join(shard_dir, f"shard_{i}.txt")
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        self.collection.add(ids=[f"S_{i}"], documents=[f.read().strip()])
            return "CORE_INGESTED"
        return "CORE_READY"

    def get_context(self, query=""):
        """Aggregates history and vector shards for the Brain."""
        history = self.data.get("sessions", [])[-10:]
        h_str = "\n".join([f"L: {s['u']} | K: {s['k']}" for s in history])
        
        shards = ""
        if query and self.collection.count() > 0:
            try:
                results = self.collection.query(query_texts=[query], n_results=2)
                shards = "\n".join(results['documents'][0])
            except:
                pass
            
        return f"[HISTORY]\n{h_str}\n\n[LOGIC_CORE]\n{shards}"

    def save(self, u, k):
        """Saves exchange and updates the internal data object."""
        if "sessions" not in self.data:
            self.data["sessions"] = []
            
        self.data["sessions"].append({
            "u": u, 
            "k": k, 
            "t": datetime.now().isoformat()
        })
        
        # Maintain rolling 20 session limit for entropy stability
        self.data["sessions"] = self.data["sessions"][-20:]
        
        with open(self.history_file, 'w') as f: 
            json.dump(self.data, f, indent=4)
