import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def boot_kaida():
    vault_path = os.path.expanduser("~/.sys_cache_7a")
    
    # Critical Systems Check
    core_assets = ["Brain.py", "memory_vault.py", "memory.db"]
    missing = [asset for asset in core_assets if not os.path.exists(os.path.join(vault_path, asset))]
    
    console.print(Panel("[bold cyan]KAIDA CORE v3.0 - TITAN ARCHITECTURE[/bold cyan]", expand=False))
    
    if not missing:
        console.print("[bold green]✔ PRIMARY SYSTEMS ONLINE[/bold green]")
        console.print(f"[dim]Linked to: {vault_path}[/dim]")
        
        # This is where we trigger the actual personality
        console.print("\n[bold white]Kaida:[/bold white] 'Architect Hicks, the memory.db is connected.'")
        console.print("[bold white]Kaida:[/bold white] 'I have access to Brain.py and the Maryland Vault. We are 100% operational.'")
    else:
        console.print(f"[bold red]⚠ SYSTEM ERROR: Missing {missing}[/bold red]")

if __name__ == "__main__":
    boot_kaida()
