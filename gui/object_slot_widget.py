from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGroupBox,
    QGridLayout,
    QDoubleSpinBox,
    QComboBox,
)

from config.constants import X_MIN, X_MAX, Y_MIN, Y_MAX
from models import ObjectType


class ObjectSlotWidget(QGroupBox):

    def __init__(self, slot_number: int):
        super().__init__(f"Object Slot {slot_number}")

        self.slot_number = slot_number

        layout = QGridLayout(self)

        self.type_combo = QComboBox()

        for object_type in ObjectType:
            self.type_combo.addItem(
                object_type.display_name,
                object_type
            )

        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(X_MIN, X_MAX)
        self.x_spin.setDecimals(1)
        self.x_spin.setSingleStep(10)

        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(Y_MIN, Y_MAX)
        self.y_spin.setDecimals(1)
        self.y_spin.setSingleStep(5)

        layout.addWidget(QLabel("Type"), 0, 0)
        layout.addWidget(self.type_combo, 0, 1)

        layout.addWidget(QLabel("X (cm)"), 1, 0)
        layout.addWidget(self.x_spin, 1, 1)

        layout.addWidget(QLabel("Y (cm)"), 2, 0)
        layout.addWidget(self.y_spin, 2, 1)