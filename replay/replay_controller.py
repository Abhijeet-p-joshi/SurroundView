from PySide6.QtCore import QObject, Signal

from replay.replay_reader import ReplayReader


class ReplayController(QObject):
    """
    Controls CANoe replay.
    """

    batch_updated = Signal(list)
    status_changed = Signal(str)

    def __init__(self):

        super().__init__()

        self.reader = ReplayReader()

        self.reader.batch_ready.connect(
            self._on_batch_ready
        )

        self.running = False
        self.batch_count = 0

    def start(self):

        if self.running:
            return

        self.batch_count = 0

        self.reader.start()

        self.running = True

        self.status_changed.emit(
            "Replay Started"
        )

    def stop(self):

        if not self.running:
            return

        self.reader.stop()

        self.running = False

        self.status_changed.emit(
            "Replay Stopped"
        )

    def _on_batch_ready(self, objects):

        self.batch_count += 1

        self.batch_updated.emit(objects)

    def is_running(self):

        return self.running