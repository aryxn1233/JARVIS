from llm.ollama_client import OllamaClient
from config.settings import REASONING_MODEL

ollama = OllamaClient()

def classify_intent(user_input):
    prompt = f"""
You are an AI OS controller.

Return ONLY JSON:
{{
  "intent": "...",
  "requires_permission": true/false,
  "requires_code": true/false
}}

User request: "{user_input}"
"""

    return ollama.generate_json(REASONING_MODEL, prompt)
