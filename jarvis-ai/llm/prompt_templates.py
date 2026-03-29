"""
LLM Module: Prompt Templates
Centralized prompt template builders.
The main prompt builders live in core/router.py.
These helpers are for standalone or testing use.
"""

import sys


def build_reasoning_prompt(text: str) -> str:
    """Build a structured reasoning prompt for the given user input."""
    return f"""
You are an AI OS controller.

Analyze and classify the user request. Return ONLY valid JSON:
{{
  "intent": "...",
  "requires_permission": true,
  "requires_code": false,
  "description": "..."
}}

User request: "{text}"
"""


def build_coding_prompt(text: str) -> str:
    """Build a code generation prompt for the given user input."""
    platform = "Windows" if sys.platform == "win32" else "Linux"
    return f"""
Write safe Python automation code for {platform}.
Return ONLY code. No markdown, no explanations.
Request: "{text}"
"""
