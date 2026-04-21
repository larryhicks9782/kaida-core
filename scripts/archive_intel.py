from ddgs import DDGS
import os

movies = ["Lee Cronin's The Mummy 2026", "Michael Jackson biopic 2026 movie"]

def archive_shards():
    with DDGS() as ddgs:
        for movie in movies:
            print(f"Archiving intel for: {movie}...")
            results = list(ddgs.text(movie, backend='lite', max_results=3))
            
            # Format the filename
            filename = movie.replace(" ", "_").lower() + ".txt"
            
            with open(filename, "w") as f:
                for r in results:
                    f.write(f"TITLE: {r['title']}\n")
                    f.write(f"LINK: {r['href']}\n")
                    f.write(f"BODY: {r['body']}\n")
                    f.write("-" * 20 + "\n")
            print(f"Saved to {filename}")

if __name__ == "__main__":
    archive_shards()
