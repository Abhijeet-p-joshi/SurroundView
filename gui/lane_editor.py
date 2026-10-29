from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)

from gui.lane_group import LaneGroup


class LaneEditor(QWidget):

    apply_clicked = Signal(list)

    def __init__(self):

        super().__init__()

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

    def lanes(self):
        return [
            self.laneA.lane("A"),
            self.laneB.lane("B"),
            self.laneC.lane("C"),
            self.laneD.lane("D"),
        ]