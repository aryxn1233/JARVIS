"""
LLM Module: Reasoning Model
Wraps the Ollama client for intent classification.
Note: Use core.router.route_command() as the main entry point.
This module is kept for direct/standalone use only.
"""

from llm.ollama_client import OllamaClient
from config.settings import REASONING_MODEL

ollama = OllamaClient()

def classify_intent(user_input: str):
    """Classify user input into a structured intent dict."""
    prompt = f"""
You are an AI OS controller.

Return ONLY JSON:
{{
  "intent": "...",
  "requires_permission": true,
  "requires_code": false,
  "description": "..."
}}

User request: "{user_input}"
"""
    return ollama.generate_json(REASONING_MODEL, prompt)
