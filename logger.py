import logging
from datetime import datetime as dt
from pathlib import Path

DEBUG = True

start_session = dt.now().strftime("%Y%m%d") # %H%M%S

log_dir = Path("./logs/")
if not log_dir.exists():
    log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

cons_handler = logging.StreamHandler()
cons_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
cons_handler.setFormatter(formatter)
logger.addHandler(cons_handler)

file_handler = logging.FileHandler(start_session/f"{start_session}.log", mode="a", encoding="utf-8-sig")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if DEBUG:
    debug_handler = logging.FileHandler(start_session/f"{start_session}.log", mode="a", encoding="utf-8-sig")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] %(message)s"))
    logger.addHandler(debug_handler)


logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')