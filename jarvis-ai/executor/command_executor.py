"""
Command Executor
Executes approved action plans safely — cross-platform (Windows + Linux).
Features: direct intents, AI-generated scripts, open apps, web search.
"""

import sys
import subprocess
import tempfile
import os
import re
from core.logger import log_event


# -------------------------------------------------
# Main Execution Entry
# -------------------------------------------------

def execute_command(action_plan: dict):
    """
    Executes action plan returned by router.
    """
    execution_type = action_plan.get("execution_type")
    intent = action_plan.get("intent", "")
    parameters = action_plan.get("parameters", {})

    if execution_type == "direct":
        return handle_direct_intent(intent, parameters)
    elif execution_type == "script":
        generated_code = action_plan.get("generated_code")
        return execute_generated_script(generated_code)
    else:
        return "Unknown execution type."


# -------------------------------------------------
# Direct System Intent Handler (Cross-Platform)
# -------------------------------------------------

def handle_direct_intent(intent: str, parameters: dict = None):
    """
    Maps known intents to OS-appropriate actions.
    Supports Windows and Linux.
    """
    if parameters is None:
        parameters = {}

    is_windows = sys.platform == "win32"

    try:
        # ── System Control ────────────────────────────────
        if intent == "shutdown":
            if is_windows:
                subprocess.run(["shutdown", "/s", "/t", "0"])
            else:
                subprocess.run(["sudo", "shutdown", "now"])
            return "System shutting down."

        elif intent == "restart":
            if is_windows:
                subprocess.run(["shutdown", "/r", "/t", "0"])
            else:
                subprocess.run(["sudo", "reboot"])
            return "System restarting."

        # ── Process / Resource Monitoring ────────────────
        elif intent == "list_processes":
            if is_windows:
                result = subprocess.run(["tasklist"], capture_output=True, text=True)
            else:
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            return result.stdout[:1500]

        elif intent == "check_cpu":
            import psutil
            cpu = psutil.cpu_percent(interval=1)
            per_core = psutil.cpu_percent(interval=0, percpu=True)
            return f"CPU Usage: {cpu}% overall | Cores: {per_core}"

        elif intent == "check_disk":
            import psutil
            disk_path = "C:\\" if is_windows else "/"
            disk = psutil.disk_usage(disk_path)
            return (
                f"Disk Usage: {disk.percent}% | "
                f"Used: {disk.used // (1024**3)} GB / "
                f"Total: {disk.total // (1024**3)} GB | "
                f"Free: {disk.free // (1024**3)} GB"
            )

        elif intent == "check_ram":
            import psutil
            ram = psutil.virtual_memory()
            return (
                f"RAM Usage: {ram.percent}% | "
                f"Used: {ram.used // (1024**2)} MB / "
                f"Total: {ram.total // (1024**2)} MB | "
                f"Free: {ram.available // (1024**2)} MB"
            )

        elif intent in ("optimize_cpu", "optimize_ram"):
            if is_windows:
                result = subprocess.run(["tasklist"], capture_output=True, text=True)
            else:
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            return result.stdout[:1500]

        elif intent == "cleanup_disk":
            return handle_direct_intent("check_disk")

        # ── Open App (Feature 1) ──────────────────────────
        elif intent == "open_app":
            app_name = parameters.get("app_name", "").lower().strip()
            return open_application(app_name)

        # ── Web Search (Feature 3) ────────────────────────
        elif intent == "web_search":
            query = parameters.get("query", "").strip()
            if not query:
                return "Please provide a search query."
            from os_layer.web_search import search_web
            return search_web(query)

        # ── Network ──────────────────────────────────────
        elif intent == "wifi_off":
            from os_layer.network_control import wifi_off
            wifi_off()
            return "WiFi turned off."

        elif intent == "wifi_on":
            from os_layer.network_control import wifi_on
            wifi_on()
            return "WiFi turned on."

        else:
            return f"No direct handler for intent: {intent}"

    except Exception as e:
        log_event(f"Execution error: {str(e)}", level="error")
        return "Execution failed."


# -------------------------------------------------
# Feature 1: Open Application
# -------------------------------------------------

def open_application(app_name: str) -> str:
    """
    Opens an application by friendly name.
    Falls back to running the name directly if not in the map.
    """
    from config.app_map import APP_MAP

    is_windows = sys.platform == "win32"
    platform_key = "win" if is_windows else "linux"

    # Try exact match first, then partial match
    entry = APP_MAP.get(app_name)
    if not entry:
        for key, val in APP_MAP.items():
            if key in app_name or app_name in key:
                entry = val
                break

    if entry:
        executable = entry[platform_key]
    else:
        # Try running name directly as a fallback
        executable = app_name
        log_event(f"App '{app_name}' not in map, trying directly.", level="warning")

    try:
        # Handle ms-settings: URLs on Windows
        if executable.startswith("ms-"):
            subprocess.Popen(["explorer.exe", executable], shell=False)
        elif is_windows:
            subprocess.Popen(executable, shell=True)
        else:
            subprocess.Popen(executable.split(), start_new_session=True)

        log_event(f"Launched app: {executable}")
        return f"Opening {app_name}."

    except FileNotFoundError:
        return f"Could not find '{app_name}'. Make sure it's installed and in your PATH."
    except Exception as e:
        log_event(f"App launch error: {e}", level="error")
        return f"Failed to open {app_name}: {e}"


# -------------------------------------------------
# AI-Generated Script Execution
# -------------------------------------------------

def execute_generated_script(code: str):
    """
    Executes AI-generated Python script in a temporary file.
    """
    if not code:
        return "No script generated."

    if is_dangerous(code):
        log_event("Blocked potentially dangerous script.")
        return "Script blocked due to unsafe content."

    is_windows = sys.platform == "win32"
    suffix = ".py"
    interpreter = [sys.executable]
    temp_script_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, mode="w", encoding="utf-8"
        ) as temp_script:
            temp_script.write(code)
            temp_script_path = temp_script.name

        result = subprocess.run(
            interpreter + [temp_script_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        log_event("Script executed successfully.")
        output = result.stdout[:1000]
        if result.returncode != 0 and result.stderr:
            output += f"\n[stderr]: {result.stderr[:300]}"
        return output or "Script ran with no output."

    except subprocess.TimeoutExpired:
        log_event("Script execution timed out.")
        return "Script timed out after 30 seconds."

    except Exception as e:
        log_event(f"Script execution error: {str(e)}", level="error")
        return "Script execution failed."

    finally:
        if temp_script_path and os.path.exists(temp_script_path):
            os.remove(temp_script_path)


# -------------------------------------------------
# Safety Filter (Hardened)
# -------------------------------------------------

DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"mkfs",
    r"dd\s+if=",
    r">:",
    r"iptables\s+-F",
    r"chmod\s+777\s+/",
    r"format\s+[Cc]:",
    r"del\s+/[Ss]\s+/[Qq]",
    r"rd\s+/[Ss]\s+/[Qq]",
    r":\(\)\{.*\};:",
    r"base64\s+.*\|.*bash",
]

def is_dangerous(code: str) -> bool:
    """
    Hardened filtering for destructive commands.
    Case-insensitive regex to prevent trivial bypasses.
    """
    normalized = code.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True
    return False
