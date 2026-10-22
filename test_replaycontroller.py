import sys

from PySide6.QtWidgets import QApplication

from replay.replay_controller import ReplayController


def on_status(message):
    print(message)


def on_batch(objects):
    print(f"Batch received: {len(objects)} objects")


app = QApplication(sys.argv)

controller = ReplayController()

controller.status_changed.connect(on_status)

controller.batch_updated.connect(on_batch)

controller.start()

sys.exit(app.exec())