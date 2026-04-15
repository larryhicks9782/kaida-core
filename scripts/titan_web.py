import requests
import urllib3
from titan_brain import TitanBrain
from titan_reasoning import ReasoningEngine
from datetime import datetime
from bs4 import BeautifulSoup  # Added for scraping logic
try:
    from duckduckgo_search import DDGS  # You'll need to: pip install duckduckgo_search
except ImportError:
    DDGS = None
    reasoner = ReasoningEngine(brain_instance=brain_instance)
    brain_instance = TitanBrain() 
# 1. Silences the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TitanWeb:
    def __init__(self):
        self.agent_name = "Kaida"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def get_weather(self, city="baltimore"):
        try:
            response = requests.get(f"https://wttr.in/{city}?format=3", verify=False, timeout=5)
            return response.text.strip()
        except Exception as e:
            self.log_rejection("Weather Fetch Failure", str(e))
            return "Weather unavailable"

    def search(self, query):
        """Perform a live search and return the top results."""
        try:
            print(f"[{self.agent_name}] Searching for: {query}...")
            if DDGS is None:
                return "Search unavailable: duckduckgo_search library not installed."
            
            results = []
            with DDGS() as ddgs:
                # Taking the top 3 results for 2026 context
                for r in ddgs.text(query, max_results=3):
                    results.append(f"{r['title']}: {r['href']}")
            
            return results if results else "No results found."
        except Exception as e:
            self.log_rejection("Search Failure", str(e))
            return f"Search error: {e}"

    def scrape_page(self, url):
        """Scrapes the text content of a specific URL."""
        try:
            print(f"[{self.agent_name}] Scraping: {url}...")
            response = requests.get(url, headers=self.headers, verify=False, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extracting paragraphs to get the gist of the page
            paragraphs = soup.find_all('p')
            text_content = " ".join([p.get_text() for p in paragraphs[:5]]) # Get first 5 paragraphs
            return text_content[:500] + "..." # Return snippet
        except Exception as e:
            self.log_rejection("Scraping Failure", str(e))
            return "Failed to scrape page."

    def log_rejection(self, error_type, detail):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("rejection_log.txt", "a") as f:
            f.write(f"[{timestamp}] {self.agent_name} - {error_type}: {detail}\n")

    def run_task(self, user_query="What are the top news headlines for April 2026?"):
        try:
            print(f"--- {self.agent_name} System Online ---")
            print(f"Current Weather: {self.get_weather()}")
            
            # 1. Search for data
            search_results = self.search(user_query)
            print(f"Search Results: {search_results}")
            
            # 2. If we found a URL, let's scrape the first one
            if isinstance(search_results, list) and len(search_results) > 0:
                first_url = search_results[0].split(": ")[1]
                content = self.scrape_page(first_url)
                print(f"Scraped Insight: {content}")
            
        except Exception as e:
            self.log_rejection("Protocol Bypass Attempt", str(e))
            print(f"Critical Deviation Caught: {e}")

if __name__ == "__main__":

    # 1. Initialize the components
    # (Assuming your 'brain' instance is already defined)
    titan_web = TitanWeb()
    reasoner = ReasoningEngine(brain_instance=brain_instance)

    # 2. Define the goal
    user_query = "Summarize recent media releases."

    # 3. The 'Splice': Connect the search to the reasoning
    print(f"--- Starting Task: {user_query} ---")
    
    # First, get the raw data from the web
    raw_web_data = titan_web.get_weather() # or titan_web.search(user_query)
    
    # Second, pass that specific data into the Tree of Thoughts engine
    
    # 4. Final Result
    print("\nResult:")
    print(final_output)
