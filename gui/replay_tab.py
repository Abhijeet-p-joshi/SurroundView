from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
)


class ReplayTab(QWidget):
    """
    Replay tab.

    Responsibilities
    ----------------
    - Display replay controls.
    - Emit Start/Stop replay requests.
    - Display replay status.

    The ReplayController performs all replay logic.
    """

    startReplayRequested = Signal()
    stopReplayRequested = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self._create_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _create_ui(self):

        main_layout = QVBoxLayout(self)

        #
        # Replay Controls
        #

        replay_group = QGroupBox("Replay")

        replay_layout = QVBoxLayout(replay_group)

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Replay")
        self.stop_button = QPushButton("Stop Replay")

        self.stop_button.setEnabled(False)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        replay_layout.addLayout(button_layout)

        #
        # Status
        #

        status_layout = QHBoxLayout()

        status_title = QLabel("Status:")

        self.status_label = QLabel("Stopped")

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        replay_layout.addLayout(status_layout)

        main_layout.addWidget(replay_group)
        main_layout.addStretch()

        #
        # Connections
        #

        self.start_button.clicked.connect(
            self._start_clicked
        )

        self.stop_button.clicked.connect(
            self._stop_clicked
        )

    # ---------------------------------------------------------
    # Button Callbacks
    # ---------------------------------------------------------

    def _start_clicked(self):

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.set_status("Running")

        self.startReplayRequested.emit()

    def _stop_clicked(self):

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        self.set_status("Stopped")

        self.stopReplayRequested.emit()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def set_status(self, text: str):

        self.status_label.setText(text)

    def replay_started(self):

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.set_status("Running")

    def replay_stopped(self):

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        self.set_status("Stopped")