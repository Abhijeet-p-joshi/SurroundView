from models import DetectedObject


class SurroundViewController:

    def __init__(self, visualization):

        self.visualization = visualization

    def update_objects(self, objects: list[DetectedObject]):

        # Update visualization
        self.visualization.update_objects(objects)

        # CANoe update
        # (Next milestone)

        # Logger
        # (Future)

        # Recording
        # (Future)