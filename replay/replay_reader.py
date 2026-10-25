from PySide6.QtCore import QObject, Signal, QTimer

from canoe.canoe_interface import CANoeInterface
from replay.batch_processor import BatchProcessor
from config.replay_config import POLL_INTERVAL_MS


class ReplayReader(QObject):
    """
    Reads CANoe replay data every POLL_INTERVAL_MS.

    Emits one complete batch (18 objects)
    whenever available.
    """

    batch_ready = Signal(list)

    def __init__(self):

        super().__init__()

        self.canoe = CANoeInterface()

        self.processor = BatchProcessor()

        self.timer = QTimer()

        self.timer.timeout.connect(self.poll)

    def start(self):

        print("Replay started")

        self.processor.reset()

        self.timer.start(POLL_INTERVAL_MS)

    def stop(self):

        print("Replay stopped")

        self.timer.stop()

        self.processor.reset()

    # def poll(self):
    #     print("Polling...")
    #     update_bit = self.canoe.read_update_bit()

    #     objects = self.canoe.read_current_objects()

    #     completed_batch = self.processor.process(
    #         update_bit,
    #         objects
    #     )

    #     if completed_batch is not None:
    #         self.batch_ready.emit(completed_batch)

    def poll(self):

        print("\n==============================")

        update_bit = self.canoe.read_update_bit()

        print(f"Update Bit : {update_bit}")

        objects = self.canoe.read_current_objects()

        for obj in objects:

            print(
                f"Slot={obj.slot} "
                f"Type={obj.object_type.name} "
                f"X={obj.x} "
                f"Y={obj.y}"
            )

        completed_batch = self.processor.process(
            update_bit,
            objects
        )

        if completed_batch is not None:

            print(f"Batch Ready : {len(completed_batch)} objects")

            self.batch_ready.emit(completed_batch)