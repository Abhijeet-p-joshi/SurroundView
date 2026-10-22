from canoe.canoe_interface import CANoeInterface
class SurroundViewController:

    def __init__(self, visualization):

        self.visualization = visualization
        self.canoe = CANoeInterface()

    def update_objects(self, objects):
        """
        Updates visualization and CANoe.
        """

        # Update visualization
        self.visualization.update_objects(objects)

        # Write every object to CANoe
        for obj in objects:
            self.canoe.write_object(obj)

        print(f"Updated {len(objects)} objects")

    def object_dragged(self, slot, x, y):

        obj = self.visualization.object_map[slot]

        obj.x = x
        obj.y = y

        self.canoe.write_object(obj)

        print(f"Slot {slot} updated")