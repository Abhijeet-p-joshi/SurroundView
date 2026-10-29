from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QDoubleSpinBox,
    QCheckBox,
    QFrame,
    QHeaderView,
)

from injection.scenario import Scenario
from models import DetectedObject, ObjectType
from injection.scenario_io import ScenarioIO

class InjectTab(QWidget):

    scenarioApplied = Signal(Scenario)

    startInjectionRequested = Signal()

    stopInjectionRequested = Signal()

    OBJECT_COUNT = 18

    def __init__(self, parent=None):

        super().__init__(parent)

        self.injection_running = False

        self._create_ui()

        self._populate_table()

        self.load_default_scenario()

    # ----------------------------------------------------------

    def _create_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # =====================================================
        # Title
        # =====================================================

        title = QLabel("Injection Scenario")

        title.setStyleSheet(
            """
            font-size:16px;
            font-weight:bold;
            """
        )

        layout.addWidget(title)

        # =====================================================
        # Table
        # =====================================================

        self.table = QTableWidget(
            self.OBJECT_COUNT,
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "✓",
                "Type",
                "X (cm)",
                "Y (cm)"
            ]
        )

        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(20)

        header = self.table.horizontalHeader()

        header.setFixedHeight(26)

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        header.setStretchLastSection(True)

        layout.addWidget(
            self.table,
            stretch=1
        )

        # =====================================================
        # Buttons
        # =====================================================

        self.apply_button = QPushButton(
            "Apply Scenario"
        )

        self.toggle_button = QPushButton(
            "Start Injection"
        )

        self.apply_button.setMinimumHeight(36)
        self.toggle_button.setMinimumHeight(36)

        # Make buttons compact
        self.apply_button.setFixedWidth(140)
        self.toggle_button.setFixedWidth(140)

        button_layout = QHBoxLayout()

        button_layout.setSpacing(10)

        button_layout.addWidget(
            self.apply_button
        )

        button_layout.addWidget(
            self.toggle_button
        )

        # Push everything else to the right
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # =====================================================
        # Status
        # =====================================================

        self.status_label = QLabel(
            "⚪ Stopped"
        )

        self.scenario_label = QLabel(
            "Scenario : None"
        )

        self.object_label = QLabel(
            "Objects : 0"
        )

        layout.addWidget(self.status_label)
        layout.addWidget(self.scenario_label)
        layout.addWidget(self.object_label)

        # =====================================================
        # Connections
        # =====================================================

        self.apply_button.clicked.connect(
            self.apply_scenario
        )

        self.toggle_button.clicked.connect(
            self.toggle_injection
        )

    def _populate_table(self):

        for row in range(self.OBJECT_COUNT):

            # --------------------------------------------------
            # Enable
            # --------------------------------------------------

            enable = QCheckBox()

            enable.setChecked(False)

            self.table.setCellWidget(
                row,
                0,
                enable,
            )

            # --------------------------------------------------
            # Object Type
            # --------------------------------------------------

            combo = QComboBox()

            combo.addItems(
                [
                    "None",
                    "Car",
                    "Truck",
                    "Bike",
                ]
            )

            combo.setCurrentIndex(0)

            self.table.setCellWidget(
                row,
                1,
                combo,
            )

            # --------------------------------------------------
            # X Coordinate
            # --------------------------------------------------

            x = QDoubleSpinBox()

            x.setRange(0, 13000)

            x.setDecimals(1)

            x.setSingleStep(10)

            x.setAlignment(Qt.AlignCenter)

            x.setSuffix(" cm")

            self.table.setCellWidget(
                row,
                2,
                x,
            )

            # --------------------------------------------------
            # Y Coordinate
            # --------------------------------------------------

            y = QDoubleSpinBox()

            y.setRange(-1000, 1000)

            y.setDecimals(1)

            y.setSingleStep(10)

            y.setAlignment(Qt.AlignCenter)

            y.setSuffix(" cm")

            self.table.setCellWidget(
                row,
                3,
                y,
            )

    # ----------------------------------------------------------

    def current_scenario(self) -> Scenario:
        """
        Reads the current table contents and returns
        a Scenario object containing all enabled objects.
        """

        scenario = Scenario()
        scenario.name = "Default Scenario"

        type_mapping = {
            "Car": ObjectType.CAR,
            "Truck": ObjectType.TRUCK,
            "Bike": ObjectType.BIKE,
            "None": ObjectType.NONE,
        }

        for row in range(self.OBJECT_COUNT):

            enable_widget = self.table.cellWidget(row, 0)
            type_widget = self.table.cellWidget(row, 1)
            x_widget = self.table.cellWidget(row, 2)
            y_widget = self.table.cellWidget(row, 3)

            if not enable_widget.isChecked():
                continue

            detected_object = DetectedObject(
                slot=row + 1,
                object_type=type_mapping[type_widget.currentText()],
                x=x_widget.value(),
                y=y_widget.value(),
            )

            scenario.add_object(detected_object)

        return scenario

    def apply_scenario(self):
        """
        Applies the current table contents as the active scenario.
        """
        scenario = self.current_scenario()
        ScenarioIO.save(scenario)
        self.scenario_label.setText(
            f"Scenario : {scenario.name}"
        )
        self.object_label.setText(
            f"Objects : {scenario.object_count()}"
        )
        
        self.scenarioApplied.emit(scenario)

    # ----------------------------------------------------------

    def toggle_injection(self):
        """
        Starts or stops cyclic injection.
        """

        if self.injection_running:
            self.stopInjectionRequested.emit()
        else:
            self.startInjectionRequested.emit()

        # #
        # # Prevent accidental double-clicks.
        # #

        # self.toggle_button.setEnabled(False)

    # ----------------------------------------------------------

    def injection_started(self):
        """
        Updates the GUI after injection starts.
        """

        self.injection_running = True

        self.status_label.setText(
            "🟢 Running"
        )

        self.toggle_button.setText(
            "Stop Injection"
        )

    # ----------------------------------------------------------

    def injection_stopped(self):
        """
        Updates the GUI after injection stops.
        """
        self.injection_running = False
        self.status_label.setText(
            "⚪ Stopped"
        )
        self.toggle_button.setText(
            "Start Injection"
        )

    def load_default_scenario(self):
        """
        Loads the default scenario from default.json
        and populates the table.
        """

        scenario = ScenarioIO.load()

        reverse_mapping = {
            ObjectType.CAR: "Car",
            ObjectType.TRUCK: "Truck",
            ObjectType.BIKE: "Bike",
            ObjectType.NONE: "None",
        }

        # Clear all rows first
        for row in range(self.OBJECT_COUNT):

            self.table.cellWidget(row, 0).setChecked(False)

            self.table.cellWidget(row, 1).setCurrentIndex(0)

            self.table.cellWidget(row, 2).setValue(0.0)

            self.table.cellWidget(row, 3).setValue(0.0)

        # Load scenario objects
        for obj in scenario:

            if obj.slot < 1 or obj.slot > self.OBJECT_COUNT:
                continue

            row = obj.slot - 1

            self.table.cellWidget(row, 0).setChecked(True)

            self.table.cellWidget(row, 1).setCurrentText(
                reverse_mapping.get(
                    obj.object_type,
                    "Car"
                )
            )

            self.table.cellWidget(row, 2).setValue(obj.x)

            self.table.cellWidget(row, 3).setValue(obj.y)

        self.scenario_label.setText(
            f"Scenario : {scenario.name}"
        )

        self.object_label.setText(
            f"Objects : {scenario.object_count()}"
        )