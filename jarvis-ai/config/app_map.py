"""
App Map — Feature 1: Open Apps by Name
Maps friendly app names to their Windows/Linux executables.
"""

APP_MAP = {
    # Browsers
    "chrome":       {"win": "chrome.exe",              "linux": "google-chrome"},
    "firefox":      {"win": "firefox.exe",             "linux": "firefox"},
    "edge":         {"win": "msedge.exe",              "linux": "microsoft-edge"},
    "brave":        {"win": "brave.exe",               "linux": "brave-browser"},

    # Editors / IDEs
    "vscode":       {"win": "code",                    "linux": "code"},
    "code":         {"win": "code",                    "linux": "code"},
    "notepad":      {"win": "notepad.exe",             "linux": "gedit"},
    "notepad++":    {"win": "notepad++.exe",           "linux": "notepadqq"},
    "pycharm":      {"win": "pycharm64.exe",           "linux": "pycharm"},

    # Terminal
    "terminal":     {"win": "wt.exe",                  "linux": "gnome-terminal"},
    "cmd":          {"win": "cmd.exe",                 "linux": "bash"},
    "powershell":   {"win": "powershell.exe",          "linux": "bash"},

    # Media
    "vlc":          {"win": "vlc.exe",                 "linux": "vlc"},
    "spotify":      {"win": "Spotify.exe",             "linux": "spotify"},

    # Productivity
    "word":         {"win": "WINWORD.EXE",             "linux": "libreoffice --writer"},
    "excel":        {"win": "EXCEL.EXE",               "linux": "libreoffice --calc"},
    "outlook":      {"win": "OUTLOOK.EXE",             "linux": "thunderbird"},
    "teams":        {"win": "Teams.exe",               "linux": "teams"},
    "discord":      {"win": "Discord.exe",             "linux": "discord"},
    "slack":        {"win": "slack.exe",               "linux": "slack"},
    "zoom":         {"win": "Zoom.exe",                "linux": "zoom"},

    # System
    "calculator":   {"win": "calc.exe",                "linux": "gnome-calculator"},
    "taskmanager":  {"win": "taskmgr.exe",             "linux": "gnome-system-monitor"},
    "explorer":     {"win": "explorer.exe",            "linux": "nautilus"},
    "paint":        {"win": "mspaint.exe",             "linux": "kolourpaint"},
    "settings":     {"win": "ms-settings:",            "linux": "gnome-control-center"},
    "control panel":{"win": "control.exe",             "linux": "gnome-control-center"},
    "snipping tool":{"win": "SnippingTool.exe",        "linux": "gnome-screenshot"},
}
