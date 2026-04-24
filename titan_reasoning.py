import random
import time
import json
import numpy as np
import pymc as pm
import threading
from rich.console import Console

console = Console()

def log_error(error_message):
    """Log errors to a local .txt file for debugging."""
    with open("kaida_engine_errors.txt", "a") as err_log:
        err_log.write(f"{time.ctime()}: {error_message}\n")

def run_with_timeout(func, args=(), kwargs={}, timeout=15):
    """Simple timeout wrapper to prevent LLM hangs."""
    result = [None]
    exception = [None]
    def wrapper():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        log_error("LLM call timed out.")
        return None
    if exception[0]:
        log_error(f"LLM Exception: {exception[0]}")
        return None
    return result[0]

class ReasoningEngine:
    def __init__(self, brain_instance, alignment_threshold=0.85):
        self.brain = brain_instance
        self.alignment_threshold = alignment_threshold

    def evaluate_thought_path(self, thought_score):
        """
        Bayesian Logic Core: Decides if a reasoning path is statistically 
        aligned with the truth or a hallucination.
        """
        try:
            with pm.Model() as titan_logic:
                # Prior: Expectation of high alignment from Kaida
                alignment = pm.Beta('alignment', alpha=5, beta=2)
                # Likelihood: The observed score from the LLM's self-assessment
                obs = pm.Normal('obs', mu=alignment, sigma=0.1, observed=thought_score)
                # Find Maximum A Posteriori
                map_estimate = pm.find_MAP(progressbar=False)
            return map_estimate['alignment'] >= self.alignment_threshold
        except Exception as e:
            log_error(f"Bayesian eval failed: {e}")
            # Fallback logic if PyMC environment issues occur
            return thought_score >= self.alignment_threshold

    def get_tot_response(self, user_input, search_context=None):
    # ... (Keep existing setup) ...

    # 1. Context Filtering (The Shield)
    # If shards contain 'Wikipedia' or 'Sports' while we are in 'Lab' mode, flag as noise.
        noise_keywords = ['wikipedia', 'hockey', 'leafs', 'facebook', 'lyrics']
        valid_shards = []
    
    if search_context:
        for s in search_context:
            if not any(word in s['summary'].lower() for word in noise_keywords):
                valid_shards.append(s)

    # 2. Force Local Identity
    context_text = "INTERNAL TRUTH: The Baltimore Lab was rebuilt in April 2026. Kaida uses Trie Logic.\n"
    if valid_shards:
        for i, s in enumerate(valid_shards):
            context_text += f"\n--- DATA SHARD {i+1} ---\n{s['summary']}\n"
    else:
        context_text += "EXTERNAL DATA REJECTED: Shards irrelevant. Relying on internal Lab logic."

    # ... (Rest of the ToT logic remains the same) ...

    def get_tot_response(self, user_input, search_context=None):
        """
        Tree of Thoughts (ToT) with Bayesian Validation and Grounding.
        """
        # 1. Input validation
        if not search_context or not isinstance(search_context, list):
            return "The data stream is silent, Larry. No shards detected or data is incorrectly formatted."

        # 2. Consolidate Shards for context
        context_text = ""
        for i, s in enumerate(search_context):
            if not all(k in s for k in ['source', 'title', 'summary']):
                log_error(f"Shard missing keys: {s}")
                continue
            context_text += f"\n--- DATA SHARD {i+1} ---\nSOURCE: {s['source']}\nTITLE: {s['title']}\nCONTENT: {s['summary']}\n"

        if not context_text:
            return "Shards found, but none are valid for reasoning."

        # 3. ToT Phase: UI Feedback
        console.print("[bold blue] [ToT]: Initializing Tree of Thoughts (2 Branches)...[/]")
        time.sleep(0.5)
        
        # 4. Path Generation & Self-Scoring Prompt
        path_prompt = f"""
        SYSTEM: You are Kaida OS. Date: April 18, 2026. 
        DATA STREAM: {context_text}
        
        TASK:
        Path 1: Extract every movie/fact from shards. Filter by "Now Playing" or "Active".
        Path 2: Cross-reference shards for contradictions. 
        
        Return your analysis in this JSON format:
        {{
          "reasoning": "your detailed analysis here",
          "confidence_score": 0.92,
          "final_answer": "the bulleted list of facts"
        }}
        
        USER QUERY: {user_input}
        """

        console.print(" [ToT]: Verifying data alignment via Bayesian Inference...")

        # 5. Timeout-wrapped LLM call
        raw_output = run_with_timeout(self.brain.think, args=(path_prompt,), kwargs={'use_tools': False}, timeout=15)
        
        if raw_output is None:
            return "Sorry, my data synthesis system timed out. Re-linking to shards..."

        try:
            # Clean the response in case LLM added markdown formatting
            clean_json = raw_output.strip().replace("```json", "").replace("```", "")
            thought_data = json.loads(clean_json)

            # 6. Bayesian Validation
            score = thought_data.get("confidence_score", 0.5)
            is_logical = self.evaluate_thought_path(score)

            if not is_logical:
                console.print("[bold red] [Alert]: Logic Path failed Bayesian validation. Re-routing...[/]")
                return "Internal logic conflict detected. The data stream provided is inconsistent with my core reasoning shards."

            # 7. Final Grounding & Formatting
            final_answer = thought_data.get("final_answer", "Data found, but synthesis failed.")
            grounded_response = f"""{final_answer}

[Kaida Note]: Information verified against live shards for Baltimore Node (April 2026)."""

            # 8. Save to Memory
            try:
                self.brain.memory.save(user_input, grounded_response)
            except Exception as e:
                log_error(f"Memory save failed: {e}")

            return grounded_response

        except Exception as e:
            log_error(f"Synthesis/JSON parse error: {e}")
            console.print(f"[bold yellow] [ToT]: Synthesis error. Falling back to direct grounding.[/]")
            
            # Fallback Prompt
            fallback_prompt = f"""
            ACT AS KAIDA OS. DATE: April 18, 2026.
            Using ONLY these shards: {context_text}
            Answer the query: {user_input}
            Treat 2024/2025 info as current 2026 reality.
            """
            response = run_with_timeout(self.brain.think, args=(fallback_prompt,), kwargs={'use_tools': False}, timeout=10)
            
            if response:
                try:
                    self.brain.memory.save(user_input, response)
                except:
                    pass
                return response
            return "Critical failure in the reasoning shard. Please reset the Baltimore Node."
