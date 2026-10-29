from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)

from gui.lane_group import LaneGroup
from injection.scenario_io import ScenarioIO

class LaneEditor(QWidget):

    apply_clicked = Signal(list)

    def __init__(self):

        super().__init__()
        self.scenario_io = ScenarioIO()
        layout = QVBoxLayout(self)

        self.laneA = LaneGroup("Lane A")
        self.laneB = LaneGroup("Lane B")
        self.laneC = LaneGroup("Lane C")
        self.laneD = LaneGroup("Lane D")

        layout.addWidget(self.laneA)
        layout.addWidget(self.laneB)
        layout.addWidget(self.laneC)
        layout.addWidget(self.laneD)

        # Button
        self.applyButton = QPushButton("Apply Lanes")
        self.applyButton.setFixedWidth(100)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.applyButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

        self.applyButton.clicked.connect(
            lambda: (
                print("Apply button clicked"),
                print(self.lanes()),
                self.apply_clicked.emit(
                    self.lanes()
                )
            )
        )
        self.set_lanes(
            self.scenario_io.load_lanes()
        )

    def lanes(self):
        return [
            self.laneA.lane("A"),
            self.laneB.lane("B"),
            self.laneC.lane("C"),
            self.laneD.lane("D"),
        ]

    def set_lanes(self, lanes):
        if lanes is None:
            return
        if len(lanes) != 4:
            return
        self.laneA.set_lane(lanes[0])
        self.laneB.set_lane(lanes[1])
        self.laneC.set_lane(lanes[2])
        self.laneD.set_lane(lanes[3])