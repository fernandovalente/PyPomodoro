from __future__ import annotations

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


class SettingsDialog(QDialog):
    def __init__(self, config: AppConfig, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Configuracoes")
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

        self._sound_enabled = QCheckBox("Som ativado")
        self._sound_enabled.setChecked(config.sound_enabled)

        self._sound_path = QLineEdit()
        self._sound_path.setPlaceholderText("Arquivo de som")
        self._sound_path.setText(config.sound_file)
        self._sound_path.setReadOnly(True)

        self._sound_browse = QPushButton("Selecionar")
        self._sound_browse.clicked.connect(self._select_sound)

        self._auto_start_break = QCheckBox("Auto iniciar pausas")
        self._auto_start_break.setChecked(config.auto_start_break)

        self._auto_start_work = QCheckBox("Auto iniciar trabalho")
        self._auto_start_work.setChecked(config.auto_start_work)

        form = QFormLayout()
        form.addRow("Trabalho (min)", self._work_input)
        form.addRow("Pausa curta (min)", self._short_break_input)
        form.addRow("Pausa longa (min)", self._long_break_input)
        form.addRow("Tema", self._theme_select)
        form.addRow("", self._sound_enabled)

        sound_row = QHBoxLayout()
        sound_row.addWidget(self._sound_path, stretch=1)
        sound_row.addWidget(self._sound_browse)
        form.addRow("Som", sound_row)
        form.addRow("", self._auto_start_break)
        form.addRow("", self._auto_start_work)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        save_button = QPushButton("Salvar")
        cancel_button = QPushButton("Cancelar")
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
        return AppConfig(
            work_minutes=self._work_input.value(),
            short_break_minutes=self._short_break_input.value(),
            long_break_minutes=self._long_break_input.value(),
            theme=self._theme_select.currentText(),
            sound_enabled=self._sound_enabled.isChecked(),
            sound_file=self._sound_path.text().strip(),
            auto_start_break=self._auto_start_break.isChecked(),
            auto_start_work=self._auto_start_work.isChecked(),
        )

    def _select_sound(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar som",
            str(Path.home()),
            "Audio Files (*.wav);;Todos os arquivos (*)",
        )
        if path:
            self._sound_path.setText(path)
