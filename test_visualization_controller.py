import sys

from PySide6.QtWidgets import QApplication

from visualization.surround_view_widget import SurroundViewWidget
from controllers.visualization_controller import VisualizationController

from models import DetectedObject, ObjectType

app = QApplication(sys.argv)

widget = SurroundViewWidget()

controller = VisualizationController(widget)

widget.show()

objects = []

for slot in range(18):

    objects.append(

        DetectedObject(

            slot=slot + 1,

            object_type=ObjectType.CAR,

            x=1000 + slot * 500,

            y=-250 + slot * 30,

        )

    )

controller.show_objects(objects)

sys.exit(app.exec())