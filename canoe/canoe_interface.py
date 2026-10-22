import win32com.client
from canoe.signal_mapping import SIGNALS
from canoe.signal_map import (
    UPDATE_BIT,
    OBJECT_SIGNALS,
    BATCH_COUNTER
)
from models import DetectedObject, ObjectType
from config.object_types import OBJECT_TYPE_MAP, ECU_OBJECT_TYPE_MAP
from config.replay_config import OBJECTS_PER_UPDATE

class CANoeInterface:
    """
    Handles communication with CANoe through the COM interface.
    """

    def __init__(self):
        print("CANoeInterface constructor called")
        
        self.canoe = win32com.client.gencache.EnsureDispatch(
            "CANoe.Application"
        )

        if not self.canoe.Measurement.Running:
            raise RuntimeError("CANoe Measurement is not running.")

        # Cache signal COM objects
        self.signal_cache = {}

        # Preload all signals
        self._preload_signals()

        print("Connected to CANoe.")

    def _preload_signals(self):

        for mapping in SIGNALS.values():

            self.get_signal(mapping["x"])
            self.get_signal(mapping["y"])
            self.get_signal(mapping["type"])

    def get_signal(self, short_name):
        """
        Returns a cached CANoe Signal object.
        """

        if short_name not in self.signal_cache:

            full_name = self.canoe.Signals.FullSignalName(short_name)

            signal = self.canoe.Signals.Item(full_name)

            self.signal_cache[short_name] = signal

        return self.signal_cache[short_name]

    def read_update_bit(self):

        value = self.read_signal(UPDATE_BIT)

        if value is None:
            return False

        return bool(value)

    def read_signal(self, full_signal_name):
        """
        Reads a CANoe signal using its FullSignalName.
        """

        try:
            signal = self.canoe.Signals.Item(full_signal_name)
            return signal.Value

        except Exception as e:
            print(f"Failed to read {full_signal_name}: {e}")
            return None

    def write_signal(self, short_name, value):
        """
        Write a signal value to CANoe.
        """

        self.get_signal(short_name).Value = value

    def write_object(self, obj):
        """
        Writes one detected object to CANoe.
        """
        signal_set = next(
            signal
            for signal in OBJECT_SIGNALS
            if signal.slot == obj.slot
        )

        self.write_signal(
            signal_set.x,
            obj.x
        )
        self.write_signal(
            signal_set.y,
            obj.y
        )
        self.write_signal(
            signal_set.obj_type,
            ECU_OBJECT_TYPE_MAP[obj.object_type]
        )

    def decode_object_type(self, value):
        """
        Converts ECU object type value to ObjectType enum.
        """

        return OBJECT_TYPE_MAP.get(value, ObjectType.CAR)

    def read_current_objects(self):
        """
        Reads one replay update from CANoe.
        One replay update contains OBJECTS_PER_UPDATE objects.
        """

        objects = []

        for signal_set in OBJECT_SIGNALS[:OBJECTS_PER_UPDATE]:

            x = self.read_signal(signal_set.x)
            y = self.read_signal(signal_set.y)
            obj_type = self.read_signal(signal_set.obj_type)

            obj = DetectedObject(
                slot=signal_set.slot,
                object_type=self.decode_object_type(obj_type),
                x=x,
                y=y,
            )

            objects.append(obj)

        return objects

    def read_batch_counter(self):
        """
        Reads the current batch counter (0..15).
        """

        value = self.read_signal(BATCH_COUNTER)

        if value is None:
            return 0

        return int(value)

#Temporary
    def debug_print_objects(self):

        objects = self.read_current_objects()

        print("--------------------------------")

        for obj in objects:

            print(
                obj.slot,
                obj.object_type,
                obj.x,
                obj.y
            )