"""
Logger Module
Handles system-wide logging.
"""

import logging
import os
from datetime import datetime


LOG_DIR = "logs"
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
