from dataclasses import dataclass
from enum import Enum

class LanePosition(Enum):
    CLOSEST_LEFT = 0
    SECOND_CLOSEST_LEFT = 1
    CLOSEST_RIGHT = 2
    SECOND_CLOSEST_RIGHT = 3

DISPLAY_NAMES = {

    LanePosition.CLOSEST_LEFT:
        "Closest Left",

    LanePosition.SECOND_CLOSEST_LEFT:
        "Second Closest Left",

    LanePosition.CLOSEST_RIGHT:
        "Closest Right",

    LanePosition.SECOND_CLOSEST_RIGHT:
        "Second Closest Right",
}

@dataclass
class Lane:

    name: str

    a: float = 0.0
    b: float = 0.0
    c: float = 0.0
    d1: float = 0.0
    d2: float = 0.0

    position: LanePosition = LanePosition.CLOSEST_LEFT