from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect


class SoundPlayer:
    def __init__(self) -> None:
        self._effect = QSoundEffect()
        self._enabled = False
        self._sound_file: Optional[Path] = None

    def configure(self, enabled: bool, sound_file: str) -> None:
        self._enabled = enabled
        self._sound_file = Path(sound_file) if sound_file else None
        if self._sound_file and self._sound_file.exists():
            self._effect.setSource(QUrl.fromLocalFile(str(self._sound_file)))
        else:
            self._effect.setSource(QUrl())

    def play(self) -> None:
        if not self._enabled:
            return
        if not self._effect.source().isEmpty():
            self._effect.play()
