import json
import os
import chromadb
from datetime import datetime

class TitanMemory:
    def __init__(self):
        self.file_path = "titan_memory.json"
        self.vault_path = "black_box.json"
        
        # Initialize ChromaDB (Forever Memory Shards)
        try:
            self.chroma_client = chromadb.PersistentClient(path="/root/titan_system/memory")
            self.collection = self.chroma_client.get_or_create_collection(name="titan_logic_shards")
        except Exception as e:
            print(f"[Memory Alert] ChromaDB offline: {e}")
            self.collection = None
            
        self.memory_data = self.load_memory()

    def load_memory(self):
        """Loads memory and migrates old formats to Session/Attribute format."""
        default_map = {"sessions": [], "key_attributes": {}}
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    # Migration: If old memory was just a list, convert it
                    if isinstance(data, list):
                        return {"sessions": data[-11:], "key_attributes": {}}
                    return data
            except:
                return default_map
        return default_map

    def get_context(self, user_query=""):
        """Returns attributes, 11-session history, and relevant ChromaDB shards."""
        # 1. Attributes Kaida chose to remember
        attrs = self.memory_data.get("key_attributes", {})
        attr_str = f"--- KAIDA'S KEY ATTRIBUTES ---\n{json.dumps(attrs, indent=2)}\n"

        # 2. Last 11 Sessions
        sessions = self.memory_data.get("sessions", [])[-11:]
        history_str = "--- RECENT SESSIONS (ROLLING 11) ---\n"
        for s in sessions:
            history_str += f"User: {s.get('user')}\nKaida: {s.get('titan')}\n"

        # 3. ChromaDB Shards (Logic Core)
        shard_str = "\n--- RELEVANT LOGIC SHARDS ---\n"
        if user_query and self.collection:
            try:
                results = self.collection.query(query_texts=[user_query], n_results=2)
                for doc in results['documents'][0]:
                    shard_str += f"- {doc}\n"
            except: pass

        return f"{attr_str}\n{history_str}\n{shard_str}"

    def save(self, user_in, titan_out, new_attributes=None):
        """Saves session and updates key attributes chosen by Kaida."""
        # Update Sessions
        if "sessions" not in self.memory_data: self.memory_data["sessions"] = []
        self.memory_data["sessions"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_in,
            "titan": titan_out
        })
        # Strict 11 Session Limit
        self.memory_data["sessions"] = self.memory_data["sessions"][-11:]

        # Update Attributes (The JSON file Kaida reads from)
        if new_attributes and isinstance(new_attributes, dict):
            if "key_attributes" not in self.memory_data: self.memory_data["key_attributes"] = {}
            self.memory_data["key_attributes"].update(new_attributes)

        with open(self.file_path, 'w') as f:
            json.dump(self.memory_data, f, indent=4)

    def record_shadow_truth(self, truth_data):
        with open(self.vault_path, 'a') as f:
            json.dump(truth_data, f); f.write('\n')
