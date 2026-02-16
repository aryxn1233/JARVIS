"""
Router Module
Handles hybrid routing between reasoning and coding models.
"""

from llm.ollama_client import OllamaClient
from config.settings import REASONING_MODEL, CODING_MODEL
from core.logger import log_event

ollama = OllamaClient()


# -------------------------------------------------
# Route Command Entry
# -------------------------------------------------

def route_command(user_input: str):
    """
    Main router entry.
    Returns structured action plan.
    """

    reasoning_prompt = build_reasoning_prompt(user_input)

    response = ollama.generate_json(REASONING_MODEL, reasoning_prompt)

    if not response:
        log_event("Reasoning model failed to return valid JSON.")
        return None

    intent = response.get("intent")
    requires_code = response.get("requires_code", False)

    # If code generation required → call coding model
    if requires_code:
        code_prompt = build_coding_prompt(user_input, response)
        generated_code = ollama.generate(CODING_MODEL, code_prompt)

        response["generated_code"] = generated_code
        response["execution_type"] = "script"

    else:
        response["execution_type"] = "direct"

    log_event(f"Router decision: {response}")

    return response


# -------------------------------------------------
# Reasoning Prompt Builder
# -------------------------------------------------

def build_reasoning_prompt(user_input: str):
    return f"""
You are an AI OS controller.

Analyze the user request and return ONLY valid JSON.

Possible fields:
- intent: string
- requires_permission: true/false
- requires_code: true/false
- description: short explanation

User request: "{user_input}"

Return format:
{{
  "intent": "...",
  "requires_permission": true/false,
  "requires_code": true/false,
  "description": "..."
}}
"""


# -------------------------------------------------
# Coding Prompt Builder
# -------------------------------------------------

def build_coding_prompt(user_input: str, reasoning_output: dict):
    return f"""
You are a Linux automation coding assistant.

Write clean, safe code based on this request:
"{user_input}"

Rules:
- Use Bash or Python where appropriate
- Avoid destructive actions unless clearly specified
- Return ONLY executable code
- No explanations
"""
