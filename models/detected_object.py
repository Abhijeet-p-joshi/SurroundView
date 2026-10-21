from dataclasses import dataclass
from models.object_type import ObjectType

@dataclass
class DetectedObject:
    object_type: ObjectType
    x: float
    y: float