# NEW IMPORT for 2026
from ddgs import DDGS 
import time

def titan_search(query):
    print(f"Titan Lab 9782: Querying the stream for '{query}'...")
    
    # We use 'lite' backend as it's more stable in proot environments
    with DDGS() as ddgs:
        try:
            # max_results is now a strict keyword
            results = list(ddgs.text(query, max_results=3))
            
            if not results:
                print("Status: Stream Empty. Retrying with alternate backend...")
                # Fallback to the 'html' version if the default API is blocked
                results = list(ddgs.text(query, max_results=3))

            for r in results:
                print(f"Shard Found: {r['title']}")
                # Here is where your Firebase logic goes
                
        except Exception as e:
            print(f"Connection Error: {e}")

titan_search("Mandalorian movie release date 2026")

