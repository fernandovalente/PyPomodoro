from __future__ import annotations

import platform
import subprocess
from typing import Optional

from plyer import notification


def send_notification(title: str, message: str) -> None:
    try:
        notification.notify(title=title, message=message, app_name="PyPomodoro")
    except Exception:
        _fallback_notification(title, message)


def _fallback_notification(title: str, message: str) -> None:
    if platform.system().lower() == "darwin":
        _macos_notification(title, message)


def _macos_notification(title: str, message: str) -> None:
    script = f'display notification "{_escape(message)}" with title "{_escape(title)}"'
    try:
        subprocess.run(["osascript", "-e", script], check=False)
    except Exception:
        return


def _escape(value: Optional[str]) -> str:
    return (value or "").replace('"', '\\"')
