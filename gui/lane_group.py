from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QHBoxLayout,
)

from models.lane import LanePosition, Lane


class LaneGroup(QGroupBox):

    def __init__(self, title):

        super().__init__(title)
        layout = QGridLayout(self)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)

        layout.setContentsMargins(10, 12, 10, 12)

        self.position = QComboBox()
        self.position.addItem(
            "Closest Left",
            LanePosition.CLOSEST_LEFT
        )
        self.position.addItem(
            "Second Closest Left",
            LanePosition.SECOND_CLOSEST_LEFT
        )
        self.position.addItem(
            "Closest Right",
            LanePosition.CLOSEST_RIGHT
        )
        self.position.addItem(
            "Second Closest Right",
            LanePosition.SECOND_CLOSEST_RIGHT
        )
        self.a = QDoubleSpinBox()
        self.b = QDoubleSpinBox()
        self.c = QDoubleSpinBox()
        self.d1 = QDoubleSpinBox()
        self.d2 = QDoubleSpinBox()

        spins = [
            self.a,
            self.b,
            self.c,
            self.d1,
            self.d2,
        ]

        for spin in spins:
            spin.setDecimals(6)
            spin.setRange(
                -1000,
                1000,
            )
            spin.setSingleStep(0.01)

        for spin in spins:
            spin.setFixedWidth(80)

        self.position.setFixedWidth(100)



        layout.addWidget(QLabel("Position"), 0, 0)
        layout.addWidget(self.position,       0, 1)

        layout.addWidget(QLabel("a"), 1, 0)
        layout.addWidget(self.a,      1, 1)

        layout.addWidget(QLabel("b"), 1, 2)
        layout.addWidget(self.b,      1, 3)

        layout.addWidget(QLabel("c"), 1, 4)
        layout.addWidget(self.c,      1, 5)

        layout.addWidget(QLabel("d1"), 1, 6)
        layout.addWidget(self.d1,      1, 7)

        layout.addWidget(QLabel("d2"), 1, 8)
        layout.addWidget(self.d2,      1, 9)

        # Label columns
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(2, 0)
        layout.setColumnStretch(4, 0)
        layout.setColumnStretch(6, 0)
        layout.setColumnStretch(8, 0)

        # Spinbox columns
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(3, 0)
        layout.setColumnStretch(5, 0)
        layout.setColumnStretch(7, 0)
        layout.setColumnStretch(9, 0)

        # Let any remaining space stay at the end
        layout.setColumnStretch(10, 1)

    def lane(self, name):
        return Lane(
            name=name,
            position=self.position.currentData(),
            a=self.a.value(),
            b=self.b.value(),
            c=self.c.value(),
            d1=self.d1.value(),
            d2=self.d2.value(),
        )