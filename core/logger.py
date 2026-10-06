import logging
from logging.handlers import TimedRotatingFileHandler
from core.app_settings import LOG_DIR, DEBUG, ENCODING

def setup_logging(name_log: str = "book_utils") -> logging.Logger:
    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name_log)
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    base_fmt = "[%(asctime)s] [%(levelname)s] %(message)s"

    cons_formatter = logging.Formatter(base_fmt, datefmt="%H:%M:%S")
    cons_handler = logging.StreamHandler()
    cons_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    cons_handler.setFormatter(cons_formatter)
    logger.addHandler(cons_handler)

    file_formatter = logging.Formatter(base_fmt)
    file_handler = TimedRotatingFileHandler(LOG_DIR/f"{name_log}.log", when="h", encoding=ENCODING, backupCount=24)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if DEBUG:
        debug_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] %(message)s")
        debug_handler = logging.FileHandler(LOG_DIR/f"{name_log}_debug.log", mode="a", encoding=ENCODING)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(debug_formatter)
        logger.addHandler(debug_handler)

    return logger

def q(value) -> str:
    """Оборачивает значение в кавычки для читаемости в логах."""
    return f"'{value}'"