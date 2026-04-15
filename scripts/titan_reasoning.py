import random
# Make sure you are importing your model class
from titan_brain import TitanBrain

class ReasoningEngine:
    def __init__(self, brain_instance):
        self.brain = brain_instance
        brain_instance = TitanBrain() 



    def get_tot_response(self, prompt, **kwargs):
    # This will now catch 'search_context' inside the kwargs dictionary
        search_context = kwargs.get('search_context', "No web data provided.")
    
    # Logic follows...
        return f"Processed prompt: {prompt} with context."

    def get_tot_response(self, prompt, search_context=None):
        """
        TOT (Tree of Thought) Logic: 
        Uses the prompt and optional search context to reason.
        """
        # Integrate the search data into the reasoning flow
        if search_context:
            full_query = f"CONTEXT: {search_context}\n\nUSER REQUEST: {prompt}"
        else:
            full_query = prompt
            
        # Call your LLM/Groq logic here
        return f"Reasoning processed for: {full_query[:50]}..."

    def get_tot_response(self, prompt, search_context, branches=3, depth=2):
        """
        prompt: The user's question
        search_context: The REAL data found by TitanWeb
        """
        print(f"\n[ToT System]: Grounding analysis in live data...")
        
        # We start by forcing the first thought to be based on the search results
        thoughts = [
            f"Fact-based Plan {i+1}: Use these search results: {search_context} to answer: {prompt}" 
            for i in range(branches)
        ]
        
        for d in range(depth):
            print(f"[ToT System]: Expanding depth {d+1}...")
            new_thoughts = []
            for thought in thoughts:
                # GROUNDING STEP: We tell the brain it MUST use the context provided
                grounded_prompt = (
                    f"You are Kaida. Use this verified web data: {search_context}. "
                    f"Evaluate and expand this specific thought: {thought}. "
                    f"If the data doesn't mention it, do not invent it."
                )
                
                expansion = self.brain.think(grounded_prompt)
                new_thoughts.append(expansion)
            
            # Keep the most 'realistic' branches
            thoughts = random.sample(new_thoughts, min(len(new_thoughts), branches))

        return thoughts[0]
    def get_tot_response(self, prompt, branches=3, depth=2):
        print(f"\n[ToT System]: Analyzing {branches} branches...")
        
        # Level 1: Initial thoughts
        thoughts = [f"Plan {i+1}: {prompt}" for i in range(branches)]
        
        for d in range(depth):
            print(f"[ToT System]: Expanding depth {d+1}...")
            new_thoughts = []
            for thought in thoughts:
                # Get expansion from the model
                expansion = self.brain.think(f"Expand this idea: {thought}")
                new_thoughts.append(expansion)
            
            # Keep only the best branches
            thoughts = random.sample(new_thoughts, min(len(new_thoughts), branches))

        # This MUST line up with 'for d in range'
        return thoughts[0]

