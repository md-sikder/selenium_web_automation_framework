import logging, os
from logging.handlers import RotatingFileHandler

def get_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("tests")
    if logger.handlers: return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh = RotatingFileHandler("logs/test.log", maxBytes=5_000_000, backupCount=3)
    fh.setFormatter(fmt); ch = logging.StreamHandler(); ch.setFormatter(fmt)
    logger.addHandler(fh); logger.addHandler(ch)
    return logger
