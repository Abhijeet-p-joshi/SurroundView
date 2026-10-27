import win32com.client
# from canoe.signal_mapping import SIGNALS

from models import DetectedObject

from models import ObjectType

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

            if obj.object_type.name == ObjectType.NONE:

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
                    3,          # NONE
                )

                continue

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
                to_ecu(obj.object_type),
            )

        print("Scenario written to CANoe.")

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
                to_ecu(ObjectType.NONE),
            )

        print("Scenario cleared.")