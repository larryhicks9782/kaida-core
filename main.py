import os
os.environ["ONNXRUNTIME_DEVICE_TYPE"] = "CPU"

from titan_brain import TitanBrain
from titan_web import KaidaTitanEngine
from titan_reasoning import ReasoningEngine
from titan_linguistics import Trie, get_shard_weight # <--- NEW IMPORT
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    brain = TitanBrain()
    kaida = KaidaTitanEngine()
    reasoner = ReasoningEngine(brain_instance=brain)
    
    # INITIALIZE LINGUISTIC MAP
    linguistic_map = Trie()

    console.print(Panel("[bold cyan]KAIDA OS ONLINE[/]\n[dim]Baltimore Node Active[/]", border_style="blue"))

    while True:
        try:
            u_in = console.input(f"\n[bold green]LARRY @ TITAN: [/]")
            
            if u_in.lower() in ["exit", "quit"]:
                break

            # --- TRIE INTEGRATION ---
            # Kaida "learns" the structure of your input
            for word in u_in.split():
                linguistic_map.insert(word.lower())

            # DIAGNOSTIC COMMAND: Check the Trie state
            if "internal diagnostic" in u_in.lower():
                path = linguistic_map.get_reconstructed_path()
                weight = get_shard_weight(path)
                diag_msg = (
                    f"LINGUISTIC_MAP_DIAGNOSTIC:\n"
                    f"Reconstructed Path: [bold yellow]{path}[/]\n"
                    f"Logic Shard Weight: [bold cyan]{weight}[/]\n"
                    f"Status: Shard integrity nominal."
                )
                console.print(Panel(diag_msg, title="SYSTEM INFO", border_style="white"))
                continue 

            # --- NORMAL SEARCH/THINK LOGIC ---
            fact_keywords = ["who", "what", "where", "when", "how", "news", "status", "search", "current", "movie"]
            needs_web = any(word in u_in.lower() for word in fact_keywords) or len(u_in.split()) > 5

            if needs_web:
                with console.status("[bold blue]Scanning Global Data Stream..."):
                    shards = kaida.ingest(u_in)
                    if shards:
                        response = reasoner.get_tot_response(u_in, search_context=shards)
                    else:
                        response = brain.think(f"SYSTEM_ALERT: Data stream silent for query: {u_in}")
            else:
                with console.status("[bold yellow]Thinking..."):
                    response = brain.think(u_in)

            console.print(Panel(response, title="[bold magenta]KAIDA[/]", border_style="cyan"))

        except Exception as e:
            console.print(f"[bold red]System Error:[/] {e}")

if __name__ == "__main__":
    main()
