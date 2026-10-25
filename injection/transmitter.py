from PySide6.QtCore import QObject

from canoe.canoe_interface import CANoeInterface
from injection.scenario_buffer import ScenarioBuffer
from config.replay_config import OBJECTS_PER_UPDATE


class Transmitter(QObject):
    """
    Transmits one scenario to CANoe.

    Scheduler:
        Slot 0 -> Objects 1-3
        Slot 1 -> Objects 4-6
        ...
        Slot 5 -> Objects 16-18
    """

    def __init__(
        self,
        canoe: CANoeInterface,
        scenario_buffer: ScenarioBuffer,
    ):

        super().__init__()

        self.canoe = canoe

        self.buffer = scenario_buffer

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def start_cycle(self):
        """
        Beginning of an 80 ms cycle.

        Update Bit becomes HIGH.
        """

        self.canoe.write_update_bit(True)

    def finish_cycle(self):
        """
        End of active transmission.

        Update Bit becomes LOW.
        """

        self.canoe.write_update_bit(False)

    def transmit_slot(self, slot_index: int):
        """
        Transmits one scheduler slot.

        Each slot consists of three objects that are
        written into the three physical CANoe
        object signal groups.
        """

        print("=" * 60)
        print(f"transmit_slot({slot_index})")

        objects = self.buffer.get_objects()

        start = slot_index * OBJECTS_PER_UPDATE

        end = start + OBJECTS_PER_UPDATE

        slot_objects = objects[start:end]

        if len(slot_objects) != OBJECTS_PER_UPDATE:
            return

        print(f"\nTransmit Slot {slot_index + 1}")

        for signal_group, obj in enumerate(slot_objects):

            print(
                f"  Group {signal_group}"
                f" -> Slot {obj.slot}"
                f"  {obj.object_type.name}"
                f"  X={obj.x}"
                f"  Y={obj.y}"
            )

            self.canoe.write_object(
                signal_group,
                obj,
            )

    # ---------------------------------------------------------

    def has_scenario(self):

        return self.buffer.has_scenario()

    def object_count(self):

        return self.buffer.object_count()