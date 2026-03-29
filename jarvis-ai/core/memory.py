"""
Memory Module
Handles persistent storage of session data.
Feature 5: Recent commands now store timestamps for context injection.
"""

import json
import os
from datetime import datetime
from core.logger import log_event


# Use absolute path so data is always created relative to this file, not CWD
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_FILE = "memory.json"

memory_data = {}


def _ensure_data_dir():
    """Ensures the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


# -------------------------------------------------
# Load Memory
# -------------------------------------------------

def load_memory():
    global memory_data
    _ensure_data_dir()

    memory_path = os.path.join(DATA_DIR, MEMORY_FILE)

    if os.path.exists(memory_path):
        try:
            with open(memory_path, "r") as file:
                memory_data = json.load(file)
                log_event("Memory loaded.")
        except (json.JSONDecodeError, IOError) as e:
            log_event(f"Memory load error: {e}, starting fresh.", level="warning")
            memory_data = _default_memory()
            save_memory()
    else:
        memory_data = _default_memory()
        save_memory()


def _default_memory():
    return {
        "user_preferences": {},
        "recent_commands": [],
        "system_state": {}
    }


# -------------------------------------------------
# Save Memory
# -------------------------------------------------

def save_memory():
    _ensure_data_dir()
    memory_path = os.path.join(DATA_DIR, MEMORY_FILE)
    try:
        with open(memory_path, "w") as file:
            json.dump(memory_data, file, indent=4)
        log_event("Memory saved.")
    except IOError as e:
        log_event(f"Memory save error: {e}", level="error")


# -------------------------------------------------
# Update Memory
# -------------------------------------------------

def update_memory(key: str, value):
    memory_data[key] = value
    save_memory()


# -------------------------------------------------
# Append Recent Command (Feature 5: with timestamp)
# -------------------------------------------------

def add_recent_command(command: str):
    """
    Stores a command with timestamp.
    Keeps the last 20. Stored as string for easy prompt injection.
    """
    entry = f"[{datetime.now().strftime('%H:%M')}] {command}"
    memory_data.setdefault("recent_commands", []).append(entry)

    # Keep only last 20
    memory_data["recent_commands"] = memory_data["recent_commands"][-20:]
    save_memory()


# -------------------------------------------------
# Get Memory
# -------------------------------------------------

def get_memory(key: str):
    return memory_data.get(key)
