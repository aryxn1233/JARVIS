"""
Logger Module
Handles system-wide logging.
"""

import logging
import os
from datetime import datetime

# Use absolute path so logs are always created relative to this file, not CWD
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = "jarvis.log"


def setup_logger():
    """
    Initializes logging system.
    """

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(
        filename=os.path.join(LOG_DIR, LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.info("Logger initialized.")


def log_event(message: str, level: str = "info"):
    """
    Logs an event.
    """

    if level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    else:
        logging.info(message)
