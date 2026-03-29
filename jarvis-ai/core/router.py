"""
Router Module
Handles hybrid routing between reasoning and coding models.
Feature 5: Injects last N commands as context into the reasoning prompt.
"""

import sys
from llm.ollama_client import OllamaClient
from config.settings import REASONING_MODEL, CODING_MODEL, MEMORY_CONTEXT_SIZE
from core.logger import log_event

ollama = OllamaClient()


# -------------------------------------------------
# Route Command Entry
# -------------------------------------------------

def route_command(user_input: str):
    """
    Main router entry. Returns structured action plan.
    1. Tries the LLM (Ollama) for full reasoning.
    2. Falls back to keyword matching if LLM is unavailable.
    """
    from core.memory import get_memory

    # Feature 5: Build context from recent commands
    recent = get_memory("recent_commands") or []
    context_commands = recent[-MEMORY_CONTEXT_SIZE:] if recent else []

    reasoning_prompt = build_reasoning_prompt(user_input, context_commands)
    response = ollama.generate_json(REASONING_MODEL, reasoning_prompt)

    if not response:
        log_event("LLM unavailable — using keyword fallback router.")
        response = fallback_route(user_input)
        if not response:
            return None

    requires_code = response.get("requires_code", False)

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
# Keyword Fallback Router (works without Ollama)
# -------------------------------------------------

# Each rule: (list of trigger keywords, intent, requires_permission, param_extractor)
_FALLBACK_RULES = [
    # System info
    (["cpu", "processor"],                        "check_cpu",       False, None),
    (["ram", "memory", "mem"],                    "check_ram",       False, None),
    (["disk", "storage", "drive", "space"],       "check_disk",      False, None),
    (["process", "processes", "running", "tasks"],"list_processes",  False, None),

    # System actions
    (["shutdown", "turn off", "power off"],       "shutdown",        True,  None),
    (["restart", "reboot", "boot"],               "restart",         True,  None),

    # Network
    (["wifi off", "wifi disable", "turn off wifi"],"wifi_off",       True,  None),
    (["wifi on", "wifi enable",  "turn on wifi"],  "wifi_on",        True,  None),

    # Maintenance
    (["clean", "cleanup", "temp", "free space"],  "cleanup_disk",    False, None),
    (["optimiz", "top process", "what's using"],  "optimize_cpu",    False, None),
]

def fallback_route(user_input: str) -> dict:
    """
    Keyword-based intent matcher — no LLM required.
    Handles common commands so JARVIS works even when Ollama is offline.
    """
    text = user_input.lower().strip()

    # ── Open app: "open X" / "launch X" / "start X" ────────────
    for prefix in ("open ", "launch ", "start ", "run "):
        if text.startswith(prefix):
            app_name = text[len(prefix):].strip()
            return {
                "intent": "open_app",
                "requires_permission": False,
                "requires_code": False,
                "description": f"Open {app_name}",
                "execution_type": "direct",
                "parameters": {"app_name": app_name}
            }

    # ── Web search: "search X" / "look up X" / "google X" ──────
    for prefix in ("search ", "look up ", "google ", "find ", "what is ", "who is ", "how to "):
        if text.startswith(prefix):
            query = text[len(prefix):].strip()
            return {
                "intent": "web_search",
                "requires_permission": False,
                "requires_code": False,
                "description": f"Search for {query}",
                "execution_type": "direct",
                "parameters": {"query": query}
            }

    # ── Catch "how much RAM" / "how fast is my CPU" style ───────
    if any(w in text for w in ("how much", "how fast", "check my", "show my", "what's my", "whats my")):
        if any(w in text for w in ("ram", "memory")):
            return _make_plan("check_ram", "Check RAM usage")
        if any(w in text for w in ("cpu", "processor", "speed")):
            return _make_plan("check_cpu", "Check CPU usage")
        if any(w in text for w in ("disk", "storage", "space")):
            return _make_plan("check_disk", "Check disk usage")

    # ── Keyword rules ────────────────────────────────────────────
    for keywords, intent, requires_perm, _ in _FALLBACK_RULES:
        if any(kw in text for kw in keywords):
            return {
                "intent": intent,
                "requires_permission": requires_perm,
                "requires_code": False,
                "description": intent.replace("_", " ").capitalize(),
                "execution_type": "direct",
                "parameters": {}
            }

    log_event(f"Fallback router: no match for '{user_input}'")
    return None


def _make_plan(intent: str, desc: str, requires_perm: bool = False) -> dict:
    return {
        "intent": intent,
        "requires_permission": requires_perm,
        "requires_code": False,
        "description": desc,
        "execution_type": "direct",
        "parameters": {}
    }


# -------------------------------------------------
# Reasoning Prompt Builder (with context)
# -------------------------------------------------

def build_reasoning_prompt(user_input: str, recent_commands: list = None):
    context_block = ""
    if recent_commands:
        history = "\n".join(f"  - {cmd}" for cmd in recent_commands)
        context_block = f"""
Recent command history (use for context):
{history}
"""

    return f"""
You are Jarvis, an AI OS controller running on {'Windows' if sys.platform == 'win32' else 'Linux'}.

Analyze the user request and return ONLY valid JSON.
{context_block}
Available intents:
- shutdown, restart
- list_processes, check_cpu, check_disk, check_ram
- open_app (requires: parameters.app_name)
- web_search (requires: parameters.query)
- wifi_on, wifi_off
- cleanup_disk, optimize_cpu, optimize_ram
- custom (use requires_code: true for custom tasks)

User request: "{user_input}"

Return format:
{{
  "intent": "...",
  "requires_permission": false,
  "requires_code": false,
  "description": "...",
  "parameters": {{}}
}}
"""


# -------------------------------------------------
# Coding Prompt Builder (Cross-Platform)
# -------------------------------------------------

def build_coding_prompt(user_input: str, reasoning_output: dict):
    platform = "Windows" if sys.platform == "win32" else "Linux"
    return f"""
You are a system automation coding assistant running on {platform}.

Write clean, safe Python code based on this request:
"{user_input}"

Rules:
- Use Python for maximum cross-platform compatibility
- Avoid destructive actions unless clearly specified
- Return ONLY executable code
- No explanations, no markdown fences
"""
