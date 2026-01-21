from __future__ import annotations

import json
import time
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from pypomodoro.core.config import AppConfig
from pypomodoro.core.i18n import get_strings


def _debug_log(message: str, data: dict, hypothesis_id: str) -> None:
    payload = {
        "sessionId": "debug-session",
        "runId": "pre-fix",
        "hypothesisId": hypothesis_id,
        "location": "settings_dialog.py",
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    log_path = Path("/Users/valente/Documents/projects/pomodoro/.cursor/debug.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


class SettingsDialog(QDialog):
    def __init__(self, config: AppConfig, parent=None) -> None:
        super().__init__(parent)
        self.strings = get_strings(config.language)
        self.setWindowTitle(self.strings["settings_title"])
        self.setModal(True)

        self._work_input = QSpinBox()
        self._work_input.setRange(1, 180)
        self._work_input.setValue(config.work_minutes)

        self._short_break_input = QSpinBox()
        self._short_break_input.setRange(1, 60)
        self._short_break_input.setValue(config.short_break_minutes)

        self._long_break_input = QSpinBox()
        self._long_break_input.setRange(1, 120)
        self._long_break_input.setValue(config.long_break_minutes)

        self._theme_select = QComboBox()
        self._theme_select.addItems(["light", "dark"])
        self._theme_select.setCurrentText(config.theme)

        self._language_select = QComboBox()
        self._language_select.addItem(self.strings["language_pt"], "pt-BR")
        self._language_select.addItem(self.strings["language_en"], "en")
        self._language_select.setCurrentIndex(
            0 if config.language == "pt-BR" else 1
        )

        self._sound_enabled = QCheckBox(self.strings["sound_enabled_label"])
        self._sound_enabled.setChecked(config.sound_enabled)

        self._sound_path = QLineEdit()
        self._sound_path.setPlaceholderText(self.strings["sound_placeholder"])
        self._sound_path.setText(config.sound_file)
        self._sound_path.setReadOnly(True)

        self._sound_browse = QPushButton(self.strings["select_sound"])
        self._sound_browse.clicked.connect(self._select_sound)

        self._auto_start_break = QCheckBox(self.strings["auto_start_break"])
        self._auto_start_break.setChecked(config.auto_start_break)

        self._auto_start_work = QCheckBox(self.strings["auto_start_work"])
        self._auto_start_work.setChecked(config.auto_start_work)

        form = QFormLayout()
        form.addRow(self.strings["work_label"], self._work_input)
        form.addRow(self.strings["short_break_label"], self._short_break_input)
        form.addRow(self.strings["long_break_label"], self._long_break_input)
        form.addRow(self.strings["language_label"], self._language_select)
        form.addRow(self.strings["theme_label"], self._theme_select)
        form.addRow("", self._sound_enabled)

        sound_row = QHBoxLayout()
        sound_row.addWidget(self._sound_path, stretch=1)
        sound_row.addWidget(self._sound_browse)
        form.addRow(self.strings["sound_label"], sound_row)
        form.addRow("", self._auto_start_break)
        form.addRow("", self._auto_start_work)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        save_button = QPushButton(self.strings["save"])
        cancel_button = QPushButton(self.strings["cancel"])
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttons)
        self.setLayout(layout)
        self.setFixedWidth(360)

    def get_config(self) -> AppConfig:
        self._work_input.interpretText()
        self._short_break_input.interpretText()
        self._long_break_input.interpretText()
        language = self._language_select.currentData()
        if not language:
            language = "pt-BR" if self._language_select.currentIndex() == 0 else "en"
        # #region agent log
        _debug_log(
            "settings_get_config",
            {
                "work_minutes": self._work_input.value(),
                "short_break_minutes": self._short_break_input.value(),
                "long_break_minutes": self._long_break_input.value(),
                "language": language,
                "theme": self._theme_select.currentText(),
            },
            "H2",
        )
        # #endregion
        return AppConfig(
            work_minutes=self._work_input.value(),
            short_break_minutes=self._short_break_input.value(),
            long_break_minutes=self._long_break_input.value(),
            language=language,
            theme=self._theme_select.currentText(),
            sound_enabled=self._sound_enabled.isChecked(),
            sound_file=self._sound_path.text().strip(),
            auto_start_break=self._auto_start_break.isChecked(),
            auto_start_work=self._auto_start_work.isChecked(),
        )

    def _select_sound(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            self.strings["select_sound"],
            str(Path.home()),
            f'{self.strings["audio_filter"]};;{self.strings["all_files"]}',
        )
        if path:
            self._sound_path.setText(path)
