"""
Speech Input Module
Feature 2 & 4: Voice-first input with support for both:
  - Google Speech Recognition (online, default)
  - OpenAI Whisper (offline, high-quality)

Controlled via config.settings.VOICE_ENGINE
"""

from typing import Optional
from core.logger import log_event


def get_voice_input(timeout: int = 5, engine: str = "google") -> Optional[str]:
    """
    Listens for voice input and returns recognized text.
    Returns None if recognition fails or microphone is unavailable.

    Args:
        timeout: Seconds to wait for speech
        engine: "google" | "whisper"
    """
    if engine == "whisper":
        return _get_voice_whisper()
    else:
        return _get_voice_google(timeout)


# -------------------------------------------------
# Google Speech Recognition (online)
# -------------------------------------------------

def _get_voice_google(timeout: int = 5) -> Optional[str]:
    """Uses Google's free Speech Recognition API. Requires internet."""
    try:
        import speech_recognition as sr
    except ImportError:
        log_event("SpeechRecognition not installed. Run: pip install SpeechRecognition pyaudio", level="warning")
        return None

    try:
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        with sr.Microphone() as source:
            print("\n🎤 Listening... (speak now)")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)

        print("⏳ Recognizing...")
        text = recognizer.recognize_google(audio)
        log_event(f"Google SR recognized: {text}")
        return text.strip()

    except Exception as e:
        name = type(e).__name__
        if "WaitTimeoutError" in name:
            return None  # No speech detected — not an error
        log_event(f"Google SR error: {e}", level="warning")
        return None


# -------------------------------------------------
# Whisper (offline, Feature 4)
# -------------------------------------------------

def _get_voice_whisper() -> Optional[str]:
    """
    Uses OpenAI Whisper for fully offline speech recognition.
    Requires: pip install openai-whisper sounddevice soundfile numpy
    """
    try:
        import whisper
        import sounddevice as sd
        import soundfile as sf
        import numpy as np
        import tempfile
        import os
    except ImportError as e:
        log_event(
            f"Whisper deps missing ({e}). "
            "Run: pip install openai-whisper sounddevice soundfile numpy",
            level="warning"
        )
        return None

    try:
        SAMPLE_RATE = 16000
        DURATION = 6  # seconds to record

        print("\n🎤 Listening (Whisper)... speak for up to 6 seconds")
        audio_data = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32"
        )
        sd.wait()
        print("⏳ Transcribing offline...")

        # Save to temp WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            tmp_path = f.name
        sf.write(tmp_path, audio_data, SAMPLE_RATE)

        model = whisper.load_model("base")
        result = model.transcribe(tmp_path, language="en")
        os.remove(tmp_path)

        text = result.get("text", "").strip()
        if text:
            log_event(f"Whisper recognized: {text}")
            return text

        return None

    except Exception as e:
        log_event(f"Whisper error: {e}", level="error")
        return None
