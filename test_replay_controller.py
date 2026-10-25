import sys

from PySide6.QtWidgets import QApplication

from controllers.replay_controller import ReplayController

app = QApplication(sys.argv)

controller = ReplayController()

controller.status_changed.connect(print)

controller.batch_updated.connect(

    lambda batch:
    print(
        f"Batch received ({len(batch)} objects)"
    )

)

controller.start()

sys.exit(app.exec())