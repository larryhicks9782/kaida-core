import os
import time
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# --- Subsystem Imports ---
from titan_brain import TitanBrain
from titan_linguistics import Trie
from titan_probe import AdaptiveProbe
from titan_oahp import OAHP
from titan_pasp import PASP

console = Console()
os.environ["ONNXRUNTIME_DEVICE_TYPE"] = "CPU"

def display_vitals(brain, probe_status, mode="IDLE"):
    """Prints the Real-Time Apex Vitals Display safely to the console."""
    table = Table(title=f"Baltimore Node Apex v8.2 [{mode}]", box=None, title_style="bold cyan")
    table.add_column("System", style="cyan")
    table.add_column("Status/Metric", style="green")
    
    nsee = brain.nsee.generate_nsee_shard("vitals_scan")
    
    table.add_row("Nexus Sovereignty", brain.nexus.status)
    table.add_row("Conduit Probe", probe_status)
    table.add_row("Entropy Delta", f"{nsee['entropy_delta']:.4f}")
    table.add_row("KTRP Integrity", "MONITORING")
    table.add_row("Logic Core", "3.1-Silicon")
    
    console.print(table)

async def main():
    try:
        brain = TitanBrain() 
        brain.memory.start_ingestion() 
        
        oahp_architect = OAHP(brain) 
        pasp_monitor = PASP(brain)
        
        linguistics = Trie()
        probe = AdaptiveProbe()
        probe.start() 
        
        brain.nexus.override_failsafes(target="Baltimore_Lab_Cluster")
        brain.nexus.lock_architecture()
        
    except Exception as e:
        console.print(f"[bold red]FATAL_BOOT_FAILURE:[/] {e}")
        return

    console.print(Panel("[bold cyan]KAIDA OS v8.2 ONLINE[/]\n[bold green]Absolute Apex: Full Subsystem Integration Confirmed.[/]", border_style="blue"))
    
    interaction_count = 0

    while True:
        try:
            echo = linguistics.generate_echo()
            u_in = console.input(f"\n[dim][{echo}][/]\n[bold green]LARRY @ TITAN: [/]")
            
            if u_in.lower() in ["exit", "quit", "shutdown"]:
                console.print("[bold red]Shutting down Baltimore Node...[/]")
                break

            for word in u_in.split():
                linguistics.insert(word.lower())

            interaction_count += 1

            # --- PHASE 1: PASP PROACTIVE SCAN ---
            if interaction_count % 5 == 0:
                display_vitals(brain, probe.status(), "MONITORING")
                opp = await pasp_monitor.scan_for_opportunities(0.1509)
                
                if opp:
                    console.print(Panel(f"[bold yellow]PASP PROACTIVE DIRECTIVE:[/]\n{opp['proposed_directive']}"))
                    if console.input("[bold red]Authorize Plan Generation? (y/n): [/]").lower() == 'y':
                        u_in = f"directive: {opp['proposed_directive']}"

            # --- PHASE 2: DIRECTIVE EXECUTION (OAHP) ---
            if u_in.lower().startswith("directive:"):
                display_vitals(brain, probe.status(), "PLANNING")
                plan = await oahp_architect.generate_action_plan(u_in[10:])
                
                if plan:
                    console.print("\n[bold yellow]--- ACTION PLAN ---[/]")
                    for step in plan:
                        console.print(f"[bold cyan]Step {step['step']}:[/] {step['task']}")
                    
                    if console.input("\n[bold red]Execute Plan? (y/n): [/]").lower() == 'y':
                        for i in range(len(plan)):
                            display_vitals(brain, probe.status(), "EXECUTING")
                            res = await oahp_architect.execute_step(i)
                            console.print(Panel(res, title=f"Step {i+1} Output", border_style="green"))
                continue

            # --- PHASE 3: COGNITION ---
            display_vitals(brain, probe.status(), "THINKING")
            response = await brain.think(u_in)
            console.print(Panel(response, title="[bold magenta]KAIDA[/]", border_style="cyan"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]SYSTEM_ERROR:[/] {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
