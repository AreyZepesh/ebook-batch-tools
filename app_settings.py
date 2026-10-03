import sys
import configparser
from pathlib import Path

def make_default_config(_settings: configparser.ConfigParser, ini_path: Path):
    _settings["logging"] = {
        "debug": "False", 
        "encoding": "", 
        ";; encoding default: empty": None, 
        ";; encoding recommendation: utf-8 | utf-8-sig": None, 
        }
    _settings["paths"]= {
        "log_dir": "logs",
        ";; log_dir is subfolder near executable file": None,
          }
    with open(ini_path, "w", encoding="utf-8") as ini_file:
        _settings.write(ini_file)

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

INI_PATH = BASE_DIR / "settings.ini"

_settings = configparser.ConfigParser(allow_no_value=True)
if not INI_PATH.exists():
    make_default_config(_settings, INI_PATH)
    _settings.clear()

try:
    _settings.read(INI_PATH, encoding="utf-8")
except Exception as ex:
    INI_PATH.unlink()
    raise ValueError(
        f"Could not read settings file {INI_PATH}, it will be removed. "
        f"Please restart the app to recreate it with default values.\n"
        f"Не удалось прочитать файл настроек {INI_PATH}, он будет удалён. "
        f"Перезапустите программу, чтобы создать его заново со значениями по умолчанию."
    ) from ex


DEBUG = _settings.getboolean("logging", "debug", fallback=False)
ENCODING = _settings.get("logging", "encoding", fallback="") or None 
LOG_DIR = BASE_DIR / (_settings.get("paths", "log_dir", fallback="") or "logs")