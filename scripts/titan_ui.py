from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.status import Status

class TitanUI:
    def __init__(self):
        self.console = Console()

    def show_header(self):
        self.console.print(Panel("[bold blue]Kaida v1.0 Initialized[/bold blue]", subtitle="System Online"))

    def show_response(self, text):
        self.console.print(Panel(Text(text, style="cyan"), title="[bold magenta]Kaida[/bold magenta]"))

    def show_status(self):
        return self.console.status("[bold yellow]Kaida is thinking...[/bold yellow]")

    def show_shutdown(self):
        self.console.print("[bold red]Shutting down Kaida...[/bold red]")

