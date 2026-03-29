"""
OS Layer: Network Control
Cross-platform WiFi control.
"""

import sys
import subprocess


def wifi_off():
    """Disables WiFi, cross-platform."""
    if sys.platform == "win32":
        subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "disabled"])
    else:
        subprocess.run(["nmcli", "radio", "wifi", "off"])


def wifi_on():
    """Enables WiFi, cross-platform."""
    if sys.platform == "win32":
        subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"])
    else:
        subprocess.run(["nmcli", "radio", "wifi", "on"])
