from dataclasses import dataclass, field
from typing import List

from models import DetectedObject


@dataclass
class Scenario:
    """
    Represents one complete injection scenario.

    A scenario contains up to 18 detected objects that are
    cyclically transmitted to CANoe.

    This class is independent of the GUI and CANoe.
    """

    name: str = "Untitled Scenario"

    objects: List[DetectedObject] = field(default_factory=list)

    # ---------------------------------------------------------
    # Object Management
    # ---------------------------------------------------------

    def add_object(self, obj: DetectedObject):

        self.objects.append(obj)

    def set_objects(self, objects: List[DetectedObject]):

        self.objects = list(objects)

    def clear(self):

        self.objects.clear()

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    def get_objects(self) -> List[DetectedObject]:

        return list(self.objects)

    def get_object(self, slot: int):

        for obj in self.objects:

            if obj.slot == slot:
                return obj

        return None

    def object_count(self):

        return len(self.objects)

    def is_empty(self):

        return len(self.objects) == 0

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def is_valid(self):

        """
        Basic validation.

        Rules:
            - Maximum 18 objects
            - Slot numbers unique
            - Slot numbers between 1 and 18
        """

        if len(self.objects) > 18:
            return False

        slots = set()

        for obj in self.objects:

            if obj.slot < 1 or obj.slot > 18:
                return False

            if obj.slot in slots:
                return False

            slots.add(obj.slot)

        return True

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def sorted_objects(self):

        return sorted(
            self.objects,
            key=lambda obj: obj.slot
        )

    def replace(self, scenario):

        """
        Replace the contents with another scenario.
        """

        self.name = scenario.name
        self.objects = list(scenario.objects)

    def __len__(self):

        return len(self.objects)

    def __iter__(self):

        return iter(self.objects)

    def __str__(self):

        return (
            f"{self.name} "
            f"({len(self.objects)} objects)"
        )