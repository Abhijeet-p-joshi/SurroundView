from PySide6.QtCore import QObject

from visualization.surround_view_widget import SurroundViewWidget
from models import DetectedObject
from models.lane import Lane


class VisualizationController(QObject):
    """
    Controls everything displayed inside the Surround View.

    Responsibilities
    ----------------
    - Own the currently displayed objects.
    - Update the visualization.
    - Provide the current visualization state.

    This controller contains no CANoe logic and no replay logic.
    """

    def __init__(self, widget: SurroundViewWidget):

        super().__init__()

        self.widget = widget

        self._objects = []

        self._lanes = []

    # ---------------------------------------------------------
    # Visualization
    # ---------------------------------------------------------

    def show_objects(
        self,
        objects: list[DetectedObject],
    ):
        """
        Display a new object list.
        """

        self._objects = list(objects)

        self.widget.update_objects(
            self._objects
        )

        print("VisualizationController")
        print(len(objects))

    # ---------------------------------------------------------

    def show_lanes(
        self,
        lanes: list[Lane],
    ):
        """
        Display lane geometry.
        """

        self._lanes = list(lanes)

        self.widget.update_lanes(
            self._lanes
        )

        print("VisualizationController")
        print(f"{len(lanes)} lanes")

    def clear(self):
        """
        Remove all displayed objects and lanes.
        """

        self._objects.clear()
        self._lanes.clear()

        self.widget.update_objects([])
        self.widget.update_lanes([])

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    def current_objects(self):
        return list(self._objects)

    def object_count(self):
        return len(self._objects)

    def is_empty(self):
        return len(self._objects) == 0

    def current_lanes(self):
        return list(self._lanes)

    def lane_count(self):
        return len(self._lanes)

    # ---------------------------------------------------------

    def get_object(self, slot):

        for obj in self._objects:

            if obj.slot == slot:
                return obj

        return None