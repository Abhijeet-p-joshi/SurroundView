from PySide6.QtCore import QObject, Signal

from replay.replay_reader import ReplayReader
from replay.replay_frame_builder import ReplayFrameBuilder


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
        self.frame_builder = ReplayFrameBuilder()

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
        """
        Receives one completed replay batch (18 DetectedObjects)
        from the ReplayReader, converts it into a logical replay
        frame and forwards it to the visualization.
        """

        self.batch_count += 1

        frame = self.frame_builder.build(objects)

        self.batch_updated.emit(frame)

    def is_running(self):

        return self.running