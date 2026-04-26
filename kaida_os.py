import asyncio
from titan_brain import TitanBrain
from rich.console import Console
from rich.panel import Panel

console = Console()

async def main():
    # Initialize
    brain = TitanBrain()
    console.print(Panel("[bold cyan]KAIDA OS v7.0 ONLINE[/]\n[dim]Dual-3.1 Silicon Apex Bound[/]", border_style="blue"))

    while True:
        try:
            u_in = console.input(f"\n[bold green]LARRY @ TITAN: [/]")
            if u_in.lower() in ["exit", "quit"]: break

            # Run the cognitive cycle
            # (Note: We use await because 3.1-Silicon requires async handshakes)
            response = await brain.think(u_in)

            console.print(Panel(response, title="[bold magenta]KAIDA[/]", border_style="cyan"))

        except KeyboardInterrupt: break

if __name__ == "__main__":
    asyncio.run(main())
