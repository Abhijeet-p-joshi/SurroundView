from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QApplication

from canoe.canoe_interface import CANoeInterface
from canoe.preview_canoe_interface import PreviewCANoeInterface

from injection.scenario_io import ScenarioIO

class LaneController(QObject):
    """
    Handles lane geometry editing.
    """

    status_changed = Signal(str)

    def __init__(
        self,
        visualization,
        preview_mode=False,
    ):
        super().__init__()

        self.visualization = visualization
        self.scenario_io = ScenarioIO()

        if preview_mode:
            self.canoe = PreviewCANoeInterface()
        else:
            self.canoe = CANoeInterface()

    def apply_lanes(self, lanes):

        QApplication.setOverrideCursor(
            Qt.WaitCursor
        )

        try:
            if len(lanes) != 4:
                self.status_changed.emit(
                    "Exactly four lanes required."
                )
                return

            self.canoe.write_lanes(lanes)

            self.visualization.show_lanes(lanes)

            self.scenario_io.save_lanes(lanes)

            self.status_changed.emit(
                "Lane geometry applied."
            )
        finally:
            QApplication.restoreOverrideCursor()