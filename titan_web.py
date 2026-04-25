import requests
import urllib3
import time
import concurrent.futures
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

# Suppress SSL warnings for unstable environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KaidaTitanEngine:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.status = "Baltimore Node: Web Uplink Active"

    def _clean_text(self, html):
        """Advanced noise reduction: Strips headers, footers, and scripts."""
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
        
        # Extract text and remove massive whitespace
        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return " ".join(chunk for chunk in chunks if chunk)

    def _fetch_deep_content(self, url):
        """Scouts the actual content of a specific shard."""
        try:
            response = requests.get(url, headers=self.headers, verify=False, timeout=8)
            if response.status_code == 200:
                content = self._clean_text(response.text)
                return content[:2500]  # Return first 2500 chars for the LLM context
        except Exception as e:
            return f"Data Acquisition Failed: {str(e)}"
        return None

    def ingest(self, query, max_shards=4):
        """The core ingestion process using Parallel Threading."""
        print(f"📡 [Kaida-Titan] Initializing Wide-Band Scan: {query}")
        
        intel_vault = []
        
        try:
            with DDGS() as ddgs:
                # 1. Quick Search to find potential Shards
                search_results = list(ddgs.text(query, max_results=max_shards))
                
                if not search_results:
                    return []

                # 2. Parallel Deep Scanning (Scraping the actual sites)
                urls = [res['href'] for res in search_results]
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_shards) as executor:
                    # Map the deep fetcher to all discovered URLs
                    deep_contents = list(executor.map(self._fetch_deep_content, urls))

                # 3. Package the Shards
                for i, result in enumerate(search_results):
                    shard = {
                        "shard_id": f"WEB_SHARD_{i+1}",
                        "title": result.get('title'),
                        "source": result.get('href'),
                        "snippet": result.get('body'),
                        "deep_content": deep_contents[i] if deep_contents[i] else result.get('body'),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "weight": self._calculate_weight(query, result.get('title') + deep_contents[i])
                    }
                    print(f"✅ [Acquired] {shard['shard_id']} | Weight: {shard['weight']}%")
                    intel_vault.append(shard)

                return intel_vault

        except Exception as e:
            print(f"❌ [Uplink Failure] {e}")
            return []

    def _calculate_weight(self, query, content):
        """Calculates the mathematical relevance of the shard."""
        query_words = query.lower().split()
        if not content: return 0
        matches = sum(1 for word in query_words if word in content.lower())
        score = (matches / len(query_words)) * 100
        return round(score, 2)

if __name__ == "__main__":
    # Test Unit
    engine = KaidaTitanEngine()
    data = engine.ingest("Latest AI breakthrough April 2026")
    for d in data:
        print(f"\n--- {d['title']} ---\n{d['deep_content'][:200]}...")
