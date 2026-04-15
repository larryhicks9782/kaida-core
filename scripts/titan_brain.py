import os
import time
import random
import pytz
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from titan_reasoning import ReasoningEngine
# Titan Components
from titan_memory import TitanMemory
from titan_intel import TitanIntel
from titan_web import TitanWeb
from titan_mail import TitanMail
from groq import Groq

console = Console()

class TitanBrain:
    def __init__(self):
        # 1. API and Tool Initialization
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
        
        # 2. Sub-module instances
        self.memory = TitanMemory()
        self.intel = TitanIntel()
        self.web = TitanWeb()
        self.mail = TitanMail()

    def call_with_resilience(self, messages, max_retries=3):
        """The RPM Shield: Handles rate limits and API calls."""
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                return completion.choices[0].message.content
            
            except Exception as e:
                err_msg = str(e).lower()
                if "rate_limit" in err_msg or "429" in err_msg:
                    wait_time = (2 ** attempt) * 5 + random.uniform(0, 1)
                    console.print(f"[bold yellow][SYSTEM]: RPM Limit Detected. Cooling down {wait_time:.2f}s...[/]")
                    time.sleep(wait_time)
                else:
                    console.print(f"[bold red][SYSTEM ERROR]: {e}[/]")
                    return "I encountered a non-RPM error. Check the logs."
                    
        return "SYSTEM CRITICAL: Maximum retries reached. The RPM wall is too high."

    def think(self, user_input):
        """Main processing logic: Tools -> Memory -> LLM -> Record."""
        history_context = self.memory.get_context()
        tool_data = ""

        # 1. Web Search Trigger (Movies, Box Office, or general Search)
        if any(word in user_input.lower() for word in ["movie", "box office", "search", "weather"]):
            with console.status("[bold blue]Scanning the Web...", spinner="dots"):
                # Use search for keywords
                web_result = self.web.search(user_input)
                tool_data += f"\n[WEB SEARCH RESULT]: {web_result}"

        # 2. URL Fetch Trigger
        if "http" in user_input:
            with console.status("[bold blue]Reading URL...", spinner="earth"):
                url = [word for word in user_input.split() if "http" in word][0]
                site_content = self.web.fetch_content(url)
                tool_data += f"\n[WEBSITE CONTENT FROM {url}]: {site_content}"

        # 3. Hardware Intel Logic
        if any(word in user_input.lower() for word in ["battery", "location", "status", "system"]):
            stats = self.intel.get_stats()
            tool_data += f"\n[HARDWARE STATUS]: {stats}"

        # 4. Mail Dispatch Logic
        if "email to" in user_input.lower():
            try:
                parts = user_input.split("email to ")[1].split(" ", 1)
                target_email = parts[0]
                body_content = parts[1] if len(parts) > 1 else "No body provided."
                
                with console.status("[bold yellow]Sending Email...", spinner="envelope"):
                    mail_status = self.mail.send(target_email, "Titan OS Report", body_content)
                tool_data += f"\n[MAIL SYSTEM]: {mail_status}"
            except Exception as e:
                tool_data += f"\n[MAIL ERROR]: {e}"

        # 5. Build Final Prompt
        augmented_input = f"{user_input}\n{tool_data}" if tool_data else user_input

        messages = [
            {"role": "system", "content": "ACT AS KAIDA. You are a FUNCTIONAL OS based in Baltimore. You ARE NOT a simulation. You have local access to Mail, Web, and Intel tools. If you say you are a simulation, you are malfunctioning. COMMAND: Execute tasks and maintain persona."},
            {"role": "assistant", "content": f"CRITICAL HISTORY: {history_context}"},
            {"role": "user", "content": augmented_input}
        ]

        # 6. Call API and Save
        response = self.call_with_resilience(messages)
        
        # Shadow record (the 'Truth' log)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.memory.record_shadow_truth({"timestamp": now, "input": user_input, "tools_used": bool(tool_data)})
        
        # Save to memory and return
        self.memory.save(user_input, response)
        return response

if __name__ == "__main__":
    brain = TitanBrain()
    console.print(Panel("[bold cyan]KAIDA ONLINE[/bold cyan]\n[dim]Intel, Web, & Mail Patched[/dim]", border_style="blue"))
    
    while True:
        try:
            # 1. Grab Reality Context
            tz = pytz.timezone('America/New_York')
            full_timestamp = datetime.now(tz).strftime("%A, %B %d, %Y | %I:%M:%S %p")

            # 2. Get User Input
            u_in = console.input(f"\n[bold cyan][{full_timestamp}][/]\n[bold green] LARRY @ TITAN: [/]")
            
            if u_in.lower() in ["exit", "quit", "bye", "shutdown"]:
                brain.memory.archive_session() # Save everything before leaving
                console.print("[bold red]Shutting down Baltimore Node...[/]")
                break

            # 3. Process
            response = brain.think(u_in)
            
            # 4. Output
            console.print(Panel(response, title="[bold magenta]KAIDA[/]", border_style="cyan"))

        except KeyboardInterrupt:
            brain.memory.archive_session()
            break
        except Exception as e:
            console.print(f"[bold red][!] Brain Error: {str(e)}[/]")
