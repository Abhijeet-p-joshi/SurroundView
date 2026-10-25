from PySide6.QtCore import QObject, Signal

from canoe.canoe_interface import CANoeInterface

from injection.scheduler import Scheduler
from injection.transmitter import Transmitter
from injection.scenario import Scenario
from injection.scenario_buffer import ScenarioBuffer

from controllers.visualization_controller import VisualizationController


class InjectionController(QObject):
    """
    Controls scenario injection.

    Responsibilities
    ----------------
    - Accept scenarios from the Scenario Editor
    - Update the visualization immediately
    - Store the active scenario
    - Start/Stop cyclic transmission
    """

    status_changed = Signal(str)

    def __init__(
        self,
        visualization: VisualizationController,
    ):

        super().__init__()

        self.visualization = visualization

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
        Called by ScenarioEditor.

        Stores the scenario and immediately updates the
        visualization.
        """

        self.buffer.set_scenario(scenario)

        self.visualization.show_objects(
            scenario.sorted_objects()
        )

        self.status_changed.emit(
            f"Scenario loaded ({scenario.object_count()} objects)"
        )

    # ---------------------------------------------------------
    # Injection
    # ---------------------------------------------------------

    def start(self):

        print("InjectionController.start()")
        if self.running:
            return

        if not self.buffer.has_scenario():

            self.status_changed.emit(
                "No scenario loaded"
            )

            return

        self.scheduler.start()

        self.running = True

        self.status_changed.emit(
            "Injection Started"
        )

    # ---------------------------------------------------------

    def stop(self):

        if not self.running:
            return

        self.scheduler.stop()

        self.canoe.write_update_bit(False)

        self.running = False

        self.status_changed.emit(
            "Injection Stopped"
        )

    # ---------------------------------------------------------

    def is_running(self):

        return self.running

    # ---------------------------------------------------------

    def has_scenario(self):

        return self.buffer.has_scenario()

    # ---------------------------------------------------------

    def current_scenario(self):

        return self.buffer.get_scenario()