from dataclasses import dataclass
from models.object_type import ObjectType

@dataclass
class DetectedObject:
    slot: int
    object_type: ObjectType
    x: float
    y: float