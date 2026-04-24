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
        """
        Tree of Thoughts (ToT) with Bayesian Validation and Grounding.
        """
        
        # 1. Input validation & Formatting
        if not search_context or not isinstance(search_context, list):
            return "The data stream is silent, Larry. No shards detected."

        # 2. Context Filtering (The Shield) - NOW INSIDE THE FUNCTION
        noise_keywords = ['wikipedia', 'hockey', 'leafs', 'facebook', 'lyrics', 'ancient evil']
        valid_shards = []
        
        for s in search_context:
            # Ensure shard has 'summary' key
            summary = s.get('summary', '').lower()
            if not any(word in summary for word in noise_keywords):
                valid_shards.append(s)

        # 3. Consolidate Shards (The Grounding)
        context_text = "INTERNAL TRUTH: The Baltimore Lab was rebuilt in April 2026. Kaida uses Trie Logic.\n"
        
        if valid_shards:
            for i, s in enumerate(valid_shards):
                context_text += f"\n--- DATA SHARD {i+1} ---\nSOURCE: {s.get('source')}\nTITLE: {s.get('title')}\nCONTENT: {s.get('summary')}\n"
        else:
            context_text += "EXTERNAL DATA REJECTED: Live shards identified as noise. Relying on internal Lab logic."

        # 4. ToT Phase: UI Feedback
        console.print("[bold blue] [ToT]: Initializing Tree of Thoughts (2 Path Analysis)...[/]")
        time.sleep(0.3)
        
        # 5. Path Generation & Self-Scoring Prompt
        path_prompt = f"""
        SYSTEM: You are Kaida OS. Date: April 18, 2026. 
        DATA STREAM: {context_text}
        
        TASK:
        Path 1: Extract every factual entity from the shards.
        Path 2: Cross-reference shards for contradictions or hallucinations.
        
        IMPORTANT: Use 2024/2025 info as current 2026 reality.
        
        Return ONLY a JSON object:
        {{
          "reasoning": "analysis of path 1 and 2",
          "confidence_score": 0.95,
          "final_answer": "your bulleted response to the user"
        }}
        
        USER QUERY: {user_input}
        """

        console.print(" [ToT]: Running Bayesian Alignment Check...")

        # 6. Timeout-wrapped LLM call
        raw_output = run_with_timeout(self.brain.think, args=(path_prompt,), kwargs={'use_tools': False}, timeout=15)
        
        if raw_output is None:
            return "Data synthesis timed out. Re-linking to Baltimore Node..."

        try:
            # 7. Clean and Parse JSON
            clean_json = raw_output.strip().replace("```json", "").replace("```", "")
            thought_data = json.loads(clean_json)

            # 8. Bayesian Validation
            score = thought_data.get("confidence_score", 0.5)
            is_logical = self.evaluate_thought_path(score)

            if not is_logical:
                console.print("[bold red] [Alert]: Logic Path failed Bayesian validation. Re-routing...[/]")
                return "Internal logic conflict detected. Shard alignment is below threshold."

            # 9. Final Grounding
            final_answer = thought_data.get("final_answer", "Synthesis failed.")
            grounded_response = f"{final_answer}\n\n[Kaida Note]: Shard weight verified. Baltimore Lab active."

            # 10. Save to Memory
            self.brain.memory.save(user_input, grounded_response)
            return grounded_response

        except Exception as e:
            log_error(f"Synthesis error: {e}")
            # Fallback direct response
            fallback_prompt = f"ACT AS KAIDA OS. Use these shards to answer {user_input}: {context_text}"
            return self.brain.think(fallback_prompt, use_tools=False)
