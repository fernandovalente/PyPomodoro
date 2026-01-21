from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from pypomodoro.core.config import load_config
from pypomodoro.ui.main_window import MainWindow


def _icon_path() -> Path:
    return Path(__file__).resolve().parent.parent / "tomato.png"


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("PyPomodoro")
    icon_path = _icon_path()
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    config = load_config()
    window = MainWindow(config, icon_path if icon_path.exists() else None)
    window.resize(520, 360)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
