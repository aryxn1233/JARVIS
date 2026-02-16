"""
System Monitor Module
Provides real-time CPU, RAM, and Disk monitoring.
"""

import psutil
import threading
import time
from core.logger import log_event
from permission.permission_manager import check_permission
from executor.command_executor import execute_command


# -------------------------------------------------
# Threshold Configuration
# -------------------------------------------------

CPU_THRESHOLD = 85      # percent
RAM_THRESHOLD = 85      # percent
DISK_THRESHOLD = 90     # percent
MONITOR_INTERVAL = 10   # seconds


monitoring_active = False


# -------------------------------------------------
# System Snapshot
# -------------------------------------------------

def get_system_snapshot():
    """
    Returns current system usage metrics.
    """
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }


# -------------------------------------------------
# Proactive Decision Engine
# -------------------------------------------------

def analyze_snapshot(snapshot):
    """
    Analyzes system metrics and suggests actions.
    """

    if snapshot["cpu"] > CPU_THRESHOLD:
        log_event(f"High CPU detected: {snapshot['cpu']}%")
        return {
            "intent": "optimize_cpu",
            "requires_permission": True,
            "execution_type": "direct"
        }

    if snapshot["ram"] > RAM_THRESHOLD:
        log_event(f"High RAM detected: {snapshot['ram']}%")
        return {
            "intent": "optimize_ram",
            "requires_permission": True,
            "execution_type": "direct"
        }

    if snapshot["disk"] > DISK_THRESHOLD:
        log_event(f"High Disk usage detected: {snapshot['disk']}%")
        return {
            "intent": "cleanup_disk",
            "requires_permission": True,
            "execution_type": "direct"
        }

    return None


# -------------------------------------------------
# Optimization Handlers
# -------------------------------------------------

def handle_optimization(intent):
    """
    Basic optimization actions.
    """

    if intent == "optimize_cpu":
        return execute_command({
            "intent": "list_processes",
            "execution_type": "direct"
        })

    elif intent == "optimize_ram":
        return execute_command({
            "intent": "list_processes",
            "execution_type": "direct"
        })

    elif intent == "cleanup_disk":
        return execute_command({
            "intent": "check_disk",
            "execution_type": "direct"
        })

    return "No optimization available."


# -------------------------------------------------
# Monitoring Loop
# -------------------------------------------------

def monitor_loop():
    global monitoring_active
    monitoring_active = True

    log_event("System monitor started.")

    while monitoring_active:
        snapshot = get_system_snapshot()

        action_plan = analyze_snapshot(snapshot)

        if action_plan:
            approved = check_permission(action_plan)

            if approved:
                result = handle_optimization(action_plan["intent"])
                log_event(f"Optimization executed: {result}")
            else:
                log_event("Optimization denied by user.")

        time.sleep(MONITOR_INTERVAL)


# -------------------------------------------------
# Start Monitoring
# -------------------------------------------------

def start_monitoring():
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()


# -------------------------------------------------
# Stop Monitoring
# -------------------------------------------------

def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    log_event("System monitor stopped.")
