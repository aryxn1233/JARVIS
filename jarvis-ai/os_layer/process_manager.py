"""
OS Layer: Process Manager
Cross-platform process listing.
"""

import sys
import subprocess


def list_processes():
    """Lists running processes, cross-platform."""
    if sys.platform == "win32":
        result = subprocess.run(["tasklist"], capture_output=True, text=True)
    else:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    return result.stdout
