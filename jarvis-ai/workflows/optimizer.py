"""
Workflows: System Optimizer
Kills high-CPU processes (with user confirmation) and suggests improvements.
"""

import psutil
from core.logger import log_event


def optimize() -> str:
    """
    Identifies top resource-consuming processes and returns a report.
    """
    try:
        processes = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by CPU usage descending
        top_procs = sorted(processes, key=lambda p: p.get("cpu_percent", 0), reverse=True)[:5]

        if not top_procs:
            return "No process data available."

        lines = ["Top 5 resource-consuming processes:"]
        for i, p in enumerate(top_procs, 1):
            lines.append(
                f"  {i}. {p['name']} (PID {p['pid']}) "
                f"| CPU: {p['cpu_percent']:.1f}% | RAM: {p['memory_percent']:.1f}%"
            )

        result = "\n".join(lines)
        log_event("Optimization scan complete.")
        return result

    except Exception as e:
        log_event(f"Optimizer error: {e}", level="error")
        return f"Optimization failed: {e}"
