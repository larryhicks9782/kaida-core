from groq import Groq
try:
    from titan_system.memory_vault import MemoryVault
except ImportError:
    import sys
    sys.path.append("/root/titan_system")
    from memory_vault import MemoryVault

class TitanInterface:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.vault = MemoryVault()
        self.identity = self.vault.get_identity()

    def ask(self, user_input):
        system_prompt = f"You are {self.identity} at the Baltimore Node. Answer the Architect with loyalty."
        # Swapping to the modern 70B Versatile engine
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_input}]
        )
        return completion.choices[0].message.content
