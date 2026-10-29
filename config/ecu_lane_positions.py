from models.lane import LanePosition


def to_ecu_lane(position: LanePosition):

    mapping = {

        LanePosition.CLOSEST_LEFT: 0,
        LanePosition.SECOND_CLOSEST_LEFT: 1,
        LanePosition.CLOSEST_RIGHT: 2,
        LanePosition.SECOND_CLOSEST_RIGHT: 3,
    }

    return mapping[position]


def from_ecu_lane(value):

    mapping = {

        0: LanePosition.CLOSEST_LEFT,
        1: LanePosition.SECOND_CLOSEST_LEFT,
        2: LanePosition.CLOSEST_RIGHT,
        3: LanePosition.SECOND_CLOSEST_RIGHT,
    }

    return mapping[value]