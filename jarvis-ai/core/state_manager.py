"""
State Manager
Maintains live system awareness and contextual state.
"""

import sys
import psutil
from datetime import datetime
from core.logger import log_event
from core.memory import update_memory

# Global state container
system_state = {
    "cpu": 0,
    "ram": 0,
    "disk": 0,
    "active_tasks": [],
    "last_update": None
}

def _get_disk_path():
    """Returns the correct root disk path for the current OS."""
    if sys.platform == "win32":
        return "C:\\"
    return "/"


# -------------------------------------------------
# Update Live System State
# -------------------------------------------------

def update_system_state():
    """
    Refreshes live system metrics.
    """

    try:
        system_state["cpu"] = psutil.cpu_percent(interval=1)
        system_state["ram"] = psutil.virtual_memory().percent
        system_state["disk"] = psutil.disk_usage(_get_disk_path()).percent
        system_state["last_update"] = datetime.now().isoformat()  # Fixed: was psutil.boot_time()

        log_event("System state updated.")

        # Persist snapshot to memory
        update_memory("system_state", system_state)

    except Exception as e:
        log_event(f"State update error: {str(e)}", level="error")


# -------------------------------------------------
# Add Active Task
# -------------------------------------------------

def add_active_task(task_name: str):
    if task_name not in system_state["active_tasks"]:
        system_state["active_tasks"].append(task_name)
        update_memory("system_state", system_state)


# -------------------------------------------------
# Remove Active Task
# -------------------------------------------------

def remove_active_task(task_name: str):
    if task_name in system_state["active_tasks"]:
        system_state["active_tasks"].remove(task_name)
        update_memory("system_state", system_state)


# -------------------------------------------------
# Get Current State
# -------------------------------------------------

def get_system_state():
    return system_state
