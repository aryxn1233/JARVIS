"""
Jarvis AI - Hybrid OS Shell
Main Entry Point
Author: Aryan Thakur
"""

import sys
import signal
from core.router import route_command
from core.logger import setup_logger, log_event
from core.memory import load_memory, save_memory, add_recent_command
from interface.tts_output import speak
from permission.permission_manager import check_permission
from executor.command_executor import execute_command
from config.settings import SAFE_MODE, GUI_MODE
from llm.ollama_client import OllamaClient


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

    # Health-check Ollama before greeting
    ollama = OllamaClient()
    if not ollama.health_check():
        print("⚠️  WARNING: Ollama server is not running at the configured URL.")
        print("   Start Ollama with: ollama serve")
        print("   Jarvis will still launch, but AI commands will fail.\n")
        log_event("Ollama health check failed at startup.", level="warning")
    else:
        log_event("Ollama health check passed.")

    speak("Jarvis AI Shell is now online.")


# -------------------------------------------------
# Main CLI Loop
# -------------------------------------------------

def main_loop():
    from interface.cli_interface import get_user_input
    from os_layer.monitor import start_monitoring, get_pending_alerts

    start_monitoring()

    while True:
        try:
            # Display pending background monitor alerts
            for alert in get_pending_alerts():
                print(f"\n{alert}")

            user_input = get_user_input()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "shutdown jarvis"]:
                handle_exit()

            # Step 1: Route
            action_plan = route_command(user_input)
            if not action_plan:
                speak("I could not understand the request.")
                continue

            log_event(f"Intent detected: {action_plan}")

            # Step 2: Permission
            approved = check_permission(action_plan)
            if not approved:
                speak("Action cancelled.")
                log_event("Action denied by user.")
                continue

            # Step 3: Execute
            result = execute_command(action_plan)

            # Step 4: Store command in memory (Feature 5)
            add_recent_command(user_input)

            # Step 5: Respond
            if result:
                speak(result)

            log_event(f"Execution result: {result}")

        except Exception as e:
            log_event(f"Error: {str(e)}", level="error")
            speak("An internal error occurred.")


# -------------------------------------------------
# Entry Point
# -------------------------------------------------

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    initialize()

    # Feature 6: Launch GUI if --gui flag or GUI_MODE setting
    use_gui = GUI_MODE or "--gui" in sys.argv

    if use_gui:
        from interface.gui import launch_gui
        launch_gui()
    else:
        main_loop()
