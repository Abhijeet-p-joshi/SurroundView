from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)

from gui.lane_group import LaneGroup
from injection.scenario_io import ScenarioIO
from models.lane import LanePosition

class LaneEditor(QWidget):

    apply_clicked = Signal(list)

    def __init__(self):

        super().__init__()
        self.scenario_io = ScenarioIO()
        layout = QVBoxLayout(self)

        self.laneA = LaneGroup(
            "Lane A",
            LanePosition.SECOND_CLOSEST_LEFT,
        )

        self.laneB = LaneGroup(
            "Lane B",
            LanePosition.CLOSEST_LEFT,
        )

        self.laneC = LaneGroup(
            "Lane C",
            LanePosition.CLOSEST_RIGHT,
        )

        self.laneD = LaneGroup(
            "Lane D",
            LanePosition.SECOND_CLOSEST_RIGHT,
        )

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
        lanes = self.scenario_io.load_lanes()

        self.set_lanes(lanes)

    def lanes(self):
        return [
            self.laneA.lane("A"),
            self.laneB.lane("B"),
            self.laneC.lane("C"),
            self.laneD.lane("D"),
        ]

    def set_lanes(self, lanes):

        # print("LaneEditor.set_lanes()")
        # print(lanes)

        if lanes is None:
            return
        if len(lanes) != 4:
            return

        # print("Setting Lane A")
        # self.laneA.set_lane(lanes[0])

        # print("Setting Lane B")
        # self.laneB.set_lane(lanes[1])

        # print("Setting Lane C")
        # self.laneC.set_lane(lanes[2])

        # print("Setting Lane D")
        # self.laneD.set_lane(lanes[3])