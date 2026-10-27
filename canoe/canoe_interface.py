import win32com.client
# from canoe.signal_mapping import SIGNALS

from models import DetectedObject

from config.ecu_object_types import (
    from_ecu,
    to_ecu,
)

from canoe.system_variables import (
    INJECTION_ENABLE,
    OBJ_X,
    OBJ_Y,
    OBJ_TYPE,
)

class CANoeInterface:
    """
    Handles communication with CANoe through the COM interface.
    """

    def __init__(self):
        
        self.canoe = win32com.client.gencache.EnsureDispatch(
            "CANoe.Application"
        )
        if not self.canoe.Measurement.Running:
            raise RuntimeError("CANoe Measurement is not running.")

        # self._load_capl_functions()
        # # Cache signal COM objects
        # self.signal_cache = {}

        # # Preload all signals
        # self._preload_signals()

        print("Connected to CANoe.")

    # def _preload_signals(self):

    #     for mapping in SIGNALS.values():

    #         self.get_signal(mapping["x"])
    #         self.get_signal(mapping["y"])
    #         self.get_signal(mapping["type"])

    # def get_signal(self, short_name):

    #     if short_name not in self.signal_cache:

    #         full_name = self.canoe.Signals.FullSignalName(short_name)

    #         print(f"{short_name}  ->  {full_name}")

    #         signal = self.canoe.Signals.Item(full_name)

    #         self.signal_cache[short_name] = signal

    #     return self.signal_cache[short_name]

    # def read_update_bit(self):

    #     value = self.read_signal(UPDATE_BIT)

    #     if value is None:
    #         return False

    #     return bool(value)

    # def read_signal(self, full_signal_name):
    #     """
    #     Reads a CANoe signal using its FullSignalName.
    #     """

    #     try:
    #         signal = self.canoe.Signals.Item(full_signal_name)
    #         return signal.Value

    #     except Exception as e:
    #         print(f"Failed to read {full_signal_name}: {e}")
    #         return None

    # def write_signal(self, full_signal_name: str, value):
    #     """
    #     Writes a CANoe signal using its FullSignalName.
    #     """
    #     try:
    #         signal = self.canoe.Signals.Item(full_signal_name)
    #         signal.Value = value
    #     except Exception as e:
    #         print(
    #             f"Failed to write {full_signal_name}: {e}"
    #         )

    # def write_update_bit(self, value: bool):
    #     """
    #     Controls the Update Bit through the CANoe System Variable.
    #     3 = Update Bit ON
    #     0 = Update Bit OFF
    #     """

    #     try:
    #         ns = self.canoe.System.Namespaces.Item("_SPACommon")
    #         var = ns.Variables.Item("UBControl")
    #         var.Value = SIGNAL_UB_ON if value else SIGNAL_UB_OFF
    #         print(f"UBControl = {var.Value}")

    #     except Exception as e:
    #         print(f"Failed to write UBControl: {e}")

    # def write_object(
    #     self,
    #     signal_group: int,
    #     obj: DetectedObject,
    # ):
    #     """
    #     Writes one object into one of the three
    #     physical CANoe object signal groups.

    #     signal_group:
    #         0
    #         1
    #         2
    #     """
    #     print(
    #         f"type={obj.object_type.name} "
    #         f"x={obj.x} "
    #         f"y={obj.y}"
    #     )

    #     signal_set = OBJECT_SIGNALS[signal_group]

    #     self.write_signal(
    #         signal_set.x,
    #         obj.x,
    #     )

    #     self.write_signal(
    #         signal_set.y,
    #         obj.y,
    #     )

    #     self.write_signal(
    #         signal_set.obj_type,
    #         to_ecu(obj.object_type),
    #     )

    #     print(
    #         f"type={obj.object_type.name} "
    #         f"x={obj.x} "
    #         f"y={obj.y}"
    #     )

    # def decode_object_type(self, value):
    #     """
    #     Converts ECU value into application ObjectType.
    #     """
    #     try:
    #         return from_ecu(value)
    #     except KeyError:
    #         print(f"Unknown ECU Object Type: {value}")
    #         return from_ecu(10)   # default = CAR

    # def read_current_objects(self):
    #     """
    #     Reads one replay update from CANoe.
    #     One replay update contains OBJECTS_PER_UPDATE objects.
    #     """

    #     objects = []

    #     for signal_set in OBJECT_SIGNALS[:OBJECTS_PER_UPDATE]:

    #         x = self.read_signal(signal_set.x)
    #         y = self.read_signal(signal_set.y)
    #         obj_type = self.read_signal(signal_set.obj_type)

    #         obj = DetectedObject(
    #             slot=signal_set.slot,
    #             object_type=self.decode_object_type(obj_type),
    #             x=x,
    #             y=y,
    #         )

    #         objects.append(obj)

    #     return objects

    # def read_batch_counter(self):
    #     """
    #     Reads the current batch counter (0..15).
    #     """

    #     value = self.read_signal(BATCH_COUNTER)

    #     if value is None:
    #         return 0

    #     return int(value)

    def write_system_variable(
        self,
        full_name: str,
        value,
    ):
        """
        Writes one CANoe System Variable.

        Example:

            ASDM::Obj01_X
        """

        try:

            namespace_name, variable_name = full_name.split("::")

            namespace = self.canoe.System.Namespaces.Item(
                namespace_name
            )

            variable = namespace.Variables.Item(
                variable_name
            )

            variable.Value = value

        except Exception as e:

            print(
                f"Failed writing {full_name}: {e}"
            )

    def write_scenario(
        self,
        objects,
    ):
        """
        Writes the complete scenario into
        CANoe System Variables.
        """

        if len(objects) != 18:

            raise ValueError(
                "Scenario must contain exactly 18 objects."
            )

        for i, obj in enumerate(objects):

            self.write_system_variable(
                OBJ_X[i],
                obj.x,
            )

            self.write_system_variable(
                OBJ_Y[i],
                obj.y,
            )

            self.write_system_variable(
                OBJ_TYPE[i],
                to_ecu(
                    obj.object_type
                ),
            )

        print("Scenario written to CANoe.")

    # def load_scenario(self, scenario):
    #     for obj in scenario.sorted_objects():
    #         self.write_system_variable(
    #             OBJECT_X.format(obj.slot),
    #             obj.x,
    #         )
    #         self.write_system_variable(
    #             OBJECT_Y.format(obj.slot),
    #             obj.y,
    #         )
    #         self.write_system_variable(
    #             OBJECT_TYPE.format(obj.slot),
    #             to_ecu(obj.object_type),
    #         )

    def start_injection(self):

        self.write_system_variable(
            INJECTION_ENABLE,
            1,
        )

        print("Injection Enabled")


    def stop_injection(self):

        self.write_system_variable(
            INJECTION_ENABLE,
            0,
        )

        print("Injection Disabled")

    def clear_scenario(self):
        """
        Clears all scenario variables.
        """

        self.stop_injection()

        for i in range(18):

            self.write_system_variable(
                OBJ_X[i],
                0.0,
            )

            self.write_system_variable(
                OBJ_Y[i],
                0.0,
            )

            self.write_system_variable(
                OBJ_TYPE[i],
                0,
            )

        print("Scenario cleared.")