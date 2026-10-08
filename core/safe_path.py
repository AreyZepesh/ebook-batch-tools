from pathlib import Path
import os, re, sys

from core.logger import setup_logging, q
logger = setup_logging()

_BAD_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_RESERVED = {"CON", "PRN", "AUX", "NUL",
             *(f"COM{i}" for i in range(1, 10)),
             *(f"LPT{i}" for i in range(1, 10))}

def safe_name(filename: str, max_bytes: int = 255) -> str:
    stem, ext = os.path.splitext(filename)
    stem = _BAD_CHARS.sub("_", stem).rstrip(" .")
    if ext:
        ext = _BAD_CHARS.sub("", ext).rstrip(" .")
        if not ext:
            ext = "._"

    if stem.split(".")[0].rstrip(" ").upper() in _RESERVED:
        stem = "_" + stem

    if sys.platform != "win32":
        limit = max_bytes - len(ext.encode("utf-8"))
        stem = stem.encode("utf-8")[:limit].decode("utf-8", errors="ignore")
    filename = stem + ext
    return filename.rstrip(" .") or "_"


def get_safe_path(path: str | Path) -> Path:
    """Очищает ту часть пути, которой ещё нет на диске."""
    if isinstance(path, str) and sys.platform == "win32":
        if len(path) == 2 and path[-1] == ":":
            path += "/"
        if len(path) == 1 and re.fullmatch(r"[A-Za-z]", path):
            path += ":/"
            
    path = Path(os.path.abspath(path))

    if path.exists():
        return path

    logger.debug("Принят путь: %s", q(path))

    base = path
    for base in path.parents:
        if base.exists():
             break
    else:
        raise FileNotFoundError(f"Корень пути не существует: {base}")

    logger.debug("Базовый путь, уже существует на диске: %s", q(base))
    rel = path.relative_to(base)
    logger.debug("Относительный путь, еще не существубщий на диске: %s", q(rel))
    safe_parts = [base]
    for part in rel.parts:
        safe_parts.append(safe_name(part))
    safe_path = Path(*safe_parts)
    logger.debug("Преобразованный, безопасный путь: %s", q(safe_path) )
    return safe_path
