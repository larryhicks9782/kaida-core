import random

class ReasoningEngine:
    def __init__(self, brain_instance):
        self.brain = brain_instance

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

