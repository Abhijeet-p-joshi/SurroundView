from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QSplitter
)
from visualization.surround_view_widget import SurroundViewWidget
from gui.control_panel import ControlPanel
from controllers import SurroundViewController
from replay import ReplayController


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SurroundView")
        self.resize(1400, 900)
        self._create_menu()
        self._create_ui()
        self._create_toolbar()

    def _create_ui(self):

        splitter = QSplitter(Qt.Horizontal)

        right_panel = self._create_visualization_panel()
        self.controller = SurroundViewController(
            self.surround_view
        )

        self.replay_controller = ReplayController()
        self.replay_controller.batch_updated.connect(
            self.surround_view.update_objects
        )
        self.replay_controller.status_changed.connect(
            self.statusBar().showMessage
        )

        self.surround_view.objectMoved.connect(
            self.controller.object_dragged
        )

        left_panel = self._create_control_panel()

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        splitter.setSizes([300, 1100])

        self.setCentralWidget(splitter)

        self.statusBar().showMessage("Ready")

    def _create_control_panel(self):

        self.control_panel = ControlPanel()

        self.control_panel.apply_clicked.connect(
            self.controller.update_objects
        )

        return self.control_panel

    def _create_visualization_panel(self):

        panel = QFrame()
        panel.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(panel)

        self.surround_view = SurroundViewWidget()

        layout.addWidget(self.surround_view)

        return panel

    def _create_menu(self):

        file_menu = self.menuBar().addMenu("File")

        view_menu = self.menuBar().addMenu("View")

        tools_menu = self.menuBar().addMenu("Tools")

        help_menu = self.menuBar().addMenu("Help")

    def _create_toolbar(self):

        toolbar = self.addToolBar("Main Toolbar")

        start_action = QAction("Start Replay", self)
        stop_action = QAction("Stop Replay", self)

        start_action.triggered.connect(
            self.replay_controller.start
        )

        stop_action.triggered.connect(
            self.replay_controller.stop
        )

        toolbar.addAction(start_action)
        toolbar.addAction(stop_action)