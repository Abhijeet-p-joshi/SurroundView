from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QDoubleSpinBox
)

from models import DetectedObject, ObjectType
from config.constants import X_MIN, X_MAX, Y_MIN, Y_MAX
from gui.object_slot_widget import ObjectSlotWidget


class ControlPanel(QWidget):

    apply_clicked = Signal(list)

    def __init__(self):
        super().__init__()
        self.object_slots = []
        self._create_ui()

    def _create_ui(self):

        main_layout = QVBoxLayout(self)

        for slot in range(1, 4):

            widget = ObjectSlotWidget(slot)

            self.object_slots.append(widget)

            main_layout.addWidget(widget)

        # Buttons
        self.apply_button = QPushButton("Apply")
        self.reset_button = QPushButton("Reset")

        self.apply_button.clicked.connect(self.apply)

        main_layout.addWidget(self.apply_button)
        main_layout.addWidget(self.reset_button)

        main_layout.addStretch()

    def _create_group(self, title, x_box, y_box):

        group = QGroupBox(title)

        layout = QGridLayout()

        layout.addWidget(QLabel("X"), 0, 0)
        layout.addWidget(x_box, 0, 1)

        layout.addWidget(QLabel("Y"), 1, 0)
        layout.addWidget(y_box, 1, 1)

        group.setLayout(layout)

        return group

    def _create_x_spinbox(self):

        spin = QDoubleSpinBox()

        spin.setRange(X_MIN, X_MAX)
        spin.setDecimals(1)
        spin.setSingleStep(10)

        return spin

    def _create_y_spinbox(self):

        spin = QDoubleSpinBox()

        spin.setRange(Y_MIN, Y_MAX)
        spin.setDecimals(1)
        spin.setSingleStep(5)

        return spin

    def apply(self):

        objects = []

        for widget in self.object_slots:

            objects.append(

                DetectedObject(

                    slot=widget.slot_number,

                    object_type=widget.type_combo.currentData(),

                    x=widget.x_spin.value(),

                    y=widget.y_spin.value()

                )

            )

        self.apply_clicked.emit(objects)