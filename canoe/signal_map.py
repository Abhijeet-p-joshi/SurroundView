"""
Signal map used for Replay Mode.

These are FullSignalNames returned by CANoe.
"""

# --------------------------------------------------
# Protocol signals
# --------------------------------------------------

from dataclasses import dataclass

PDU = "Backbone::ASDM::ASDMBackBoneSignalIPdu20::"

@dataclass(frozen=True)
class ObjectSignalSet:
    slot: int
    x: str
    y: str
    obj_type: str

UPDATE_BIT = (
    PDU + "SurroundObj_UB"
)

SURROUNDOBJ_UB_CONTROL = (
    "ASDM::Backbone::Signals::Control::UB::SurroundObj_UB_Control"
)

BATCH_COUNTER = (
    PDU + "SurroundObj28BatchCounter"
)

OBJECT_SIGNALS = [

    ObjectSignalSet(
        slot=1,
        x= PDU + "SurroundObj3x",
        y= PDU + "SurroundObj4y",
        obj_type= PDU + "SurroundObj2Type"
    ),

    ObjectSignalSet(
        slot=2,
        x= PDU + "SurroundObj12x",
        y= PDU + "SurroundObj13y",
        obj_type= PDU + "SurroundObj11Type"
    ),

    ObjectSignalSet(
        slot=3,
        x= PDU + "SurroundObj21x",
        y= PDU + "SurroundObj22y",
        obj_type= PDU + "SurroundObj20Type"
    ),
]

SIGNAL_UB_ON = 3
SIGNAL_UB_OFF = 0