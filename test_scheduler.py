from PySide6.QtCore import QCoreApplication

from injection.scheduler import Scheduler

import sys

app = QCoreApplication(sys.argv)

scheduler = Scheduler()


def slot(slot):

    print(f"Transmit Slot {slot+1}")


scheduler.slot_triggered.connect(slot)

scheduler.cycle_started.connect(
    lambda: print("\n===== NEW CYCLE =====")
)

scheduler.cycle_finished.connect(
    lambda: print("Cycle Finished")
)

scheduler.start()

sys.exit(app.exec())