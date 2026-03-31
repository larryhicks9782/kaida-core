# --- TITAN CORE : FOUNDATION ---

# 1. The Shield State
shield_active = True

# 2. The Command Map (The Brain's Vocabulary)
commands = {
    "start": "SYSTEM INITIALIZING...",
    "shield": "ROTATING ENCRYPTION KEYS...",
    "status": "ALL SECTORS CLEAR.",
    "emergency": "PURGING LOCAL MEMORY!"
}

# 3. The Interactive Gate (The "Sensor")
print(" --- Titan Brain Active --- ")
user_input = input("Enter Command: ")

# 4. The Logic Processor
# result looks at the commands dictionary using your input
result = commands.get(user_input.lower(), "UNKNOWN COMMAND - ACCESS DENIED.")

print(result)

