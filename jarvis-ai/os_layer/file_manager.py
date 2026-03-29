"""
OS Layer: File Manager
Safe file operations.
"""

import os
from core.logger import log_event


def create_file(path: str) -> bool:
    """Creates an empty file at the given path. Returns True on success."""
    try:
        # Ensure parent directory exists
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent)

        with open(path, "w") as f:
            f.write("")

        log_event(f"File created: {path}")
        return True

    except Exception as e:
        log_event(f"File creation error: {e}", level="error")
        return False


def delete_file(path: str) -> bool:
    """Deletes a file at the given path. Returns True on success."""
    try:
        if os.path.exists(path):
            os.remove(path)
            log_event(f"File deleted: {path}")
            return True
        else:
            log_event(f"File not found: {path}", level="warning")
            return False

    except Exception as e:
        log_event(f"File deletion error: {e}", level="error")
        return False


def list_files(directory: str) -> list:
    """Lists files in a directory. Returns list of filenames."""
    try:
        return os.listdir(directory)
    except Exception as e:
        log_event(f"Directory listing error: {e}", level="error")
        return []
