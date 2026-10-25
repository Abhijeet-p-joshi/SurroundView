from PySide6.QtCore import QCoreApplication

import sys

from canoe.canoe_interface import CANoeInterface

from injection.scenario import Scenario
from injection.scenario_buffer import ScenarioBuffer
from injection.transmitter import Transmitter

from models import (
    DetectedObject,
    ObjectType,
)

app = QCoreApplication(sys.argv)

scenario = Scenario("Test")

for i in range(18):

    scenario.add_object(

        DetectedObject(

            slot=i + 1,

            object_type=ObjectType.CAR,

            x=1000 * (i + 1),

            y=i * 10,

        )
    )

buffer = ScenarioBuffer()

buffer.set_scenario(scenario)

canoe = CANoeInterface()

tx = Transmitter(
    canoe,
    buffer,
)

tx.start_cycle()

for slot in range(6):

    tx.transmit_slot(slot)

tx.finish_cycle()