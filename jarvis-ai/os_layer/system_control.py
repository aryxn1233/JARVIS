"""
OS Layer: System Control
Cross-platform shutdown and restart.
"""

import sys
import subprocess


def shutdown():
    """Shuts down the system, cross-platform."""
    if sys.platform == "win32":
        subprocess.run(["shutdown", "/s", "/t", "0"])
    else:
        subprocess.run(["sudo", "shutdown", "now"])


def restart():
    """Restarts the system, cross-platform."""
    if sys.platform == "win32":
        subprocess.run(["shutdown", "/r", "/t", "0"])
    else:
        subprocess.run(["sudo", "reboot"])
