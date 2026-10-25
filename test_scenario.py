from injection.scenario import Scenario
from models import DetectedObject, ObjectType

scenario = Scenario(
    name="CarCentric"
)

scenario.add_object(

    DetectedObject(
        slot=1,
        object_type=ObjectType.CAR,
        x=4200,
        y=120,
    )
)

scenario.add_object(

    DetectedObject(
        slot=2,
        object_type=ObjectType.TRUCK,
        x=6500,
        y=-80,
    )
)

print(scenario)

print("Valid :", scenario.is_valid())

print("Objects :", scenario.object_count())

for obj in scenario:
    print(obj)