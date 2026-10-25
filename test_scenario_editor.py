import sys

from PySide6.QtWidgets import QApplication

from gui.scenario_editor import ScenarioEditor


def scenario_received(objects):

    print("\nScenario Applied")
    print("---------------------------")

    for obj in objects:

        print(
            f"Slot={obj.slot} | "
            f"{obj.object_type.name} | "
            f"X={obj.x} | "
            f"Y={obj.y}"
        )


app = QApplication(sys.argv)

editor = ScenarioEditor()

editor.scenarioApplied.connect(
    scenario_received
)

editor.csvLoaded.connect(
    lambda path: print(f"Loaded: {path}")
)

editor.show()

sys.exit(app.exec())