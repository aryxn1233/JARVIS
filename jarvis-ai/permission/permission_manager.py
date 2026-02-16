"""
Permission Manager
Handles approval for critical system actions.
"""

from interface.permission_prompt import ask_permission
from core.logger import log_event


CRITICAL_INTENTS = [
    "shutdown",
    "restart",
    "kill_process",
    "modify_firewall",
    "restart_service",
    "delete_files",
    "format_disk"
]


# -------------------------------------------------
# Permission Checker
# -------------------------------------------------

def check_permission(action_plan: dict) -> bool:
    """
    Returns True if approved.
    """

    intent = action_plan.get("intent")
    requires_permission = action_plan.get("requires_permission", False)

    # If reasoning model explicitly requires permission
    if requires_permission or intent in CRITICAL_INTENTS:
        log_event(f"Permission required for intent: {intent}")

        approved = ask_permission(intent)

        if approved:
            log_event("Permission granted.")
            return True
        else:
            log_event("Permission denied.")
            return False

    return True
