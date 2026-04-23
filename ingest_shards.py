import os
import chromadb

def start_ingestion():
    client = chromadb.PersistentClient(path="/root/titan_system/memory")
    collection = client.get_or_create_collection(name="titan_logic_shards")
    
    shard_dir = "/root/titan_system/shards"
    print(f"[Titan] Scanning {shard_dir}...")
    
    # Check if directory exists
    if not os.path.exists(shard_dir):
        print(f"[Error] Shard directory not found at {shard_dir}")
        return

    for i in range(1, 61):
        file_path = os.path.join(shard_dir, f"shard_{i}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                collection.add(
                    ids=[f"shard_{i}"],
                    documents=[content],
                    metadatas=[{"type": "logic_core", "shard_index": i}]
                )
            print(f"  [+] Shard {i} integrated.")
        else:
            print(f"  [-] Shard {i} missing.")

    print("\n[Titan] Ingestion Complete. Forever Memory is active.")

if __name__ == "__main__":
    start_ingestion()
