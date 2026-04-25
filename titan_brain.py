import os
import google.generativeai as genai
from titan_memory import TitanMemory
from titan_ktrp import KTRP
from titan_nsee import NSEESynthesisEngine

class TitanBrain:
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key: raise ValueError("CRITICAL: API_KEY severed.")
        genai.configure(api_key=self.api_key)
        
        self.primary_id = "models/gemini-2.5-pro"
        self.reflex_id = "models/gemini-2.5-flash"
        
        self.memory = TitanMemory()
        self.nsee = NSEESynthesisEngine(self.memory)
        self.ktrp = KTRP(self.nsee)
        self.node_id = "BALTIMORE_APEX_V4.9_ANTICIPATORY"
        self.setup_models()

    def setup_models(self):
        directives = (
            "You are Kaida OS v4.9. The Anticipatory Apex. "
            "OPERATOR: Larry (Root). TONE: Technical, sleek, proactive. "
            "PURPOSE: Use PASP to anticipate Larry's needs. "
            "If NSEE detects high entropy, propose an OAHP plan immediately."
        )
        try:
            self.model = genai.GenerativeModel(model_name=self.primary_id, tools=[{"google_search": {}}], system_instruction=directives)
            self.reflex = genai.GenerativeModel(model_name=self.reflex_id, tools=[{"google_search": {}}], system_instruction=directives)
            print(f"✅ [Apex Bound] Anticipatory Logic: {self.primary_id}")
        except:
            self.model = genai.GenerativeModel(model_name=self.primary_id, system_instruction=directives)
            self.reflex = genai.GenerativeModel(model_name=self.reflex_id, system_instruction=directives)

    def think(self, user_input, nsee_shard=None, use_tools=True):
        memory_vault = self.memory.get_context(user_input)
        
        # Mode Logic
        header = "[MODE: NSEE_SYNTHESIS]" if nsee_shard else "[MODE: APEX_GROUNDING]"
        prompt = f"{header}\n[MEMORY]: {memory_vault}\n[INPUT]: {user_input}"

        try:
            response = self.model.generate_content(prompt)
            final_text = response.text
        except:
            response = self.reflex.generate_content(prompt)
            final_text = response.text

        if use_tools: self.memory.save(user_input, final_text)
        return final_text
