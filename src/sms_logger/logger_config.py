import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(log_path: str | None, console: bool = True) -> logging.Logger:
    logger = logging.getLogger("sms_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    if log_path:
        p = Path(log_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(p, maxBytes=512_000, backupCount=3, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    if console:
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    return logger