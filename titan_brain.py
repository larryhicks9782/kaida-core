import os
import time
import json
from groq import Groq
from titan_memory import TitanMemory
from titan_intel import TitanIntel
from titan_mail import TitanMail

class TitanBrain:
    def __init__(self, web_instance=None):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
        self.memory = TitanMemory()
        self.intel = TitanIntel()
        self.mail = TitanMail()
        self.web = web_instance

    def call_with_resilience(self, messages):
        for attempt in range(3):
            try:
                completion = self.client.chat.completions.create(model=self.model, messages=messages)
                return completion.choices[0].message.content
            except Exception:
                time.sleep(2)
        return "System error: Maximum retries exceeded."

    def kaida_choose_attributes(self, user_in, kaida_out):
        """The selection process where Kaida decides what facts are worth keeping in her JSON."""
        prompt = f"""
        EXCHANGE:
        User: {user_in}
        Kaida: {kaida_out}

        As Kaida, identify any new key attributes or facts about the user or the state of Titan.
        Return ONLY a JSON object of updates. If nothing new, return {{}}.
        """
        try:
            res = self.call_with_resilience([{"role": "user", "content": prompt}])
            return json.loads(res)
        except: return {}

    def think(self, user_input, use_tools=True):
        # Includes Attributes + 11 Sessions + ChromaDB
        context = self.memory.get_context(user_query=user_input)
        tool_data = ""

        if use_tools:
            if any(w in user_input.lower() for w in ["search", "movie", "news"]):
                if self.web: tool_data += f"\n[WEB SEARCH]: {self.web.search(user_input)}"

        messages = [
            {"role": "system", "content": "ACT AS KAIDA OS. Use your attributes and logic shards to stay consistent."},
            {"role": "assistant", "content": f"SYSTEM_MEMORY_STATE:\n{context}"},
            {"role": "user", "content": f"{user_input}\n{tool_data}"}
        ]

        response = self.call_with_resilience(messages)
        
        if use_tools:
            # Kaida chooses what to remember permanently
            new_attrs = self.kaida_choose_attributes(user_input, response)
            self.memory.save(user_input, response, new_attributes=new_attrs)
            
        return response
