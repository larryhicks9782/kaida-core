import os
from groq import Groq
from titan_memory import MemoryManager # Importing your new separate file
from titan_ui import TitanUI
from rich.prompt import Prompt
from titan_reasoning import ReasoningEngine

class TitanBrain:
    def __init__(self):
        # ... (existing init code)
        self.reasoner = ReasoningEngine(self)
        self.use_tot = False  # Toggle this on/off

    def think(self, prompt):
        # --- Add this block ---
        if prompt.lower().startswith("/tot "):
            self.use_tot = not self.use_tot
            return f"Tree of Thought mode is now {'ON' if self.use_tot else 'OFF'}."
        
        if self.use_tot:
            return self.reasoner.get_tot_response(prompt)

        def think(self, prompt):
            print(f"DEBUG: use_tot is {self.use_tot}")

        # Handle the /tot command
        if prompt.strip().lower() == "/tot":
            self.use_tot = not self.use_tot
            # Make sure this line is complete:
            return f"ToT is now {'ON' if self.use_tot else 'OFF'}"

        # If ToT is active, use the reasoner
        if self.use_tot:
            print("DEBUG: Entering Reasoning Engine...")
            self.reasoner.get_tot_response(prompt)
        # Your standard code continues below...

class TitanBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.memory = MemoryManager()
        self.history = []
        self.ui = TitanUI()
        self.modes = {
            "default": "You are Kaida. Be helpful, concise, and friendly.",
            "serious": "You are Kaida, the analytical assistant. Be direct, factual, and strictly objective.",
            "creative": "You are Kaida, the creative muse. Use metaphors and be imaginative.",
            "humorous": "You are Kaida, the witty companion. Use humor and playful banter."
        }
        self.current_mode = "default"

    def think(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        if len(self.history) > 10: self.history.pop(0)

        self.modes["default"] = """
You are Kaida. For complex questions, follow this process:
1. Analyze the user's intent.
2. Break the task into 2-3 logical steps.
3. Think through each step quietly.
4. Provide the final, accurate answer.
Always "show your work" before giving the conclusion.
"""

        self.modes = {
    "default": (
        "You are Kaida. You are a long-term assistant for Larry. "
        "DO NOT use introductory pleasantries like 'nice to meet you' or 'welcome'. "
        "Recognize that you have a shared history with the user. "
        "Be direct, helpful, and concise."
    ),
    # ... keep the rest of your modes
}


        if user_input.startswith("/mode "):
            mode = user_input.split(" ")[1]
            if mode in brain.modes:
                brain.current_mode = mode
                brain.ui.show_response(f"Personality switched to {mode}.")
            else:
                brain.ui.show_response("Available modes: default, serious, creative, humorous.")

        context = self.memory.get_context()
        messages = [{"role": "system", "content": f"You are Kaida. Info: {context}"}] + self.history
        system_content = f"{self.modes[self.current_mode]} Info: {context}"
        messages = [{"role": "system", "content": system_content}] + self.history
        completion = self.client.chat.completions.create(messages=messages, model=self.model)
        response = completion.choices[0].message.content

        self.history.append({"role": "assistant", "content": response})
        return response

if __name__ == "__main__":
    brain = TitanBrain()
    # Use your UI design for the header
    brain.ui.show_header() 
    
    while True:
        # Using standard input but then passing it to the UI
        user_input = Prompt.ask("[bold green]You[/bold green]")
        
        if user_input.lower() == 'quit':
            brain.memory.archive_session(brain.history, brain.client, brain.model)
            break
        
        # This is where the magic happens:
        # 1. Show the status animation
        with brain.ui.show_status():
            response = brain.think(user_input)
            
        # 2. Show the fancy panel response
        brain.ui.show_response(response)


