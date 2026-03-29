"""
Workflows: Disk Cleanup
Removes temporary files to free disk space — cross-platform.
"""

import sys
import os
import tempfile
import shutil
from core.logger import log_event


def cleanup_temp() -> str:
    """
    Cleans up temporary files on the system.
    Returns a status message.
    """
    freed = 0

    try:
        temp_dir = tempfile.gettempdir()
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            try:
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    os.remove(item_path)
                    freed += size
                elif os.path.isdir(item_path):
                    size = sum(
                        os.path.getsize(os.path.join(dp, f))
                        for dp, _, fns in os.walk(item_path)
                        for f in fns
                    )
                    shutil.rmtree(item_path, ignore_errors=True)
                    freed += size
            except Exception:
                pass  # Skip locked or protected files

        freed_mb = freed / (1024 * 1024)
        msg = f"Cleanup complete. Freed approximately {freed_mb:.1f} MB from temp directory."
        log_event(msg)
        return msg

    except Exception as e:
        log_event(f"Cleanup error: {e}", level="error")
        return f"Cleanup failed: {e}"
