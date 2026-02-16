"""
Jarvis AI - Hybrid OS Shell
Main Entry Point
Author: Aryan Thakur
"""

import sys
import signal
from core.router import route_command
from core.logger import setup_logger, log_event
from core.memory import load_memory, save_memory
from interface.cli_interface import get_user_input
from interface.tts_output import speak
from permission.permission_manager import check_permission
from executor.command_executor import execute_command
from config.settings import SAFE_MODE


# -------------------------------------------------
# Graceful Shutdown Handler
# -------------------------------------------------

def handle_exit(signum=None, frame=None):
    speak("Shutting down Jarvis. Goodbye.")
    log_event("Jarvis stopped.")
    save_memory()
    sys.exit(0)


# -------------------------------------------------
# Initialize System
# -------------------------------------------------

def initialize():
    setup_logger()
    load_memory()
    log_event("Jarvis initialized.")
    speak("Jarvis AI Shell is now online.")


# -------------------------------------------------
# Main Loop
# -------------------------------------------------

def main_loop():
    while True:
        try:
            user_input = get_user_input()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "shutdown jarvis"]:
                handle_exit()

            # Step 1: Route through Reasoning Engine
            action_plan = route_command(user_input)

            if not action_plan:
                speak("I could not understand the request.")
                continue

            log_event(f"Intent detected: {action_plan}")

            # Step 2: Permission Layer
            if SAFE_MODE:
                approved = check_permission(action_plan)
                if not approved:
                    speak("Action cancelled.")
                    log_event("Action denied by user.")
                    continue

            # Step 3: Execute
            result = execute_command(action_plan)

            # Step 4: Response
            if result:
                speak(result)

            log_event(f"Execution result: {result}")

        except Exception as e:
            log_event(f"Error: {str(e)}")
            speak("An internal error occurred.")


# -------------------------------------------------
# Entry Point
# -------------------------------------------------

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    initialize()
    main_loop()
