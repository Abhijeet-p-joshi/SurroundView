import pyqtgraph as pg
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtWidgets import QGraphicsRectItem

from models import DetectedObject, ObjectType
from config.constants import (
    X_MIN, X_MAX, Y_MIN, Y_MAX,
    EGO_LENGTH, EGO_WIDTH)
from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtCore import QRectF
from PySide6.QtCore import Signal


class SurroundViewWidget(QWidget):

    objectMoved = Signal(int, float, float)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)

        self._setup_plot()

        self.labels = []

        self._draw_ego_vehicle()

        self.scatter = pg.ScatterPlotItem(size=12)
        legend = self.plot.addLegend()
        legend.addItem(self.scatter, "Detected Objects")

        self.plot.addItem(self.scatter)
        # self.scatter.sigClicked.connect(
        #     self.scatter_clicked
        # )

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

        self._create_legend()
        # self.object_map = {}
        # self.selected_object = None
        # self.selected_point = None

        # self.dragging = False

        # self.plot.scene().sigMouseMoved.connect(
        #     self.mouse_moved
        # )

        # self.plot.scene().sigMouseClicked.connect(
        #     self.mouse_clicked
        # )

    def _setup_plot(self):

        self.plot.setBackground("white")

        # Engineering grid
        self.plot.showGrid(x=True, y=True, alpha=0.25)

        self.plot.setLabel(
            "bottom",
            "Forward Distance (+X) [cm]"
        )

        self.plot.setLabel(
            "left",
            "Lateral Distance (+Y Left) [cm]"
        )

        self.plot.setXRange(X_MIN, X_MAX)
        self.plot.setYRange(Y_MIN, Y_MAX)
        x_axis = self.plot.getAxis("bottom")
        y_axis = self.plot.getAxis("left")

        major_x = []
        minor_x = []

        for x in range(0, 13001, 100):

            if x % 1000 == 0:
                major_x.append((x, str(x)))
            else:
                minor_x.append((x, ""))

        x_axis.setTicks([
            major_x,
            minor_x
        ])

        major_y = []
        minor_y = []

        major_y = []
        minor_y = []

        for y in range(-1000, 1001, 100):

            if y % 500 == 0:
                major_y.append((y, str(y)))
            else:
                minor_y.append((y, ""))

        y_axis.setTicks([
            major_y,
            minor_y
        ])

        # Disable automatic scaling
        self.plot.enableAutoRange(False)

        # Keep manual zooming enabled
        self.plot.setMouseEnabled(x=True, y=True)

    def update_objects(self, objects: list[DetectedObject]):

        symbol_map = {
            ObjectType.CAR: "s",
            ObjectType.BIKE: "t",
            ObjectType.TRUCK: "d",
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

        # Remove previous labels
        for label in self.labels:
            self.plot.removeItem(label)

        self.labels.clear()

        # Create labels
        for obj in objects:

            text = pg.TextItem(
                text=f"{obj.object_type.name.title()} ({obj.slot})",
                anchor=(0, 1)
            )

            text.setPos(
                obj.x + 80,
                obj.y + 15
            )

            self.plot.addItem(text)

            self.labels.append(text)

    def _draw_ego_vehicle(self):

        rect = QGraphicsRectItem(
            QRectF(
                -EGO_LENGTH / 2,
                -EGO_WIDTH / 2,
                EGO_LENGTH,
                EGO_WIDTH,
            )
        )

        rect.setPen(QPen(QColor("black"), 2))
        rect.setBrush(QBrush(QColor(210, 210, 210)))
        self.plot.addItem(rect)

        origin = pg.TextItem(
            text="Origin (0,0)",
            anchor=(0.5, 0)
        )

        origin.setPos(0, -140)

        self.plot.addItem(origin)

    def _create_legend(self):

        legend = pg.TextItem(
            html="""
            <div style="
                background-color:white;
                padding:6px;
                border:1px solid black;
                font-size:10pt;
            ">
            <b>Legend</b><br>
            ■ Car (Blue)<br>
            ▲ Bike (Green)<br>
            ◆ Truck (Red)<br><br>
            Origin = Ego Vehicle<br>
            +X = Forward<br>
            +Y = Left
            </div>
            """,
            anchor=(1, 0)
        )

        legend.setPos(X_MAX - 100, Y_MAX - 50)

        self.plot.addItem(legend)

        def scatter_clicked(self, scatter, points):

            if not points:
                return

            self.selected_point = points[0]

            self.selected_object = points[0].data()

            self.dragging = True

            print(f"Selected slot {self.selected_object.slot}")

        def mouse_moved(self, pos):

            if not self.dragging:
                return

            mouse_point = self.plot.plotItem.vb.mapSceneToView(pos)

            self.selected_object.x = mouse_point.x()
            self.selected_object.y = mouse_point.y()

            self.update_objects(
                list(self.object_map.values())
            )

        def mouse_clicked(self, event):

            if not self.dragging:
                return

            if event.button() == Qt.LeftButton:
                self.dragging = False
                self.objectMoved.emit(
                    self.selected_object.slot,
                    self.selected_object.x,
                    self.selected_object.y
                )
                print("Released")