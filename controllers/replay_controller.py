from PySide6.QtCore import QObject, Signal

from replay.replay_reader import ReplayReader


class ReplayController(QObject):
    """
    Controls CANoe replay.

    Responsibilities
    ----------------
    - Starts replay polling
    - Stops replay polling
    - Emits completed replay batches
    - Reports replay status

    Does NOT know anything about:
        - GUI
        - Visualization
        - CANoe signals
    """

    batch_updated = Signal(list)
    status_changed = Signal(str)

    def __init__(self):

        super().__init__()

        self.reader = ReplayReader()

        self.reader.batch_ready.connect(
            self._batch_received
        )

        self.running = False

        self.batch_counter = 0

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def start(self):

        if self.running:
            return

        self.batch_counter = 0

        self.reader.start()

        self.running = True

        self.status_changed.emit(
            "Replay Started"
        )

    # -----------------------------------------------------

    def stop(self):

        if not self.running:
            return

        self.reader.stop()

        self.running = False

        self.status_changed.emit(
            "Replay Stopped"
        )

    # -----------------------------------------------------

    def is_running(self):

        return self.running

    # -----------------------------------------------------

    def batch_count(self):

        return self.batch_counter

    # -----------------------------------------------------
    # Internal
    # -----------------------------------------------------

    def _batch_received(self, objects):

        self.batch_counter += 1

        print(
            f"Replay Batch {self.batch_counter}"
        )

        self.batch_updated.emit(objects)