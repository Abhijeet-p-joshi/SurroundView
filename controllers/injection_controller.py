from PySide6.QtCore import QObject, Signal

from canoe.canoe_interface import CANoeInterface

from controllers.visualization_controller import VisualizationController

from injection.scheduler import Scheduler
from injection.transmitter import Transmitter
from injection.scenario import Scenario
from injection.scenario_buffer import ScenarioBuffer


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
        visualization: VisualizationController,
    ):

        super().__init__()

        self.visualization = visualization

        #
        # Backend
        #

        self.canoe = CANoeInterface()

        self.buffer = ScenarioBuffer()

        self.transmitter = Transmitter(
            self.canoe,
            self.buffer,
        )

        self.scheduler = Scheduler(
            self.transmitter,
        )

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

        # Store scenario
        self.buffer.set_scenario(
            scenario
        )

        # Update visualization immediately
        self.visualization.show_objects(
            scenario.sorted_objects()
        )
        self.status_changed.emit(
            f"Scenario Applied ({scenario.object_count()} objects)"
        )

    # ---------------------------------------------------------
    # Injection
    # ---------------------------------------------------------

    def start(self):
        if self.running:
            return
        if not self.buffer.has_scenario():

            self.status_changed.emit(
                "No scenario loaded."
            )
            return
        self.scheduler.start()
        self.running = True
        self.injection_started.emit()
        self.status_changed.emit(
            "Injection Started"
        )

    # ---------------------------------------------------------

    def stop(self):
        if not self.running:
            return
        self.scheduler.stop()
        self.running = False
        self.injection_stopped.emit()
        self.status_changed.emit(
            "Injection Stopped"
        )

    # ---------------------------------------------------------

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    # ---------------------------------------------------------

    def clear(self):
        self.stop()
        self.buffer.clear()
        self.visualization.clear()
        self.status_changed.emit(
            "Scenario Cleared"
        )

    # ---------------------------------------------------------

    def current_scenario(self):
        return self.buffer.get_scenario()

    # ---------------------------------------------------------

    def has_scenario(self):
        return self.buffer.has_scenario()

    # ---------------------------------------------------------

    def is_running(self):
        return self.running