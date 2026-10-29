import win32com.client
import pythoncom
import pywintypes

from models import DetectedObject
from models.object_type import ObjectType

from config.ecu_object_types import (
    from_ecu,
    to_ecu,
)
from config.ecu_lane_positions import to_ecu_lane

from canoe.system_variables import (
    INJECTION_ENABLE,
    OBJ_X,
    OBJ_Y,
    OBJ_TYPE,
    LANES,
)

from models.lane import Lane

class CANoeInterface:
    """
    Handles communication with CANoe through the COM interface.
    """

    def __init__(self):

        pythoncom.CoInitialize()

        try:
            self.canoe = win32com.client.Dispatch("CANoe.Application")
            print("Connected to CANoe.")
        except Exception as e:
            raise RuntimeError(
                "CANoe is not running."
            ) from e
        
        if self.canoe.Measurement.Running:
            print("CANoe Measurement Running")
        else:
            print("CANoe Connected. Measurement Stopped.")

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

        if len(objects) > 18:
            raise ValueError(
                "Maximum 18 objects allowed."
            )

        # Make a copy
        objects = list(objects)

        # Pad remaining slots with NONE objects
        while len(objects) < 18:

            objects.append(
                DetectedObject(
                    slot=len(objects) + 1,
                    x=0.0,
                    y=0.0,
                    object_type=ObjectType.NONE,
                )
            )

        # Write all 18 slots
        for i, obj in enumerate(objects):

            if obj.object_type == ObjectType.NONE:

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

            else:

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

    def write_lane(
        self,
        lane: Lane,
        lane_index: int,
    ):

        print(f"write_lane() called: {lane.name}")
        variables = LANES[lane_index]

        self.write_system_variable(
            variables[0],
            lane.a,
        )

        self.write_system_variable(
            variables[1],
            lane.b,
        )

        self.write_system_variable(
            variables[2],
            lane.c,
        )

        self.write_system_variable(
            variables[3],
            lane.d1,
        )

        self.write_system_variable(
            variables[4],
            lane.d2,
        )

        self.write_system_variable(
            variables[5],
            lane.position.value,
        )

    def write_lanes(self, lanes):

        if len(lanes) != 4:
            raise ValueError("Exactly four lanes required.")

        for index, lane in enumerate(lanes):

            print(f"Writing Lane {lane.name}")

            self.write_lane(
                lane,
                index,
            )

        print("Lane geometry written to CANoe.")

    def is_measurement_running(self) -> bool:
        try:
            return self.canoe.Measurement.Running
        except Exception:
            return False