import sys

from PySide6.QtWidgets import QApplication

from visualization.surround_view_widget import SurroundViewWidget
from controllers.visualization_controller import VisualizationController
from controllers.injection_controller import InjectionController

from injection.scenario import Scenario

from models import (
    DetectedObject,
    ObjectType,
)


app = QApplication(sys.argv)

# -------------------------------------------------
# Visualization
# -------------------------------------------------

widget = SurroundViewWidget()

visualization = VisualizationController(widget)

# -------------------------------------------------
# Injection Controller
# -------------------------------------------------

controller = InjectionController(
    visualization
)

controller.status_changed.connect(print)

# -------------------------------------------------
# Create Scenario
# -------------------------------------------------

scenario = Scenario(
    name="Injection Test"
)

for i in range(18):

    if i % 3 == 0:
        obj_type = ObjectType.CAR

    elif i % 3 == 1:
        obj_type = ObjectType.TRUCK

    else:
        obj_type = ObjectType.BIKE

    scenario.add_object(

        DetectedObject(

            slot=i + 1,

            object_type=obj_type,

            x=1000 + i * 500,

            y=-200 + i * 20,

        )
    )

# -------------------------------------------------
# Apply Scenario
# -------------------------------------------------

controller.apply_scenario(
    scenario
)

widget.show()

# -------------------------------------------------
# Start Injection
# -------------------------------------------------

controller.start()

sys.exit(app.exec())