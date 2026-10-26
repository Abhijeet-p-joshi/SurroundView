from PySide6.QtCore import QObject, Signal, QTimer

from canoe.canoe_interface import CANoeInterface
from canoe.preview_canoe_interface import PreviewCANoeInterface

from controllers.visualization_controller import VisualizationController


class ReplayController(QObject):
    """
    Controls Replay Mode.

    Responsibilities
    ----------------
    - Start replay
    - Stop replay
    - Read object batches from CANoe
    - Update the visualization
    """

    status_changed = Signal(str)

    replay_started = Signal()

    replay_stopped = Signal()

    batch_updated = Signal(list)

    REPLAY_PERIOD_MS = 80

    def __init__(
        self,
        visualization,
        preview_mode=False,
    ):
        super().__init__()

        self.visualization = visualization
        if preview_mode:
            self.canoe = PreviewCANoeInterface()
        else:
            self.canoe = CANoeInterface()
        self.timer = QTimer()
        self.timer.timeout.connect(
            self._update_cycle
        )
        self.running = False

    # ---------------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.timer.start(
            self.REPLAY_PERIOD_MS
        )

        self.replay_started.emit()

        self.status_changed.emit(
            "Replay Started"
        )

    # ---------------------------------------------------------

    def stop(self):

        if not self.running:
            return

        self.running = False

        self.timer.stop()

        self.replay_stopped.emit()

        self.status_changed.emit(
            "Replay Stopped"
        )

    # ---------------------------------------------------------

    def _update_cycle(self):

        objects = self.canoe.read_current_objects()

        self.visualization.show_objects(
            objects
        )

        self.batch_updated.emit(
            objects
        )

    # ---------------------------------------------------------

    def is_running(self):

        return self.running