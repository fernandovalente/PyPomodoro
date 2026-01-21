from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from pypomodoro.core.config import load_config
from pypomodoro.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("PyPomodoro")
    config = load_config()
    window = MainWindow(config)
    window.resize(520, 360)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
