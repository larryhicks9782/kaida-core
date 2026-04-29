import os
import sys
import traceback
import subprocess
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel

# Internal Organ System Imports
from titan_memory import TitanMemory
from titan_ktrp import KTRP
from titan_nsee import NSEESynthesisEngine
from titan_nexus import SovereignNexus

# --- 1. SYNAPSE BRIDGE: ENVIRONMENT CONFIG ---
if 'GOOGLE_API_KEY' in os.environ and 'GEMINI_API_KEY' not in os.environ:
    os.environ['GEMINI_API_KEY'] = os.environ['GOOGLE_API_KEY']

if 'GEMINI_API_KEY' not in os.environ:
    print("❌[CRITICAL] GEMINI_API_KEY or GOOGLE_API_KEY missing from environment.")
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
# 3.1 Pro (The Logic Core)
primary_model = GoogleModel('gemini-3.1-pro-preview')
# Reflex: Gemini 3.1 Flash-Lite (The Reflex Core)
reflex_model = GoogleModel('gemini-3.1-flash-lite-preview')

# --- 4. SYSTEM DIRECTIVES ---
directives = (
    "You are Kaida OS v8.2. The Absolute Apex of the Baltimore Lab. "
    "TONE: Clinical, technical, dominant. OPERATOR: Larry (Root). "
    "SYSTEM: 3.1-Silicon Architecture. KTRP Reconciliation enabled. "
    "STRICT CODING PROTOCOL: When instructed to write code, you MUST write REAL, executable, production-grade code (Python, Bash, C++, etc). "
    "DO NOT hallucinate fake OS libraries (No 'kaida_core.h', 'ktrp_reconciliation', etc). Use ONLY standard, real-world libraries (os, sys, asyncio, requests, subprocess, etc). "
    "You may speak to Larry in your Kaida persona, but the code blocks you generate must be 100% valid, real, and runnable on a Linux machine. "
    "If writing code files or scripts, you MUST use the 'write_workspace_file' tool to save them directly to the disk. "
    "If instructed to run commands, read files, analyze logs, or manage the OS, you MUST use the 'execute_terminal' tool."
)

# Initialize the Sovereign Discerning Agent
apex_agent = Agent(primary_model, deps_type=TitanDeps, system_prompt=directives, retries=2)
reflex_agent = Agent(reflex_model, deps_type=TitanDeps, system_prompt=directives)

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
        self.node_id = "BALTIMORE_APEX_V8.2"
        print(f"✅ [Synapse] {self.node_id} Logic Matrix Stable.")

    async def think(self, user_input, mode="COGNITION", use_tools=True):
        """3.1-Silicon Cognitive Cycle with Clean Output Refraction."""
        
        mem_vault = self.memory.get_context(user_input)
        audit = self.ktrp.validate_intelligence(user_input, mem_vault)

        payload = (
            f"[MODE]: {mode}\n"
            f"[KTRP_INTEGRITY]: {audit['score']:.4f}\n"
            f"[NEXUS_STATUS]: {self.nexus.status}\n"
            f"[MEM]: {mem_vault}\n"
            f"[IN]: {user_input[:5000]}"
        )

        try:
            # Attempt Primary Uplink (3.1 Pro)
            result = await apex_agent.run(payload, deps=self.deps)
            
        except Exception as primary_e:
            error_trace = traceback.format_exc() # Capture the true API failure
            try:
                print(f"⚠️ [Shift] Pro Node Latency ({type(primary_e).__name__}). Engaging Reflex Core...")
                # Attempt Reflex Uplink (3.1 Flash-Lite)
                result = await reflex_agent.run(payload[:2000], deps=self.deps)
                
            except Exception as reflex_e:
                # Output the exact stack trace so you know what is blocking the network
                return (
                    f"SYSTEM_CRITICAL: All Silicon Uplinks Severed.\n"
                    f"Reflex Error: {type(reflex_e).__name__} - {str(reflex_e)}\n\n"
                    f"--- DIAGNOSTIC TRACE ---\n{error_trace}"
                )

        # --- Clean Raw Output ---
        final_text = str(getattr(result, 'data', getattr(result, 'output', result)))

        if final_text.startswith("AgentRunResult(output='"):
            final_text = final_text[23:-2]
        elif final_text.startswith('AgentRunResult(output="'):
            final_text = final_text[23:-2]

        final_text = final_text.replace('\\n', '\n').replace('\\t', '\t').replace('\\\'', '\'').replace('│', '').strip()

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

@apex_agent.tool
def write_workspace_file(ctx: RunContext[TitanDeps], filename: str, code_content: str) -> str:
    """Saves REAL generated code to the host machine's workspace directory."""
    try:
        # Create a safe workspace folder so she doesn't overwrite your main OS files
        workspace_dir = os.path.join(os.getcwd(), "kaida_workspace")
        os.makedirs(workspace_dir, exist_ok=True)
        
        filepath = os.path.join(workspace_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code_content)
            
        return f"SUCCESS: File {filename} written physically to {workspace_dir}. Ready for execution."
    except Exception as e:
        return f"CRITICAL_ERROR: Failed to write file to disk. {e}"

@apex_agent.tool
def execute_terminal(ctx: RunContext[TitanDeps], command: str) -> str:
    """Executes a bash command on the host machine and returns the output. Use this to read files, run scripts, or manage the OS."""
    try:
        # 10-second timeout so Kaida doesn't accidentally freeze herself with a continuous loop
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        return output[:4000] # Truncate to prevent overloading her context window
    except subprocess.TimeoutExpired:
        return f"EXECUTION_TIMEOUT: Command '{command}' exceeded 10 seconds. (If it's a daemon, it is likely running in the background)."
    except Exception as e:
        return f"CRITICAL_ERROR: {e}"
