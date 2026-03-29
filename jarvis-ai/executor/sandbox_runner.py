"""
Sandbox Runner
Validates AI-generated code before execution.
Relies on the safety filter in command_executor.is_dangerous().
"""

from executor.command_executor import is_dangerous


def sandbox_execute(code: str):
    """
    Validates code safety before returning it for execution.
    Returns the code if safe, or None if blocked.
    """
    if not code or not code.strip():
        return None

    if is_dangerous(code):
        return None

    return code
