from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QApplication

from canoe.canoe_interface import CANoeInterface
from canoe.preview_canoe_interface import PreviewCANoeInterface

from controllers.visualization_controller import VisualizationController

from injection.scenario import Scenario


class InjectionController(QObject):
    """
    Controls Injection Mode.

    Responsibilities
    ----------------
    • Accept scenarios from InjectTab
    • Update visualization immediately
    • Store the active scenario
    • Start / Stop scheduler
    """

    status_changed = Signal(str)

    injection_started = Signal()

    injection_stopped = Signal()

    def __init__(
        self,
        visualization,
        preview_mode=False,
    ):
        super().__init__()
        self.visualization = visualization

        #
        # Backend
        #

        if preview_mode:
            self.canoe = PreviewCANoeInterface()
        else:
            self.canoe = CANoeInterface()

        self.current_scenario = None

        self.running = False

    # ---------------------------------------------------------
    # Scenario
    # ---------------------------------------------------------

    def apply_scenario(
        self,
        scenario: Scenario,
    ):
        """
        Called when Apply Scenario is pressed.
        """

        if scenario is None:
            return

        if scenario.object_count() == 0:
            self.status_changed.emit(
                "Scenario contains no enabled objects."
            )
            return

        QApplication.setOverrideCursor(
            Qt.WaitCursor
        )
        QApplication.processEvents()

        try:
            self.status_changed.emit("Applying scenario...")
            self.current_scenario = scenario         # Store scenario
            self.canoe.write_scenario(               # Load objects into CANoe
                scenario.sorted_objects()
            )
            self.visualization.show_objects(         # Update visualization
                scenario.sorted_objects()
            )
            self.status_changed.emit(f"Scenario Applied ({scenario.object_count()} objects)")

        finally:
            QApplication.restoreOverrideCursor()

    # ---------------------------------------------------------
    # Injection
    # ---------------------------------------------------------

    def start(self):

        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()

        try:
            self.status_changed.emit(
                "Starting injection..."
            )
            self.canoe.start_injection()
            self._running = True
            self.injection_started.emit()
            self.status_changed.emit(
                "Injection started."
            )

        finally:
            QApplication.restoreOverrideCursor()

    # ---------------------------------------------------------

    def stop(self):

        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()

        try:
            self.status_changed.emit(
                "Stopping injection..."
            )
            self.canoe.stop_injection()
            self._running = False
            self.injection_stopped.emit()
            self.status_changed.emit(
                "Injection stopped."
            )

        finally:
            QApplication.restoreOverrideCursor()

    # ---------------------------------------------------------

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    # ---------------------------------------------------------

    def clear(self):
        self.stop()
        self.current_scenario = None
        self.canoe.clear_scenario()
        self.visualization.clear()
        self.status_changed.emit(
            "Scenario Cleared"
        )

    # ---------------------------------------------------------

    def get_current_scenario(self):
        return self.current_scenario

    # ---------------------------------------------------------

    def has_scenario(self):
        return self.current_scenario is not None

    # ---------------------------------------------------------

    def is_running(self):
        return self.running