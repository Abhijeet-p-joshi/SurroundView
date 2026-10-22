"""
Replay Configuration

All replay protocol parameters are defined here.
Changing ECU protocol should only require updating this file.
"""

# CANoe polling period
POLL_INTERVAL_MS = 5

# Protocol definition
OBJECTS_PER_UPDATE = 3
UPDATES_PER_BATCH = 6
OBJECTS_PER_BATCH = OBJECTS_PER_UPDATE * UPDATES_PER_BATCH