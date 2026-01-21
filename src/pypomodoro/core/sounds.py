from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


def _resource_path(filename: str) -> Path:
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return Path(base_path) / filename
    return Path(__file__).resolve().parents[2] / filename


class SoundPlayer:
    def __init__(self) -> None:
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        self._enabled = False
        self._sound_file: Optional[Path] = None

    def configure(self, enabled: bool, sound_file: str) -> None:
        self._enabled = enabled
        path = Path(sound_file) if sound_file else _resource_path("wood.mp3")
        if not path.is_absolute():
            path = _resource_path(str(path))
        self._sound_file = path if path.exists() else None
        if self._sound_file:
            self._player.setSource(QUrl.fromLocalFile(str(self._sound_file)))
        else:
            self._player.setSource(QUrl())

    def play(self) -> None:
        if not self._enabled:
            return
        if not self._player.source().isEmpty():
            self._player.stop()
            self._player.play()
