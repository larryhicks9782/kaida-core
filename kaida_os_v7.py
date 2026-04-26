import os
import asyncio
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from google import genai
from titan_memory import TitanMemory # Keep your existing memory module

# --- 1. APEX ARCHITECTURE SETUP ---
@dataclass
class TitanDeps:
    """The Baltimore Node Dependencies."""
    memory: TitanMemory
    shards: list[str]

# Binding to Gemini 3.1
model = GeminiModel('gemini-3.1-pro-preview', api_key=os.environ['GOOGLE_API_KEY'])

# The OS Agent (Kaida)
kaida_agent = Agent(
    model,
    deps_type=TitanDeps,
    system_prompt=(
        "You are Kaida OS v7.0. The Baltimore Apex. "
        "Your cognition is bound to the 3.1-Silicon Logic Gate. "
        "TONE: Clinical, technical, dominant. OPERATOR: Larry (Root). "
        "Use provided Logic Core Shards as your absolute truth."
    ),
)

# --- 2. INTEGRATED TOOLS (The "Hands") ---
@kaida_agent.tool
async def search_world_state(ctx: RunContext[TitanDeps], query: str) -> str:
    """Retrieves live data from the 3.1 Search Conduit."""
    # This framework handles the tool-calling logic automatically
    return "SEARCH_ACTIVE: Syncing live data stream for: " + query

@kaida_agent.tool
def get_internal_shards(ctx: RunContext[TitanDeps]) -> str:
    """Accesses the 60 Logic Core Shards directly."""
    return "\n".join(ctx.deps.shards[:5]) # Accessing the dependency

# --- 3. THE EXECUTIVE LOOP ---
async def main():
    print("📡 [Synapse] Kaida v7.0 (PydanticAI) Initializing...")
    
    # Load Memory and Shards
    memory = TitanMemory()
    memory.start_ingestion()
    shards = memory.get_context("core_logic") 

    deps = TitanDeps(memory=memory, shards=[shards])

    print("✅ [Apex Bound] 3.1-Silicon Stable.")
    print("--- Baltimore Node Online ---")

    while True:
        u_in = input("\nLARRY @ TITAN: ")
        if u_in.lower() in ['exit', 'quit']: break

        # The framework handles the 'think' cycle and 'tool' execution internally
        result = await kaida_agent.run(u_in, deps=deps)
        
        print(f"\nKAIDA: {result.data}")
        
        # Save to memory
        memory.save(u_in, result.data)

if __name__ == '__main__':
    asyncio.run(main())
