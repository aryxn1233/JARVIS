"""
Memory Module
Handles persistent storage of session data.
"""

import json
import os
from core.logger import log_event


DATA_DIR = "data"
MEMORY_FILE = "memory.json"

memory_data = {}


# -------------------------------------------------
# Load Memory
# -------------------------------------------------

def load_memory():
    global memory_data

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    memory_path = os.path.join(DATA_DIR, MEMORY_FILE)

    if os.path.exists(memory_path):
        with open(memory_path, "r") as file:
            memory_data = json.load(file)
            log_event("Memory loaded.")
    else:
        memory_data = {
            "user_preferences": {},
            "recent_commands": [],
            "system_state": {}
        }
        save_memory()


# -------------------------------------------------
# Save Memory
# -------------------------------------------------

def save_memory():
    memory_path = os.path.join(DATA_DIR, MEMORY_FILE)

    with open(memory_path, "w") as file:
        json.dump(memory_data, file, indent=4)

    log_event("Memory saved.")


# -------------------------------------------------
# Update Memory
# -------------------------------------------------

def update_memory(key: str, value):
    memory_data[key] = value
    save_memory()


# -------------------------------------------------
# Append Recent Command
# -------------------------------------------------

def add_recent_command(command: str):
    memory_data.setdefault("recent_commands", []).append(command)

    # Keep only last 20 commands
    memory_data["recent_commands"] = memory_data["recent_commands"][-20:]

    save_memory()


# -------------------------------------------------
# Get Memory
# -------------------------------------------------

def get_memory(key: str):
    return memory_data.get(key)
