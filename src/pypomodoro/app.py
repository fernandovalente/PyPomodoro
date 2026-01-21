from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from pypomodoro.core.config import load_config
from pypomodoro.ui.main_window import MainWindow


def _icon_path() -> Path:
    return Path(__file__).resolve().parent.parent / "tomato.ico"


def _debug_log(message: str, data: dict, hypothesis_id: str) -> None:
    payload = {
        "sessionId": "debug-session",
        "runId": "pre-fix",
        "hypothesisId": hypothesis_id,
        "location": "app.py",
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    log_path = Path("/Users/valente/Documents/projects/pomodoro/.cursor/debug.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("", encoding="utf-8") if False else None
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("PyPomodoro")
    icon_path = _icon_path()
    if icon_path.exists():
        icon = QIcon(str(icon_path))
        # #region agent log
        _debug_log(
            "app_icon_load",
            {"path": str(icon_path), "exists": icon_path.exists(), "icon_is_null": icon.isNull()},
            "H1",
        )
        # #endregion
        app.setWindowIcon(icon)
    config = load_config()
    window = MainWindow(config, icon_path if icon_path.exists() else None)
    window.resize(520, 360)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
