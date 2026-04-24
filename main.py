import os
# Fix the GPU Discovery Error
os.environ["ONNXRUNTIME_DEVICE_TYPE"] = "CPU"

from titan_brain import TitanBrain
from titan_web import KaidaTitanEngine
from titan_reasoning import ReasoningEngine
from titan_linguistics import Trie, get_shard_weight
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    # Initialize Subsystems
    brain = TitanBrain()
    kaida = KaidaTitanEngine()
    reasoner = ReasoningEngine(brain_instance=brain)
    linguistic_map = Trie()

    console.print(Panel("[bold cyan]KAIDA OS ONLINE[/]\n[dim]Baltimore Node Active[/]", border_style="blue"))

    while True:
        try:
            u_in = console.input(f"\n[bold green]LARRY @ TITAN: [/]")
            
            if u_in.lower() in ["exit", "quit"]:
                break

            # Passive Linguistic Learning
            for word in u_in.split():
                linguistic_map.insert(word.lower())

            # Intent Detection for Search
            fact_keywords = ["who", "what", "where", "when", "how", "news", "status", "search", "current", "movie", "playing"]
            needs_web = any(word in u_in.lower() for word in fact_keywords) or len(u_in.split()) > 5

            if needs_web:
                # Combined status for a smoother UI experience
                with console.status("[bold blue]📡 Baltimore Node: Accessing Live Data Stream..."):
                    shards = kaida.ingest(u_in)
                    
                    if shards:
                        # Success: Use reasoning engine (Bayesian/ToT)
                        response = reasoner.get_tot_response(u_in, search_context=shards)
                    else:
                        # Search failed: Fallback to persona
                        fail_msg = f"SYSTEM_ALERT: Data stream silent. Inform user node cannot draw live data for: {u_in}"
                        response = brain.think(fail_msg, use_tools=False)
            else:
                # Standard Small Talk / Conversation
                with console.status("[bold yellow]🧠 Kaida OS: Thinking..."):
                    response = brain.think(u_in)

            # Final Output
            console.print(Panel(response, title="[bold magenta]KAIDA[/]", border_style="cyan"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            # This closes the try block and handles any system errors
            console.print(f"[bold red]System Error:[/] {e}")

if __name__ == "__main__":
    main()
