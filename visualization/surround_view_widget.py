import pyqtgraph as pg
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtWidgets import QGraphicsRectItem

from models import DetectedObject, ObjectType
from config.constants import X_MIN, X_MAX, Y_MIN, Y_MAX


class SurroundViewWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)

        self._setup_plot()

        self.scatter = pg.ScatterPlotItem(size=12)

        self.plot.addItem(self.scatter)

        self.update_objects([
            DetectedObject(
                slot=1,
                object_type=ObjectType.CAR,
                x=4000,
                y=120
            ),
            DetectedObject(
                slot=2,
                object_type=ObjectType.BIKE,
                x=1800,
                y=-80
            ),
            DetectedObject(
                slot=3,
                object_type=ObjectType.TRUCK,
                x=9500,
                y=250
            )
        ])

    def _setup_plot(self):

        self.plot.setBackground("w")

        self.plot.showGrid(x=True, y=True)

        self.plot.setLabel("left", "Y (cm)")
        self.plot.setLabel("bottom", "X (cm)")

        self.plot.setXRange(X_MIN, X_MAX)
        self.plot.setYRange(Y_MIN, Y_MAX)

    def update_objects(self, objects: list[DetectedObject]):

        symbol_map = {
            ObjectType.CAR: "s",      # Square
            ObjectType.BIKE: "t",     # Triangle
            ObjectType.TRUCK: "d",    # Diamond
        }

        color_map = {
            ObjectType.CAR: "b",
            ObjectType.BIKE: "g",
            ObjectType.TRUCK: "r",
        }

        spots = []

        for obj in objects:

            spots.append(
                {
                    "pos": (obj.x, obj.y),
                    "symbol": symbol_map[obj.object_type],
                    "brush": pg.mkBrush(color_map[obj.object_type]),
                    "pen": pg.mkPen("k"),
                    "size": 14,
                }
            )

        self.scatter.setData(spots)