from copy import deepcopy

from models import DetectedObject
from config.replay_config import OBJECTS_PER_UPDATE


class ReplayFrameBuilder:
    """
    Converts one completed replay batch into a logical replay frame.

    Physical protocol:
        Update 1 : Objects 1,2,3
        Update 2 : Objects 1,2,3
        ...

    Logical replay frame:
        Objects 1...18
    """

    def build(self, batch_objects: list[DetectedObject]):
        frame = []
        for index, obj in enumerate(batch_objects):
            new_obj = deepcopy(obj)
            new_obj.slot = index + 1
            frame.append(new_obj)
        return frame