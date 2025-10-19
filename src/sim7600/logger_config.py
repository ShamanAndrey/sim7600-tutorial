"""
Logging configuration for sim7600.
Sets up rotating file handlers and console logging.
"""

from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(logfile: str | None = None, console: bool = True) -> logging.Logger:
    """
    Configure logging with optional file and console outputs.
    
    Args:
        logfile: Path to log file. If None, no file logging.
        console: Whether to log to console.
    
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("sim7600")
    logger.setLevel(logging.INFO)
    logger.handlers = []  # Clear any existing handlers
    
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    
    if logfile:
        log_path = Path(logfile)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(logfile, maxBytes=10 * 1024 * 1024, backupCount=5)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    if console:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    return logger
