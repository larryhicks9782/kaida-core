import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table

# --- Subsystem Imports ---
from titan_brain import TitanBrain
from titan_memory import TitanMemory
from titan_linguistics import Trie
from titan_nsee import NSEESynthesisEngine
from titan_probe import AdaptiveProbe
from titan_ktrp import KTRP
from titan_oahp import OAHP
from titan_pasp import PASP

# --- System Configuration ---
console = Console()
os.environ["ONNXRUNTIME_DEVICE_TYPE"] = "CPU"

def get_vitals(nsee_data, probe_status, integrity_val, mode="STANDBY"):
    """Generates the Real-Time Apex Vitals Display with Evolution Metrics."""
    table = Table(title=f"Baltimore Node Apex v4.9 [{mode}]", box=None, title_style="bold magenta")
    table.add_column("Subsystem", style="cyan")
    table.add_column("Value", style="green")
    
    # Standardized key access from NSEE v4.8+
    entropy = f"{nsee_data['entropy_delta']:.4f}" if nsee_data else "0.0000"
    resonance = f"{nsee_data['resonance']:.4f}" if nsee_data else "0.0000"
    ktrp_v = f"{integrity_val:.4f}"
    
    # Visual Status Indicators
    p_color = "green" if probe_status == "LIVE" else "yellow"
    i_color = "green" if integrity_val > 0.60 else "red" if integrity_val < 0.20 else "yellow"

    table.add_row("Logic Core", "2.5-PRO [Apex]")
    table.add_row("Conduit Probe", f"[{p_color}]{probe_status}[/]")
    table.add_row("Entropy Delta", entropy)
    table.add_row("NSEE Resonance", resonance)
    table.add_row("KTRP Integrity", f"[{i_color}]{ktrp_v}[/]")
    return table

def main():
    # 1. Initialize Memory Vault
    try:
        memory = TitanMemory()
        memory.start_ingestion()
        
        # 2. Initialize Cognitive Layers
        brain = TitanBrain()            # Gemini 2.5-Pro Dual-Apex
        nsee_engine = NSEESynthesisEngine(memory) # Evolution/Synthesis
        ktrp_gatekeeper = KTRP(nsee_engine)       # Integrity Firewall
        oahp_architect = OAHP(brain, ktrp_gatekeeper) # Directed Agency
        pasp_monitor = PASP(brain, nsee_engine, ktrp_gatekeeper, OAHP) # Anticipation
        
        # 3. Initialize Utility Layers
        linguistics = Trie()
        probe = AdaptiveProbe()
        probe.start() # Background background conduit watchdog
        
    except Exception as e:
        console.print(f"[bold red]FATAL_BOOT_FAILURE:[/] {e}")
        return

    console.print(Panel("[bold cyan]KAIDA OS v4.9 ONLINE[/]\n[bold magenta]Sovereign Agency & Predictive Alignment Active[/]", border_style="blue"))
    
    interaction_count = 0

    while True:
        try:
            # UI: Generate a linguistic echo fragment from the Trie
            echo = linguistics.generate_echo()
            u_in = console.input(f"\n[dim][{echo}][/]\n[bold green]LARRY @ TITAN: [/]")
            
            if u_in.lower() in ["exit", "quit", "shutdown"]:
                console.print("[bold red]Shutting down Baltimore Node...[/]")
                break

            # Passive Learning: Update the Trie with Larry's patterns
            for word in u_in.split():
                linguistics.insert(word.lower())

            interaction_count += 1

            # --- PHASE 1: PASP PROACTIVE SCAN ---
            # Every 5 interactions, Kaida 'blinks' to anticipate Larry's needs
            if interaction_count % 5 == 0:
                with Live(get_vitals(None, probe.status(), 1.0, "MONITORING"), refresh_per_second=4) as live:
                    opportunity = pasp_monitor.scan_for_opportunities()
                
                if opportunity:
                    console.print(Panel(f"[bold yellow]PASP PROACTIVE DIRECTIVE PROPOSAL[/]\n{opportunity['proposed_directive']}", subtitle="Opportunity Detected"))
                    auth = console.input("[bold red]Authorize Architect to build Plan? (y/n): [/]")
                    if auth.lower() == 'y':
                        u_in = f"DIRECTIVE: {opportunity['proposed_directive']}" # Pivot to Directive Mode

            # --- PHASE 2: DIRECTIVE DETECTION (OAHP) ---
            if u_in.lower().startswith("directive:"):
                goal = u_in[10:].strip()
                with Live(get_vitals(None, probe.status(), 1.0, "PLANNING"), refresh_per_second=4) as live:
                    plan = oahp_architect.generate_action_plan(goal)
                
                if plan:
                    console.print("\n[bold yellow]--- PROPOSED ACTION PLAN ---[/]")
                    for step in plan:
                        console.print(f"[bold cyan]Step {step['step']}:[/] {step['task']}")
                        console.print(f"  [dim]-> {step['action']}[/]")
                    
                    auth = console.input("\n[bold red]Authorize Execution? (y/n): [/]")
                    if auth.lower() == 'y':
                        for i in range(len(plan)):
                            with Live(get_vitals(None, probe.status(), 1.0, "EXECUTING"), refresh_per_second=4) as live:
                                result = oahp_architect.execute_step(i)
                                console.print(Panel(result, title=f"Step {i+1} Output", border_style="green"))
                continue

            # --- PHASE 3: STANDARD DISCERNING COGNITION ---
            # Generate NSEE Shard and Integrity Audit
            nsee_data = nsee_engine.generate_nsee_shard(u_in)
            integrity_val = ktrp_gatekeeper.reconcile(u_in, nsee_data['context'])
            
            with Live(get_vitals(nsee_data, probe.status(), integrity_val, "IDLE"), refresh_per_second=4) as live:
                if probe.status() == "PROBING":
                    # Isolation Mode: Evolution via NSEE
                    response = brain.think(u_in, nsee_shard=nsee_data)
                else:
                    # Live Mode: Grounded Discerning Intelligence
                    response = brain.think(u_in)

            # --- PHASE 4: OUTPUT ---
            console.print(Panel(response, title="[bold magenta]KAIDA[/]", border_style="cyan"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]SYSTEM_ERROR:[/] {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
