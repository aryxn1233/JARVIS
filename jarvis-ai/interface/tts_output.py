"""
Text-to-Speech Output Layer
Provides voice response capability.
"""

import pyttsx3
from core.logger import log_event

# Initialize engine once
engine = pyttsx3.init()

# Optional tuning
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text: str):
    """
    Speaks text aloud and logs it.
    """

    if not text:
        return

    try:
        print(f"Jarvis: {text}")  # CLI fallback display

        engine.say(text)
        engine.runAndWait()

        log_event(f"TTS Output: {text}")

    except Exception as e:
        log_event(f"TTS error: {str(e)}")
        print(text)
