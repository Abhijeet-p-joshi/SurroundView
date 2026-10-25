from injection.scenario import Scenario
from injection.scenario_buffer import ScenarioBuffer

from models import (
    DetectedObject,
    ObjectType,
)

buffer = ScenarioBuffer()

print(buffer)

scenario = Scenario(
    name="CarCentric"
)

scenario.add_object(

    DetectedObject(
        slot=1,
        object_type=ObjectType.CAR,
        x=4200,
        y=100,
    )
)

scenario.add_object(

    DetectedObject(
        slot=2,
        object_type=ObjectType.TRUCK,
        x=6500,
        y=-120,
    )
)

buffer.set_scenario(scenario)

print(buffer)

print()

print("Name :", buffer.scenario_name())

print("Objects :", buffer.object_count())

print("Valid :", buffer.is_valid())

print()

for obj in buffer.get_objects():

    print(obj)

buffer.clear()

print()

print(buffer)