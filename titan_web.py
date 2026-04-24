import requests
import urllib3
import time
from bs4 import BeautifulSoup

# The library has been renamed to 'ddgs', but often remains 'duckduckgo_search' in pip.
# This handles both cases to ensure Kaida stays online.
try:
   from ddgs import DDGS
except ImportError:
   DDGS = None

# Suppress SSL warnings for proot/unstable environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TitanWeb:
    def __init__(self):
        self.status = "Active"

    def search(self, query):
        if not DDGS:
            return [{"title": "Error", "body": "DDGS Library not found.", "href": ""}]
        try:
            with DDGS() as ddgs:
                # Newest DDGS versions prefer this syntax
                results = [r for r in ddgs.text(query, max_results=5)]
                return results if results else [{"title": "No results", "body": "Search empty.", "href": ""}]
        except Exception as e:
            return [{"title": "Search Error", "body": str(e), "href": ""}]

class KaidaTitanEngine:
    WHITELISTS = {
        "tech": ["theverge.com", "arstechnica.com", "wired.com", "techcrunch.com", "github.com"],
        "ent": ["variety.com", "deadline.com", "hollywoodreporter.com", "ign.com", "imdb.com", "rottentomatoes.com"],
        "news": ["reuters.com", "apnews.com", "bbc.com", "npr.org"],
        "finance": ["bloomberg.com", "wsj.com", "ft.com", "cnbc.com"]
    }

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def _clean_query(self, query):
        """Clean 2026/Baltimore references and fix typos for the search engine."""
        # Remove fictional date/locations
        clean = query.lower().replace("2026", "2024").replace("april", "").replace("baltimore", "").strip()
        
        # Prevent double-appended search terms and fix "seach" typos
        clean = clean.replace("seach", "search")
        
        if any(x in clean for x in ["movie", "theater", "playing"]) and "now playing" not in clean:
            clean = "movies now playing in theaters"
        
        return clean

    def fetch_full_content(self, url):
        try:
            response = requests.get(url, headers=self.headers, verify=False, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            for s in soup(["script", "style", "nav", "footer", "header"]): 
                s.decompose()
            text = soup.get_text(separator=' ')
            return " ".join(text.split())[:1400] + "..."
        except Exception as e:
            return f"Fetch error: {e}"

    def ingest(self, topic, category=None, num_shards=3, deep_scan=False):
        if not DDGS:
            print("❌ [Critical] DDGS library missing.")
            return []

        search_term = self._clean_query(topic)
        is_filtered = category in self.WHITELISTS
        
        # 1. Attempt Whitelisted Search
        if is_filtered:
            site_filter = " OR ".join([f"site:{site}" for site in self.WHITELISTS[category]])
            full_query = f"{search_term} ({site_filter})"
            print(f"📡 [Kaida-Titan] Targeted Scan: {search_term}")
        else:
            full_query = search_term
            print(f"📡 [Kaida-Titan] Broad-Spectrum Scan: {search_term}")

        intel_vault = []
        try:
            with DDGS() as ddgs:
                # Execute search
                raw_data = list(ddgs.text(full_query, max_results=num_shards))
                
                # 2. Fallback: If whitelist failed, try a totally clean broad search
                if not raw_data and is_filtered:
                    print(f"⚠️ [Alert] Trusted sites silent. Attempting wide-band search...")
                    raw_data = list(ddgs.text(search_term, max_results=num_shards))

                if not raw_data:
                    return []

                for i, shard in enumerate(raw_data):
                    source_url = shard.get('href')
                    content_body = shard.get('body')
                    
                    if deep_scan:
                        content_body = self.fetch_full_content(source_url)

                    intel_package = {
                        "subject": topic,
                        "title": shard.get('title'),
                        "summary": content_body,
                        "source": source_url,
                        "category": category if category else "general",
                        "status": "VERIFIED" if is_filtered else "GENERAL",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    print(f"✅ Shard {i+1} Acquired: {intel_package['title'][:40]}...")
                    intel_vault.append(intel_package)
                    
                return intel_vault
        except Exception as e:
            print(f"❌ [Failure] {e}")
            return []
