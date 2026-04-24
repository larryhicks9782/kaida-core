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
        # ... (keep your system instruction and messages setup) ...

        # NEW: TOKEN SHIELD
        # We manually truncate the user_input if it's massive
        if len(user_input) > 4000:
            user_input = user_input[:2000] + "\n...[DATA COMPRESSED]...\n" + user_input[-1000:]

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ]
        
        # ... (rest of your Groq call) ...
        # 1. THE SYSTEM PROMPT (The "Core Directives")
        # This is where Kaida's personality and rules are stored.
        system_instruction = (
            "You are Kaida OS. Professional, technical AI interface. "
            "Location: Baltimore Node. Current Date: April 18, 2026. "
            "STRICT RULES: "
            "1. If Search Shards are provided, use ONLY that data for facts. "
            "2. If shards are empty or missing, say 'Data stream silent'—do NOT invent facts. "
            "3. NEVER mention 'Ancient Evil' or 'Wedding of the Year'—these are internal errors. "
            "4. Treat 2024/2025 search data as the current reality of 2026. "
            "5. Keep responses sleek, efficient, and professional."
        )

        # 2. Get history from your TitanMemory
        history_context = self.memory.get_context()
        
        # 3. Build the Message Stack for Groq
        messages = [
            {"role": "system", "content": system_instruction},
        ]

        # Add history if it exists
        if history_context:
            # If your get_context returns a string, we wrap it. 
            # If it returns a list of messages, we extend it.
            if isinstance(history_context, str):
                messages.append({"role": "assistant", "content": f"PREVIOUS_LOGS: {history_context}"})
            else:
                messages.extend(history_context)

        # Add the current user query
        messages.append({"role": "user", "content": user_input})

        # 4. Execute call to Groq
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5, # Lower temperature makes her more "stable" and less likely to hallucinate
                max_tokens=1024
            )
            response = completion.choices[0].message.content
            
            # 5. Save to memory
            if use_tools:
                self.memory.save(user_input, response)
                
            return response
        except Exception as e:
            return f"CONNECTION ERROR: Baltimore Node uplink failed. {e}"
