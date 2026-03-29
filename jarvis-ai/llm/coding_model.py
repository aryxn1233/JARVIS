"""
LLM Module: Coding Model
Wraps the Ollama client for code generation.
Note: Use core.router.route_command() as the main entry point.
This module is kept for direct/standalone use only.
"""

import sys
from llm.ollama_client import OllamaClient
from config.settings import CODING_MODEL

ollama = OllamaClient()

def generate_code(user_input: str):
    """Generate safe automation code for the current platform."""
    platform = "Windows" if sys.platform == "win32" else "Linux"
    prompt = f"""
Write safe Python automation code for {platform}.
Return ONLY code. No explanations.
Request: "{user_input}"
"""
    return ollama.generate(CODING_MODEL, prompt)
