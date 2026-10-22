from models import ObjectType

"""
Maps ECU object type values to application object types.
"""

OBJECT_TYPE_MAP = {

    5: ObjectType.BIKE,

    10: ObjectType.CAR,

    11: ObjectType.TRUCK,

}

ECU_OBJECT_TYPE_MAP = {

    ObjectType.BIKE: 5,

    ObjectType.CAR: 10,

    ObjectType.TRUCK: 11,

}