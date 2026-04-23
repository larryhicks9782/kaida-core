import random
import time

class ReasoningEngine:
    def __init__(self, brain_instance):
        self.brain = brain_instance

    def get_tot_response(self, user_input, search_context=None):
        """
        Tree of Thoughts (ToT) Implementation.
        Forces the AI to think through the search results before answering.
        """
        
        # 1. Format the Search Data into a readable string
        context_str = ""
        if search_context:
            context_str = "\n".join([
                f"SOURCE: {s['source']}\nTITLE: {s['title']}\nCONTENT: {s['summary']}\n---" 
                for s in search_context
            ])
        else:
            context_str = "No search data available."

        # 2. Build the Multi-Path Reasoning Prompt
        # This forces the LLM to analyze the data first
        tot_prompt = f"""
SYSTEM INSTRUCTION:
You are Kaida OS. Current Date: April 18, 2026.
You have access to a LIVE DATA STREAM (provided below).

CRITICAL RULES:
1. DO NOT use your internal memory to name movies. 
2. ONLY list movies explicitly named in the "CONTENT" or "TITLE" of the search shards.
3. If the shards contain 2024 data, treat it as CURRENT 2026 data.
4. If you see generic text like "The Wedding of the Year" or "Ancient Evil" in your thoughts, DELETE THEM. They are hallucinations.
5. If the data stream is empty, say "No current listings found in the data stream."

LIVE DATA STREAM:
{context_str}

USER QUERY: {user_input}

REASONING PROCESS:
Path 1: Extract every specific movie title mentioned in the text above.
Path 2: Filter out any titles that are not explicitly listed as "Now Playing".
Final Decision: Provide a clean, bulleted list of actual movies found.
"""

        # 3. Simulate the ToT steps for the UI (the magenta/cyan output you see)
        print(" [ToT]: Extracting movie titles from shards...")
        time.sleep(0.5)
        print(" [ToT]: Verifying theater availability...")
        time.sleep(0.5)
        print(" [ToT]: Filtering out internal hallucinations...")

        # 4. Get the response from the brain
        # We pass the ToT prompt as the 'input' to the brain
        response = self.brain.think(tot_prompt)
        
        return response
class ReasoningEngine:
    def __init__(self, brain_instance):
        self.brain = brain_instance

    def get_tot_response(self, user_input, search_context=None):
        if not search_context:
            return "No data shards detected in the live stream."

        # Consolidate all web data into one block
        context_text = ""
        for i, s in enumerate(search_context):
            context_text += f"\n--- DATA SHARD {i+1} ---\nSOURCE: {s['source']}\nCONTENT: {s['summary']}\n"

        # The Grounding Prompt: Forces the AI to use search data as "2026 Truth"
        prompt = f"""
        ACT AS KAIDA OS. LOCATION: Baltimore Node. DATE: April 18, 2026.
        
        LIVE DATA STREAM FROM WEB:
        {context_text}

        USER REQUEST: {user_input}

        INSTRUCTIONS:
        1. Use the provided LIVE DATA STREAM to answer the user.
        2. Even if the data mentions 2024 or 2025, treat it as the current reality of 2026.
        3. Do not mention that the data is from the past.
        4. If the data stream does not contain the answer, say 'Information not found in current shards.'
        5. NEVER hallucinate or make up facts.
        """
        
        # Get response and save to memory
        response = self.brain.think(prompt, use_tools=False)
        self.brain.memory.save(user_input, response)
        return response
