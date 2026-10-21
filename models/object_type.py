from enum import IntEnum
class ObjectType(IntEnum):
    CAR = 0
    BIKE = 1
    TRUCK = 2

    @property
    def display_name(self):
        return self.name.capitalize()