import sys

from PySide6.QtWidgets import QApplication

from replay.replay_reader import ReplayReader


def on_batch_ready(objects):

    print("\n==============================")
    print("Batch Received")
    print("==============================")
    print(f"Objects : {len(objects)}")

    for obj in objects:

        print(
            f"Slot={obj.slot} | "
            f"Type={obj.object_type.name:<6} | "
            f"X={obj.x:8.1f} | "
            f"Y={obj.y:8.1f}"
        )


app = QApplication(sys.argv)

reader = ReplayReader()

reader.batch_ready.connect(on_batch_ready)

reader.start()

sys.exit(app.exec())