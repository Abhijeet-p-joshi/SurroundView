from PySide6.QtCore import QObject

from visualization.surround_view_widget import SurroundViewWidget
from models import DetectedObject


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

    def clear(self):
        """
        Remove all displayed objects.
        """

        self._objects.clear()

        self.widget.update_objects([])

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    def current_objects(self):

        return list(self._objects)

    def object_count(self):

        return len(self._objects)

    def is_empty(self):

        return len(self._objects) == 0

    # ---------------------------------------------------------

    def get_object(self, slot):

        for obj in self._objects:

            if obj.slot == slot:
                return obj

        return None