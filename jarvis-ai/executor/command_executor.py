"""
Command Executor
Executes approved action plans safely.
"""

import subprocess
import tempfile
import os
from core.logger import log_event


# -------------------------------------------------
# Main Execution Entry
# -------------------------------------------------

def execute_command(action_plan: dict):
    """
    Executes action plan returned by router.
    """

    execution_type = action_plan.get("execution_type")
    intent = action_plan.get("intent")

    if execution_type == "direct":
        return handle_direct_intent(intent)

    elif execution_type == "script":
        generated_code = action_plan.get("generated_code")
        return execute_generated_script(generated_code)

    else:
        return "Unknown execution type."
    

# -------------------------------------------------
# Direct System Intent Handler
# -------------------------------------------------

def handle_direct_intent(intent: str):
    """
    Maps known intents to Linux commands.
    """

    try:
        if intent == "shutdown":
            subprocess.run(["sudo", "shutdown", "now"])
            return "System shutting down."

        elif intent == "restart":
            subprocess.run(["sudo", "reboot"])
            return "System restarting."

        elif intent == "list_processes":
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            return result.stdout[:1000]  # limit output size

        elif intent == "check_cpu":
            result = subprocess.run(["top", "-bn1"], capture_output=True, text=True)
            return result.stdout[:1000]

        elif intent == "check_disk":
            result = subprocess.run(["df", "-h"], capture_output=True, text=True)
            return result.stdout

        else:
            return f"No direct handler for intent: {intent}"

    except Exception as e:
        log_event(f"Execution error: {str(e)}")
        return "Execution failed."


# -------------------------------------------------
# AI-Generated Script Execution (Sandboxed)
# -------------------------------------------------

def execute_generated_script(code: str):
    """
    Executes AI-generated script in temporary file.
    """

    if not code:
        return "No script generated."

    # Basic safety filter
    if is_dangerous(code):
        log_event("Blocked potentially dangerous script.")
        return "Script blocked due to unsafe content."

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sh") as temp_script:
            temp_script.write(code.encode())
            temp_script_path = temp_script.name

        os.chmod(temp_script_path, 0o755)

        result = subprocess.run(
            [temp_script_path],
            capture_output=True,
            text=True
        )

        os.remove(temp_script_path)

        log_event("Script executed successfully.")
        return result.stdout[:1000]

    except Exception as e:
        log_event(f"Script execution error: {str(e)}")
        return "Script execution failed."


# -------------------------------------------------
# Safety Filter
# -------------------------------------------------

def is_dangerous(code: str) -> bool:
    """
    Basic filtering for destructive commands.
    """

    dangerous_keywords = [
        "rm -rf /",
        "mkfs",
        "dd if=",
        ">:",
        "shutdown",
        "reboot",
        "iptables -F",
        "chmod 777 /"
    ]

    for keyword in dangerous_keywords:
        if keyword in code:
            return True

    return False
