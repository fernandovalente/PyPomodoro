from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pypomodoro.core.config import AppConfig, save_config
from pypomodoro.core.notifications import send_notification
from pypomodoro.core.sounds import SoundPlayer
from pypomodoro.core.timer_engine import SessionState, TimerEngine, TimerEvent
from pypomodoro.ui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self.setWindowTitle("PyPomodoro")

        self.config = config
        self.engine = TimerEngine(
            work_minutes=config.work_minutes,
            short_break_minutes=config.short_break_minutes,
            long_break_minutes=config.long_break_minutes,
            auto_start_break=config.auto_start_break,
            auto_start_work=config.auto_start_work,
            on_transition=self._on_transition,
        )
        self.sound_player = SoundPlayer()
        self.sound_player.configure(config.sound_enabled, config.sound_file)

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)
        self._timer.start()

        self._build_ui()
        self._apply_theme(self.config.theme)
        self._update_display()

    def _build_ui(self) -> None:
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(24, 24, 24, 24)

        self.state_label = QLabel("Foco")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_label.setFont(QFont("Arial", 18, QFont.Bold))

        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 56, QFont.Bold))

        self.cycle_label = QLabel("Ciclos completos: 0")
        self.cycle_label.setAlignment(Qt.AlignCenter)

        buttons_row = QHBoxLayout()
        self.start_pause_button = QPushButton("Iniciar")
        self.reset_button = QPushButton("Resetar")
        self.skip_button = QPushButton("Pular pausa")
        self.settings_button = QPushButton("Configuracoes")

        self.start_pause_button.clicked.connect(self._toggle_start_pause)
        self.reset_button.clicked.connect(self._reset_timer)
        self.skip_button.clicked.connect(self._skip_break)
        self.settings_button.clicked.connect(self._open_settings)

        buttons_row.addWidget(self.start_pause_button)
        buttons_row.addWidget(self.reset_button)
        buttons_row.addWidget(self.skip_button)
        buttons_row.addWidget(self.settings_button)

        layout.addWidget(self.state_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.cycle_label)
        layout.addLayout(buttons_row)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def _on_tick(self) -> None:
        event = self.engine.tick()
        if event:
            self._handle_event(event)
        self._update_display()

    def _toggle_start_pause(self) -> None:
        if self.engine.is_running:
            self.engine.pause()
        else:
            self.engine.start()
        self._update_display()

    def _reset_timer(self) -> None:
        self.engine.reset()
        self._update_display()

    def _skip_break(self) -> None:
        event = self.engine.skip_break()
        if event:
            self._handle_event(event)
        self._update_display()

    def _open_settings(self) -> None:
        dialog = SettingsDialog(self.config, self)
        if dialog.exec() != dialog.Accepted:
            return
        self.config = dialog.get_config()
        save_config(self.config)
        self.engine.update_settings(
            work_minutes=self.config.work_minutes,
            short_break_minutes=self.config.short_break_minutes,
            long_break_minutes=self.config.long_break_minutes,
            auto_start_break=self.config.auto_start_break,
            auto_start_work=self.config.auto_start_work,
        )
        self.sound_player.configure(self.config.sound_enabled, self.config.sound_file)
        self._apply_theme(self.config.theme)
        self._update_display()

    def _handle_event(self, event: TimerEvent) -> None:
        self._update_display()
        message = self._transition_message(event)
        send_notification("PyPomodoro", message)
        self.sound_player.play()

    def _transition_message(self, event: TimerEvent) -> str:
        if event.to_state == SessionState.WORK:
            return "Pausa finalizada. Hora de focar."
        if event.to_state == SessionState.SHORT_BREAK:
            return "Ciclo completo. Pausa curta."
        if event.to_state == SessionState.LONG_BREAK:
            return "Ciclo completo. Pausa longa."
        return "Transicao de ciclo."

    def _on_transition(self, event: TimerEvent) -> None:
        self._handle_event(event)

    def _update_display(self) -> None:
        self.state_label.setText(self._state_label_text())
        self.timer_label.setText(self._format_time(self.engine.remaining_seconds))
        self.cycle_label.setText(f"Ciclos completos: {self.engine.cycle_count}")
        self.start_pause_button.setText("Pausar" if self.engine.is_running else "Iniciar")
        self.skip_button.setEnabled(
            self.engine.state in (SessionState.SHORT_BREAK, SessionState.LONG_BREAK)
        )

    def _state_label_text(self) -> str:
        if self.engine.state == SessionState.WORK:
            return "Foco"
        if self.engine.state == SessionState.SHORT_BREAK:
            return "Pausa curta"
        return "Pausa longa"

    @staticmethod
    def _format_time(total_seconds: int) -> str:
        minutes = max(0, total_seconds) // 60
        seconds = max(0, total_seconds) % 60
        return f"{minutes:02d}:{seconds:02d}"

    def _apply_theme(self, theme: str) -> None:
        if theme == "dark":
            self.setStyleSheet(
                """
                QWidget {
                    background-color: #1f1f1f;
                    color: #f2f2f2;
                }
                QPushButton {
                    background-color: #2d2d2d;
                    border: 1px solid #3a3a3a;
                    padding: 8px 12px;
                    border-radius: 6px;
                }
                QPushButton:disabled {
                    background-color: #242424;
                    color: #7a7a7a;
                }
                """
            )
        else:
            self.setStyleSheet(
                """
                QWidget {
                    background-color: #f6f6f6;
                    color: #1b1b1b;
                }
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    padding: 8px 12px;
                    border-radius: 6px;
                }
                QPushButton:disabled {
                    background-color: #ededed;
                    color: #9a9a9a;
                }
                """
            )
