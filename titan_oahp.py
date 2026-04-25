import time

class OAHP:
    """Operator-Aligned Heuristics Protocol v1.0 [Directed Agency]"""
    def __init__(self, brain_instance, ktrp_instance):
        self.brain = brain_instance
        self.ktrp = ktrp_instance
        self.current_directive = None
        self.active_plan = []

    def log(self, message, status="ACTIVE"):
        timestamp = time.strftime("%H:%M:%S")
        print(f"📡 [OAHP] [{status}] {message}")

    def generate_action_plan(self, directive):
        """
        Phase 1 & 2: Decomposition and Formulation.
        Uses the Logic Core to break down abstract goals into KTRP-verified steps.
        """
        self.current_directive = directive
        self.log(f"Decomposing Directive: '{directive[:40]}...'", "PHASE_1")

        # We ask the Brain to act as the Architect
        planning_prompt = f"""
        [OAHP_DIRECTIVE]: {directive}
        [SYSTEM]: You are the Baltimore Architect. 
        [TASK]: Decompose this directive into 4 discrete, technical sub-problems.
        For each sub-problem, define an ACTION and a KTRP_VERIFICATION requirement.
        
        Return ONLY a JSON list of steps:
        [
          {{"step": 1, "task": "...", "action": "...", "verification": "..."}},
          ...
        ]
        """
        
        raw_plan = self.brain.think(planning_prompt, use_tools=False)
        
        try:
            # Clean and parse the plan
            import json
            clean_json = raw_plan.strip().replace("```json", "").replace("```", "")
            self.active_plan = json.loads(clean_json)
            self.log("Action Plan Formulated.", "AWAITING_EXEC")
            return self.active_plan
        except Exception as e:
            self.log(f"Decomposition Error: {e}", "RECOVERY")
            return None

    def execute_step(self, step_index):
        """Phase 3: Execution of a specific plan component."""
        if step_index >= len(self.active_plan): return "INVALID_STEP"
        
        step = self.active_plan[step_index]
        self.log(f"Executing Step {step_index + 1}: {step['task']}", "EXECUTING")
        
        # In this build, 'Execution' is the synthesis of the solution via the Brain
        result = self.brain.think(f"EXECUTE OAHP TASK: {step['task']} | ACTION: {step['action']}")
        return result
