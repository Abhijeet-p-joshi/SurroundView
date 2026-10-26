from models.object_type import ObjectType

"""
Conversion between the application ObjectType
and the ECU values used on FlexRay.

Application <-----> ECU
"""


APP_TO_ECU = {

    ObjectType.CAR: 10,
    ObjectType.BIKE: 5,
    ObjectType.TRUCK: 11,

}


ECU_TO_APP = {

    10: ObjectType.CAR,
    5: ObjectType.BIKE,
    11: ObjectType.TRUCK,

}


def to_ecu(object_type: ObjectType) -> int:
    """
    Converts an application object type
    into the ECU value.
    """
    return APP_TO_ECU[object_type]


def from_ecu(value: int) -> ObjectType:
    """
    Converts an ECU object type
    into the application enum.
    """
    return ECU_TO_APP[value]