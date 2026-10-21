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


class ControlPanel(QWidget):

    apply_clicked = Signal(list)

    def __init__(self):
        super().__init__()

        self._create_ui()

    def _create_ui(self):

        main_layout = QVBoxLayout(self)

        self.car_x = self._create_x_spinbox()
        self.car_y = self._create_y_spinbox()

        self.bike_x = self._create_x_spinbox()
        self.bike_y = self._create_y_spinbox()

        self.truck_x = self._create_x_spinbox()
        self.truck_y = self._create_y_spinbox()

        main_layout.addWidget(
            self._create_group(
                "Car",
                self.car_x,
                self.car_y
            )
        )

        main_layout.addWidget(
            self._create_group(
                "Bike",
                self.bike_x,
                self.bike_y
            )
        )

        main_layout.addWidget(
            self._create_group(
                "Truck",
                self.truck_x,
                self.truck_y
            )
        )

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

        objects = [

            DetectedObject(
                ObjectType.CAR,
                self.car_x.value(),
                self.car_y.value()
            ),

            DetectedObject(
                ObjectType.BIKE,
                self.bike_x.value(),
                self.bike_y.value()
            ),

            DetectedObject(
                ObjectType.TRUCK,
                self.truck_x.value(),
                self.truck_y.value()
            )

        ]

        self.apply_clicked.emit(objects)