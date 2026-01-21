from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict

from platformdirs import user_config_dir


APP_NAME = "PyPomodoro"
APP_AUTHOR = "PyPomodoro"


@dataclass
class AppConfig:
    work_minutes: int = 25
    short_break_minutes: int = 5
    long_break_minutes: int = 20
    language: str = "pt-BR"
    theme: str = "light"
    sound_enabled: bool = True
    sound_file: str = "wood.mp3"
    auto_start_break: bool = True
    auto_start_work: bool = True


def _config_dir() -> Path:
    return Path(user_config_dir(APP_NAME, APP_AUTHOR))


def config_path() -> Path:
    return _config_dir() / "config.json"


def load_config() -> AppConfig:
    path = config_path()
    if not path.exists():
        return AppConfig()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return AppConfig(**_sanitize_config(data))
    except Exception:
        return AppConfig()


def save_config(config: AppConfig) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(asdict(config), indent=2)
    path.write_text(payload, encoding="utf-8")


def _sanitize_config(data: Dict[str, Any]) -> Dict[str, Any]:
    defaults = asdict(AppConfig())
    sanitized: Dict[str, Any] = {}
    for key, default in defaults.items():
        if key not in data:
            sanitized[key] = default
            continue
        value = data[key]
        if isinstance(default, bool):
            sanitized[key] = bool(value)
        elif isinstance(default, int):
            try:
                sanitized[key] = int(value)
            except Exception:
                sanitized[key] = default
        elif isinstance(default, str):
            sanitized[key] = str(value)
        else:
            sanitized[key] = value
    return sanitized
