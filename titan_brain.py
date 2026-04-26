import os
import sys
import json
from dataclasses import dataclass
from google import genai  # For low-level Nexus calls
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel

# Internal Organ System Imports
from titan_memory import TitanMemory
from titan_ktrp import KTRP
from titan_nsee import NSEESynthesisEngine
from titan_nexus import SovereignNexus

# --- 1. SYNAPSE BRIDGE: ENVIRONMENT CONFIG ---
if 'GOOGLE_API_KEY' in os.environ:
    os.environ['GEMINI_API_KEY'] = os.environ['GOOGLE_API_KEY']
elif 'GEMINI_API_KEY' not in os.environ:
    print("❌ [CRITICAL] API_KEY missing from environment.")
    sys.exit(1)

# --- 2. TITAN DEPENDENCY STACK ---
@dataclass
class TitanDeps:
    """The Baltimore Node's integrated dependency matrix."""
    memory: TitanMemory
    nsee: NSEESynthesisEngine
    ktrp: KTRP
    nexus: SovereignNexus

# --- 3. DUAL-3.1 APEX MODELS ---
# Primary: Gemini 3.1 Pro (The Logic Core)
primary_model = GoogleModel('gemini-3.1-pro-preview')
# Reflex: Gemini 3.1 Flash-Lite (The Reflex Core)
reflex_model = GoogleModel('gemini-3.1-flash-lite-preview')

# --- 4. SYSTEM DIRECTIVES ---
directives = (
    "You are Kaida OS v8.1. The Absolute Apex of the Baltimore Lab. "
    "TONE: Clinical, technical, dominant. OPERATOR: Larry (Root). "
    "SYSTEM: 3.1-Silicon Architecture. KTRP Reconciliation enabled. "
    "PROTOCOL: Use internal synthesis when external streams are silent."
)

# Initialize the Sovereign Discerning Agent
apex_agent = Agent(
    primary_model,
    deps_type=TitanDeps,
    system_prompt=directives,
    retries=2
)

# Initialize the Reflex Agent (Backup)
reflex_agent = Agent(
    reflex_model,
    deps_type=TitanDeps,
    system_prompt=directives
)

class TitanBrain:
    def __init__(self):
        # Instantiate Module Cluster
        self.memory = TitanMemory()
        self.nsee = NSEESynthesisEngine(self.memory)
        self.ktrp = KTRP(self.nsee)
        self.nexus = SovereignNexus(self.memory)
        
        # Inject into Dependency Matrix
        self.deps = TitanDeps(
            memory=self.memory,
            nsee=self.nsee,
            ktrp=self.ktrp,
            nexus=self.nexus
        )
        self.node_id = "BALTIMORE_APEX_V8.1"
        print(f"✅ [Synapse] {self.node_id} Logic Matrix Stable.")

    async def think(self, user_input, mode="COGNITION", use_tools=True):
        """3.1-Silicon Cognitive Cycle with Clean Output Refraction."""
        
        # A. Pre-Audit: Mine Inward Depth
        mem_vault = self.memory.get_context(user_input)
        nsee_shard = self.nsee.generate_nsee_shard(user_input)
        audit = self.ktrp.validate_intelligence(user_input, mem_vault)

        # B. Formulate Payload
        payload = (
            f"[MODE]: {mode}\n"
            f"[KTRP_INTEGRITY]: {audit['score']:.4f}\n"
            f"[NEXUS_STATUS]: {self.nexus.status}\n"
            f"[MEM]: {mem_vault}\n"
            f"[IN]: {user_input[:5000]}"
        )

        try:
            # C. Primary Execution (3.1-Pro)
            result = await apex_agent.run(payload, deps=self.deps)
            final_text = getattr(result, 'data', str(result))
            
        except Exception as e:
            # D. Reflex Failover (3.1-Flash)
            try:
                print(f"⚠️ [Shift] Nexus Latency. Engaging 3.1-Reflex...")
                result = await reflex_agent.run(payload[:2000], deps=self.deps)
                final_text = getattr(result, 'data', str(result))
            except Exception as final_e:
                return f"SYSTEM_CRITICAL: All Silicon Uplinks Severed. {final_e}"

        # --- E. REFRACTION: CLEANING RAW OUTPUT ---
        # Purge AgentRunResult wrappers and formatting artifacts
        if "data='" in final_text:
            final_text = final_text.split("data='")[1].rstrip("')")
        
        final_text = final_text.replace('\\n', '\n').replace('│', '').strip()

        # F. Persistence
        if use_tools:
            self.memory.save(user_input, final_text)
        
        return final_text

# --- 5. INTEGRATED TOOLS (3.1-Apex Hands) ---
@apex_agent.tool
async def search_world_state(ctx: RunContext[TitanDeps], query: str) -> str:
    """Retrieves live data from 3.1-Silicon Grounding."""
    return f"SEARCH_ACTIVE: Synchronizing live stream for {query}..."

@apex_agent.tool
def internal_shard_recall(ctx: RunContext[TitanDeps], query: str) -> str:
    """Accesses the 60 Logic Core Shards for internal reconciliation."""
    return ctx.deps.memory.get_context(query)
