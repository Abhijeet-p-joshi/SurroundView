from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QFrame,
    QSplitter,
)

from visualization.surround_view_widget import SurroundViewWidget
from gui.control_panel import ControlPanel
from gui.scenario_editor import ScenarioEditor

from controllers.visualization_controller import VisualizationController
from controllers.replay_controller import ReplayController
from controllers.injection_controller import InjectionController


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SurroundView")
        self.resize(1400, 900)

        # -------------------------------------------------
        # Controllers
        # -------------------------------------------------

        self.visualization_controller = None
        self.replay_controller = None
        self.injection_controller = None

        self.scenario_editor = None

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        self._create_menu()
        self._create_ui()
        self._create_toolbar()

        self.statusBar().showMessage("Ready")

    # -----------------------------------------------------
    # UI
    # -----------------------------------------------------

    def _create_ui(self):

        splitter = QSplitter(Qt.Horizontal)

        left_panel = self._create_control_panel()
        right_panel = self._create_visualization_panel()

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        splitter.setSizes([300, 1100])

        self.setCentralWidget(splitter)

        # ---------------------------------------------
        # Controllers
        # ---------------------------------------------

        self.replay_controller = ReplayController()

        self.injection_controller = InjectionController(
            self.visualization_controller
        )

        # ---------------------------------------------
        # Connections
        # ---------------------------------------------

        self.replay_controller.batch_updated.connect(
            self.visualization_controller.show_objects
        )

        self.replay_controller.status_changed.connect(
            self.statusBar().showMessage
        )

        self.injection_controller.status_changed.connect(
            self.statusBar().showMessage
        )

    # -----------------------------------------------------

    def _create_control_panel(self):

        self.control_panel = ControlPanel()

        #
        # Manual object editing has been superseded by the
        # Scenario Editor. Therefore no connection is made
        # here anymore.
        #

        return self.control_panel

    # -----------------------------------------------------

    def _create_visualization_panel(self):

        panel = QFrame()

        layout = QVBoxLayout(panel)

        self.surround_view = SurroundViewWidget()

        self.visualization_controller = VisualizationController(
            self.surround_view
        )

        layout.addWidget(self.surround_view)

        return panel

    # -----------------------------------------------------

    def _create_menu(self):

        self.menuBar().addMenu("File")
        self.menuBar().addMenu("View")
        self.menuBar().addMenu("Tools")
        self.menuBar().addMenu("Help")

    # -----------------------------------------------------

    def _create_toolbar(self):

        toolbar = self.addToolBar("Main Toolbar")

        # ---------------------------------------------
        # Replay
        # ---------------------------------------------

        start_replay = QAction("Start Replay", self)
        stop_replay = QAction("Stop Replay", self)

        start_replay.triggered.connect(
            lambda: self.replay_controller.start()
        )

        stop_replay.triggered.connect(
            lambda: self.replay_controller.stop()
        )

        toolbar.addAction(start_replay)
        toolbar.addAction(stop_replay)

        toolbar.addSeparator()

        # ---------------------------------------------
        # Injection
        # ---------------------------------------------

        start_injection = QAction(
            "Start Injection",
            self,
        )

        stop_injection = QAction(
            "Stop Injection",
            self,
        )

        start_injection.triggered.connect(
            lambda: self.injection_controller.start()
        )

        stop_injection.triggered.connect(
            lambda: self.injection_controller.stop()
        )

        toolbar.addAction(start_injection)
        toolbar.addAction(stop_injection)

        toolbar.addSeparator()

        # ---------------------------------------------
        # Scenario Editor
        # ---------------------------------------------

        scenario_action = QAction(
            "Scenario Editor",
            self,
        )

        scenario_action.triggered.connect(
            self.open_scenario_editor
        )

        toolbar.addAction(scenario_action)

    # -----------------------------------------------------

    def open_scenario_editor(self):

        if self.scenario_editor is None:

            self.scenario_editor = ScenarioEditor()

            self.scenario_editor.scenarioApplied.connect(
                self.injection_controller.apply_scenario
            )

        self.scenario_editor.show()
        self.scenario_editor.raise_()
        self.scenario_editor.activateWindow()