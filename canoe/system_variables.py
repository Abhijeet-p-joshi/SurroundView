"""
CANoe System Variable names.

These variables are used by the Python application
to load one scenario into CANoe.

CAPL will later consume these variables.
"""

INJECTION_ENABLE = "ASDM::InjectionEnable"

OBJ_X = [
    f"ASDM::Obj{i:02d}_X"
    for i in range(1, 19)
]

OBJ_Y = [
    f"ASDM::Obj{i:02d}_Y"
    for i in range(1, 19)
]

OBJ_TYPE = [
    f"ASDM::Obj{i:02d}_Type"
    for i in range(1, 19)
]

# -------------------------------------------------------
# Lane A
# -------------------------------------------------------

LANE_A_A = "ASDM::LaneA_a"
LANE_A_B = "ASDM::LaneA_b"
LANE_A_C = "ASDM::LaneA_c"
LANE_A_D1 = "ASDM::LaneA_d1"
LANE_A_D2 = "ASDM::LaneA_d2"
LANE_A_POSITION = "ASDM::LaneA_Position"


# -------------------------------------------------------
# Lane B
# -------------------------------------------------------

LANE_B_A = "ASDM::LaneB_a"
LANE_B_B = "ASDM::LaneB_b"
LANE_B_C = "ASDM::LaneB_c"
LANE_B_D1 = "ASDM::LaneB_d1"
LANE_B_D2 = "ASDM::LaneB_d2"
LANE_B_POSITION = "ASDM::LaneB_Position"


# -------------------------------------------------------
# Lane C
# -------------------------------------------------------

LANE_C_A = "ASDM::LaneC_a"
LANE_C_B = "ASDM::LaneC_b"
LANE_C_C = "ASDM::LaneC_c"
LANE_C_D1 = "ASDM::LaneC_d1"
LANE_C_D2 = "ASDM::LaneC_d2"
LANE_C_POSITION = "ASDM::LaneC_Position"


# -------------------------------------------------------
# Lane D
# -------------------------------------------------------

LANE_D_A = "ASDM::LaneD_a"
LANE_D_B = "ASDM::LaneD_b"
LANE_D_C = "ASDM::LaneD_c"
LANE_D_D1 = "ASDM::LaneD_d1"
LANE_D_D2 = "ASDM::LaneD_d2"
LANE_D_POSITION = "ASDM::LaneD_Position"

LANE_A = [
    LANE_A_A,
    LANE_A_B,
    LANE_A_C,
    LANE_A_D1,
    LANE_A_D2,
    LANE_A_POSITION,
]

LANE_B = [
    LANE_B_A,
    LANE_B_B,
    LANE_B_C,
    LANE_B_D1,
    LANE_B_D2,
    LANE_B_POSITION,
]

LANE_C = [
    LANE_C_A,
    LANE_C_B,
    LANE_C_C,
    LANE_C_D1,
    LANE_C_D2,
    LANE_C_POSITION,
]

LANE_D = [
    LANE_D_A,
    LANE_D_B,
    LANE_D_C,
    LANE_D_D1,
    LANE_D_D2,
    LANE_D_POSITION,
]

LANES = [
    LANE_A,
    LANE_B,
    LANE_C,
    LANE_D,
]