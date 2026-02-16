"""
Permission Prompt Interface
Handles user confirmation for critical actions.
"""

from interface.tts_output import speak


def ask_permission(intent: str) -> bool:
    """
    Prompts user for approval.
    """

    speak(f"This action requires approval: {intent}. Do you approve? (yes/no)")

    try:
        response = input("Approve action? (yes/no): ").strip().lower()

        if response in ["yes", "y"]:
            return True
        else:
            return False

    except Exception:
        return False
