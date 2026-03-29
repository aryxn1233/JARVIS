"""
Workflows: Automation Engine
Runs named workflow modules by name.
"""

import importlib
from core.logger import log_event

AVAILABLE_WORKFLOWS = {
    "cleanup": "workflows.cleanup",
    "optimize": "workflows.optimizer",
}


def run_workflow(name: str) -> str:
    """
    Runs a named workflow by dynamically importing its module.
    Returns the result message.
    """
    module_path = AVAILABLE_WORKFLOWS.get(name.lower())

    if not module_path:
        available = ", ".join(AVAILABLE_WORKFLOWS.keys())
        return f"Workflow '{name}' not found. Available: {available}"

    try:
        module = importlib.import_module(module_path)

        # Each workflow module exposes a main function matching its name
        func_map = {
            "cleanup": "cleanup_temp",
            "optimize": "optimize",
        }
        func_name = func_map.get(name.lower())
        func = getattr(module, func_name)

        log_event(f"Running workflow: {name}")
        return func()

    except Exception as e:
        log_event(f"Workflow error: {e}", level="error")
        return f"Workflow '{name}' failed: {e}"
