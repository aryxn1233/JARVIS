"""
Ollama Client Module
Handles communication with local Ollama server.
"""

import requests
import json
from config.settings import OLLAMA_URL
from core.logger import log_event


class OllamaClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or OLLAMA_URL
        self.generate_endpoint = f"{self.base_url}/api/generate"

    # -------------------------------------------------
    # Core Model Call
    # -------------------------------------------------

    def generate(self, model: str, prompt: str, temperature: float = 0.2):
        """
        Sends prompt to Ollama model and returns response text.
        """

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        try:
            response = requests.post(self.generate_endpoint, json=payload, timeout=120)

            if response.status_code != 200:
                log_event(f"Ollama error: {response.status_code} - {response.text}")
                return None

            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            log_event(f"Ollama connection error: {str(e)}")
            return None

    # -------------------------------------------------
    # JSON-Safe Generation
    # -------------------------------------------------

    def generate_json(self, model: str, prompt: str):
        """
        Forces model to return JSON and safely parses it.
        """

        response_text = self.generate(model, prompt)

        if not response_text:
            return None

        try:
            # Clean markdown formatting if model adds it
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)

        except json.JSONDecodeError:
            log_event("Invalid JSON returned from model.")
            log_event(f"Raw Output: {response_text}")
            return None

    # -------------------------------------------------
    # Health Check
    # -------------------------------------------------

    def health_check(self):
        """
        Checks if Ollama server is running.
        """
        try:
            response = requests.get(self.base_url)
            return response.status_code == 200
        except Exception:
            return False
