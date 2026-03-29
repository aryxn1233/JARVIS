"""
CLI Interface
Feature 2: Voice-first hybrid input mode.
Supports three modes via config.settings.INPUT_MODE:
  - "text"   : keyboard only
  - "voice"  : microphone only (falls back to text on failure)
  - "hybrid" : tries voice first, falls back to text if silent
"""

from config.settings import INPUT_MODE, VOICE_ENGINE


def get_user_input() -> str:
    """
    Gets user input via configured mode.
    Returns stripped string, or empty string if nothing received.
    """
    mode = INPUT_MODE.lower()

    if mode == "text":
        return _get_text_input()

    elif mode == "voice":
        result = _get_voice()
        if result:
            print(f"You (voice): {result}")
            return result
        # Hard voice mode: if nothing heard, still prompt text as emergency
        print("(No voice detected — type your command:)")
        return _get_text_input()

    else:  # "hybrid" — default
        result = _get_voice()
        if result:
            print(f"You (voice): {result}")
            return result
        # Seamlessly fall back to text prompt
        return _get_text_input()


def _get_text_input() -> str:
    """Standard keyboard input."""
    try:
        return input("You: ").strip()
    except KeyboardInterrupt:
        return "exit"
    except EOFError:
        return "exit"


def _get_voice() -> str:
    """Attempts voice input using the configured engine."""
    try:
        from interface.speech_input import get_voice_input
        return get_voice_input(timeout=4, engine=VOICE_ENGINE)
    except Exception:
        return None
