import win32com.client
from canoe.signal_mapping import SIGNALS

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

    def read_signal(self, short_name):
        """
        Read a signal value from CANoe.
        """

        return self.get_signal(short_name).Value

    def write_signal(self, short_name, value):
        """
        Write a signal value to CANoe.
        """

        self.get_signal(short_name).Value = value

    def write_object(self, obj):
        """
        Writes one detected object to CANoe.
        """

        mapping = SIGNALS[obj.slot]

        self.write_signal(mapping["x"], obj.x)
        self.write_signal(mapping["y"], obj.y)
        self.write_signal(mapping["type"], int(obj.object_type.value))