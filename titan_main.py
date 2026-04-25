import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table

# Import upgraded subsystems
from titan_brain import TitanBrain
from titan_web import KaidaTitanEngine
from titan_reasoning import ReasoningEngine
from titan_linguistics import Trie
from titan_memory import TitanMemory

console = Console()

def get_vitals_table():
    table = Table(title="Baltimore Node Vitals", box=None)
    table.add_column("Subsystem", style="cyan")
    table.add_column("Status", style="green")
    table.add_row("Logic Core", "STABLE")
    table.add_row("Uplink", "ENCRYPTED")
    table.add_row("Memory Shards", "60/60")
    return table

def main():
    # Initialize
    memory = TitanMemory()
    memory.start_ingestion()
    
    brain = TitanBrain()
    web = KaidaTitanEngine()
    reasoner = ReasoningEngine(brain)
    linguistics = Trie()

    console.print(Panel("[bold cyan]KAIDA OS v2.0 - BALTIMORE NODE READY[/]", border_style="blue"))
    console.print(get_vitals_table())

    while True:
        try:
            # UI: Dynamic Echo
            echo = linguistics.generate_echo()
            u_in = console.input(f"\n[dim][{echo}][/]\n[bold green]LARRY @ TITAN: [/]")
            
            if u_in.lower() in ["exit", "quit", "shutdown"]:
                break

            # Passive Learning
            for word in u_in.split():
                linguistics.insert(word.lower())

            # Multi-Stage Intelligence
            with Live(console.status("[bold blue]📡 Scanning Data Stream..."), refresh_per_second=4) as live:
                
                # Step 1: Web Scrape (if needed)
                if any(k in u_in.lower() for k in ["news", "who", "what", "search"]):
                    shards = web.ingest(u_in)
                    response = reasoner.get_tot_response(u_in, search_context=shards)
                else:
                    # Step 2: Recursive Thinking
                    response = brain.think(u_in)

            # Step 3: Final Refraction
            console.print(Panel(response, title="[bold magenta]KAIDA[/]", border_style="cyan"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]SYSTEM_ERROR:[/] {e}")

if __name__ == "__main__":
    main()
