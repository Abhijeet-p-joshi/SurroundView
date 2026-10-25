from PySide6.QtCore import QObject, QTimer

from injection.transmitter import Transmitter


class Scheduler(QObject):
    """
    Executes the cyclic 80 ms transmission schedule.

    Timeline

        0 ms   -> Update Bit HIGH + Slot 1
        5 ms   -> Slot 2
        10 ms  -> Slot 3
        15 ms  -> Slot 4
        20 ms  -> Slot 5
        25 ms  -> Slot 6
        30 ms  -> Update Bit LOW
        30-80 ms -> Idle
    """

    SLOT_TIME_MS = 5
    ACTIVE_SLOTS = 6
    IDLE_TIME_MS = 50

    def __init__(self, transmitter: Transmitter):

        super().__init__()

        self.transmitter = transmitter

        self.timer = QTimer()

        self.timer.timeout.connect(self._tick)

        self.slot_index = 0

        self.running = False

    # ---------------------------------------------------------

    def start(self):

        print("Scheduler started")
        if self.running:
            return

        self.running = True

        self.slot_index = 0

        self.transmitter.start_cycle()

        self.timer.start(self.SLOT_TIME_MS)

    # ---------------------------------------------------------

    def stop(self):

        if not self.running:
            return

        self.running = False

        self.timer.stop()

        self.slot_index = 0

        self.transmitter.finish_cycle()

    # ---------------------------------------------------------

    def _tick(self):

        print(f"Tick {self.slot_index}")

        if not self.running:
            return

        if self.slot_index < self.ACTIVE_SLOTS:

            print(f"Transmit Slot {self.slot_index + 1}")

            try:
                self.transmitter.transmit_slot(
                    self.slot_index
                )
            except Exception:
                import traceback
                traceback.print_exc()

            print(f"Before increment: {self.slot_index}")

            self.slot_index += 1

            print(f"After increment : {self.slot_index}")

            return

        print("Cycle Finished")

        self.timer.stop()

        self.transmitter.finish_cycle()

        self.slot_index = 0

        QTimer.singleShot(
            self.IDLE_TIME_MS,
            self._restart_cycle,
        )

    # ---------------------------------------------------------

    def _restart_cycle(self):

        if not self.running:
            return

        self.transmitter.start_cycle()

        self.timer.start(self.SLOT_TIME_MS)

    # ---------------------------------------------------------

    def is_running(self):

        return self.running