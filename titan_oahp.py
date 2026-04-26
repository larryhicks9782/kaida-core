import time
import json

class OAHP:
    """Operator-Aligned Heuristics Protocol [Async v8.0]"""
    def __init__(self, brain_instance):
        self.brain = brain_instance
        self.active_plan = []

    async def generate_action_plan(self, directive: str):
        prompt = f"[DIRECTIVE]: {directive}\n[TASK]: Decompose into 4 technical steps. Return ONLY a JSON list."
        raw = await self.brain.think(prompt, mode="PLANNING")
        try:
            # Cleaning the 3.1 output for JSON parsing
            clean = raw.strip().replace("```json", "").replace("```", "")
            self.active_plan = json.loads(clean)
            return self.active_plan
        except: return None

    async def execute_step(self, index: int):
        if index < len(self.active_plan):
            task = self.active_plan[index]['task']
            return await self.brain.think(f"EXECUTE_DIRECTIVE_TASK: {task}")
        return "ERR_INVALID_STEP"
