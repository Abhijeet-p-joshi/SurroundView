from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QTabWidget,
    QFrame,
)

from gui.replay_tab import ReplayTab
from gui.inject_tab import InjectTab

from visualization.surround_view_widget import SurroundViewWidget

from controllers.visualization_controller import VisualizationController
from controllers.replay_controller import ReplayController
from controllers.injection_controller import InjectionController


class MainWindow(QMainWindow):
    """
    Main application window.

    Layout

        +-----------------------------------------+
        | Replay | Inject                         |
        +-----------------------------------------+
        |                                         |
        |   Current Tab                           |
        |                                         |
        +-----------------------------------------+
        |                                         |
        |    Surround View Visualization          |
        |                                         |
        +-----------------------------------------+
    """

    def __init__(self, preview_mode=False):

        super().__init__()

        self.preview_mode = preview_mode

        self.setWindowTitle("SurroundView")

        self.resize(1500, 900)

        self._create_ui()

        self._create_controllers()

        if not self.preview_mode:
            self._connect_signals()
            self.statusBar().showMessage("Ready")
        else:
            self.statusBar().showMessage("Preview Mode")

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _create_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        #
        # Splitter
        #

        splitter = QSplitter(Qt.Vertical)

        #
        # Tabs
        #

        self.tabs = QTabWidget()

        self.replay_tab = ReplayTab()

        self.inject_tab = InjectTab()

        self.tabs.addTab(
            self.replay_tab,
            "Replay",
        )

        self.tabs.addTab(
            self.inject_tab,
            "Inject",
        )

        splitter.addWidget(self.tabs)

        #
        # Visualization
        #

        visualization_frame = QFrame()

        visualization_layout = QVBoxLayout(
            visualization_frame
        )

        self.surround_view = SurroundViewWidget()

        visualization_layout.addWidget(
            self.surround_view
        )

        splitter.addWidget(
            visualization_frame
        )

        splitter.setSizes(
            [
                450,
                550,
            ]
        )

        layout.addWidget(
            splitter
        )

    # ---------------------------------------------------------
    # Controllers
    # ---------------------------------------------------------

    def _create_controllers(self):

        self.visualization_controller = VisualizationController(
            self.surround_view
        )

        if self.preview_mode:
            return

        self.replay_controller = ReplayController(
            self.visualization_controller
        )

        self.injection_controller = InjectionController(
            self.visualization_controller
        )

    # ---------------------------------------------------------
    # Signal Connections
    # ---------------------------------------------------------

    def _connect_signals(self):

        # Replay
        self.replay_tab.startReplayRequested.connect(
            self.start_replay
        )

        self.replay_tab.stopReplayRequested.connect(
            self.replay_controller.stop
        )

        self.replay_controller.replay_started.connect(
            self.replay_tab.replay_started
        )

        self.replay_controller.replay_stopped.connect(
            self.replay_tab.replay_stopped
        )

        self.replay_controller.status_changed.connect(
            self.statusBar().showMessage
        )

        # Apply Scenario
        self.inject_tab.scenarioApplied.connect(
            self.injection_controller.apply_scenario
        )

        # Toggle Injection
        self.inject_tab.startInjectionRequested.connect(
            self.start_injection
        )

        self.inject_tab.stopInjectionRequested.connect(
            self.injection_controller.stop
        )

        # Update GUI
        self.injection_controller.injection_started.connect(
            self.inject_tab.injection_started
        )

        self.injection_controller.injection_stopped.connect(
            self.inject_tab.injection_stopped
        )

        self.injection_controller.status_changed.connect(
            self.statusBar().showMessage
        )

        # ---------------------------------------------------------
        # Mode Switching
        # ---------------------------------------------------------

        def start_replay(self):
            """
            Starts Replay mode.

            If Injection is running, stop it first.
            """

            if self.injection_controller.is_running():

                self.injection_controller.stop()

            self.replay_controller.start()


        # ---------------------------------------------------------

        def start_injection(self):
            """
            Starts Injection mode.

            If Replay is running, stop it first.
            """

            if self.replay_controller.is_running():

                self.replay_controller.stop()

            self.injection_controller.start()