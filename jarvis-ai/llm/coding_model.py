from llm.ollama_client import OllamaClient
from config.settings import CODING_MODEL

ollama = OllamaClient()

def generate_code(user_input):
    prompt = f"""
Write safe Linux automation code.
Return ONLY code.
Request: "{user_input}"
"""
    return ollama.generate(CODING_MODEL, prompt)
