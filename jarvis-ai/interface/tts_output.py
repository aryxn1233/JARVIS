"""
Text-to-Speech Output Layer
Provides voice response capability with lazy initialization.
"""

from core.logger import log_event

# Engine is lazily initialized to avoid crash-at-import if no TTS driver exists
_engine = None


def _get_engine():
    """
    Returns the TTS engine, initializing it on first use.
    """
    global _engine
    if _engine is None:
        import pyttsx3
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 170)
        _engine.setProperty("volume", 1.0)
    return _engine


def speak(text: str):
    """
    Speaks text aloud and logs it.
    Falls back to print-only if TTS is unavailable.
    """

    if not text:
        return

    print(f"Jarvis: {text}")  # Always show in CLI

    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
        log_event(f"TTS Output: {text}")

    except Exception as e:
        log_event(f"TTS error: {str(e)}", level="warning")
        # Print fallback already happened above
