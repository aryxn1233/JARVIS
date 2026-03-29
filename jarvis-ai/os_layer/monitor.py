"""
System Monitor Module
Provides real-time CPU, RAM, and Disk monitoring.
Cross-platform; does NOT prompt user for input from background thread.
"""

import sys
import psutil
import threading
import time
from core.logger import log_event


# -------------------------------------------------
# Threshold Configuration
# -------------------------------------------------

CPU_THRESHOLD = 85      # percent
RAM_THRESHOLD = 85      # percent
DISK_THRESHOLD = 90     # percent
MONITOR_INTERVAL = 10   # seconds


monitoring_active = False

# Shared queue for monitor alerts (avoids stdin conflict with main loop)
_alerts = []
_alerts_lock = threading.Lock()


def _get_disk_path():
    """Returns the correct root disk path for the current OS."""
    return "C:\\" if sys.platform == "win32" else "/"


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
        "disk": psutil.disk_usage(_get_disk_path()).percent
    }


# -------------------------------------------------
# Proactive Decision Engine
# -------------------------------------------------

def analyze_snapshot(snapshot):
    """
    Analyzes system metrics and flags alerts.
    """

    if snapshot["cpu"] > CPU_THRESHOLD:
        log_event(f"High CPU detected: {snapshot['cpu']}%", level="warning")
        return {
            "intent": "optimize_cpu",
            "requires_permission": True,
            "execution_type": "direct",
            "alert_message": f"⚠️  High CPU usage detected: {snapshot['cpu']}%. Type 'check cpu' to investigate."
        }

    if snapshot["ram"] > RAM_THRESHOLD:
        log_event(f"High RAM detected: {snapshot['ram']}%", level="warning")
        return {
            "intent": "optimize_ram",
            "requires_permission": True,
            "execution_type": "direct",
            "alert_message": f"⚠️  High RAM usage detected: {snapshot['ram']}%. Type 'list processes' to investigate."
        }

    if snapshot["disk"] > DISK_THRESHOLD:
        log_event(f"High Disk usage detected: {snapshot['disk']}%", level="warning")
        return {
            "intent": "cleanup_disk",
            "requires_permission": True,
            "execution_type": "direct",
            "alert_message": f"⚠️  High disk usage detected: {snapshot['disk']}%. Type 'check disk' to investigate."
        }

    return None


# -------------------------------------------------
# Get Pending Alerts (called from main loop)
# -------------------------------------------------

def get_pending_alerts():
    """
    Returns and clears pending monitor alerts.
    Called from the main loop — safe, no stdin conflict.
    """
    with _alerts_lock:
        pending = list(_alerts)
        _alerts.clear()
    return pending


# -------------------------------------------------
# Monitoring Loop
# -------------------------------------------------

def monitor_loop():
    global monitoring_active
    monitoring_active = True

    log_event("System monitor started.")

    while monitoring_active:
        try:
            snapshot = get_system_snapshot()
            action_plan = analyze_snapshot(snapshot)

            if action_plan:
                alert_msg = action_plan.get("alert_message", "")
                if alert_msg:
                    with _alerts_lock:
                        _alerts.append(alert_msg)

        except Exception as e:
            log_event(f"Monitor loop error: {str(e)}", level="error")

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
