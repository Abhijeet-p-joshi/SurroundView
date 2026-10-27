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