# test_batch_processor.py

from replay.batch_processor import BatchProcessor
from models import DetectedObject, ObjectType

processor = BatchProcessor()

def create_objects(slot):

    return [

        DetectedObject(
            slot=1,
            object_type=ObjectType.CAR,
            x=1000 + slot,
            y=100
        ),

        DetectedObject(
            slot=2,
            object_type=ObjectType.BIKE,
            x=2000 + slot,
            y=200
        ),

        DetectedObject(
            slot=3,
            object_type=ObjectType.TRUCK,
            x=3000 + slot,
            y=300
        ),

    ]


print("------------ START TEST ------------")

# Simulate Rising Edge
result = processor.process(True, create_objects(1))
print("Returned:", result)

# Remaining 5 updates
for i in range(2, 7):

    result = processor.process(True, create_objects(i))

    if result is not None:

        print("\nBatch Returned")
        print("------------------------")

        for obj in result:

            print(
                obj.object_type,
                obj.x,
                obj.y
            )

# Simulate Falling Edge
processor.process(False, [])

print("------------- END TEST -------------")