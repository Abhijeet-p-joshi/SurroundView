"""
Defines the replay protocol.

Each update from CANoe contains three objects.

One replay batch consists of six updates.

3 objects/update × 6 updates = 18 objects
"""

OBJECTS_PER_UPDATE = 3

UPDATES_PER_BATCH = 6

OBJECTS_PER_BATCH = (
    OBJECTS_PER_UPDATE *
    UPDATES_PER_BATCH
)