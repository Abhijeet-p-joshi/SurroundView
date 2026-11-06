from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QLabel,
)

from models.lane import LanePosition, Lane, DISPLAY_NAMES


class LaneGroup(QGroupBox):

    def __init__(self, title, position: LanePosition):

        super().__init__(title)
        layout = QGridLayout(self)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)

        layout.setContentsMargins(10, 12, 10, 12)

        self.fixed_position = position
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
            spin.setRange(-1000,1000)
            spin.setSingleStep(0.01)
            spin.setMinimumWidth(150)

        layout.addWidget(QLabel("Position"),0,0,)
        layout.addWidget(QLabel(DISPLAY_NAMES[position]),0,1,)

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
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(5, 1)
        layout.setColumnStretch(7, 1)
        layout.setColumnStretch(9, 1)

        # Let any remaining space stay at the end
        layout.setColumnStretch(10, 1)

    def lane(self, name):
        return Lane(
            name=name,
            position=self.fixed_position,
            a=self.a.value(),
            b=self.b.value(),
            c=self.c.value(),
            d1=self.d1.value(),
            d2=self.d2.value(),
        )

    def set_lane(self, lane):

        print(f"Updating GUI for {lane.name}")

        self.a.setValue(lane.a)
        self.b.setValue(lane.b)
        self.c.setValue(lane.c)
        self.d1.setValue(lane.d1)
        self.d2.setValue(lane.d2)