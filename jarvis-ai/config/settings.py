
OLLAMA_URL = "http://localhost:11434"

REASONING_MODEL = "mistral:7b-instruct-q4_K_M"
CODING_MODEL = "codellama:7b-instruct-q4_K_M"

# Safety & Permissions
SAFE_MODE = True

# Input mode: "text" | "voice" | "hybrid" (voice with text fallback)
INPUT_MODE = "hybrid"

# Voice engine: "google" (needs internet) | "whisper" (offline, needs openai-whisper)
VOICE_ENGINE = "google"

# Number of recent commands to inject into reasoning prompt for context
MEMORY_CONTEXT_SIZE = 5

# GUI mode (True = launch tkinter GUI, False = CLI)
GUI_MODE = True
