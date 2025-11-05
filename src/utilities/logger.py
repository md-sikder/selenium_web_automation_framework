import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# ANSI color codes for console output
COLORS = {
    "RESET": "\033[0m",
    "INFO": "\033[92m",     # Bright Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",    # Red
    "DEBUG": "\033[94m",    # Blue
}


class ColorFormatter(logging.Formatter):
    """Formatter that adds color codes based on log level for console output."""

    def format(self, record):
        level_color = COLORS.get(record.levelname, COLORS["RESET"])
        message = super().format(record)
        return f"{level_color}{message}{COLORS['RESET']}"


def get_logger(name: str = "tests"):
    """Create or retrieve a UTF-8 safe, colorized logger."""
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)

    # Avoid duplicate handlers in interactive sessions
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Ensure UTF-8 output in Windows terminals
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # Log message format
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # File handler (persistent logs)
    file_handler = RotatingFileHandler(
        "logs/test.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(fmt)

    # Console handler (colored)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(ColorFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
