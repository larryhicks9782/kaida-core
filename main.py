from titan_brain import TitanBrain
from titan_web import TitanWeb, KaidaTitanEngine
from titan_reasoning import ReasoningEngine
from titan_ui import TitanUI
from rich.panel import Panel

def main():
    # Initialize components
    ui = TitanUI()
    web_tool = TitanWeb()
    kaida_ingestor = KaidaTitanEngine()
    brain = TitanBrain(web_instance=web_tool)
    reasoner = ReasoningEngine(brain_instance=brain)

    ui.show_header()

    while True:
        try:
            u_in = ui.console.input(f"\n[bold green]LARRY @ TITAN: [/]")
        except EOFError: break
        
        if u_in.lower() in ["exit", "quit"]:
            ui.show_shutdown()
            break

        # Search Trigger logic
        must_search = any(x in u_in.lower() for x in ["movie", "play", "theater", "news"])
        
        if must_search or len(u_in.split()) > 10:
            with ui.show_status():
                # Uses your Ingestion Engine
                raw_data = kaida_ingestor.ingest(u_in, category="ent" if must_search else None)
                if not raw_data:
                    response = "The data stream is silent, Larry."
                else:
                    # Uses your Tree of Thoughts Reasoning
                    response = reasoner.get_tot_response(u_in, search_context=raw_data)
        else:
            with ui.show_status():
                # Uses the upgraded Brain with 11 sessions + ChromaDB
                response = brain.think(u_in)

        ui.show_response(response)

if __name__ == "__main__":
    main()
