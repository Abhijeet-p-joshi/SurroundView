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
    QFileDialog,
    QMessageBox,
    QFrame,
    QHeaderView,
)

import csv

from injection.scenario import Scenario
from models import DetectedObject, ObjectType


class InjectTab(QWidget):

    scenarioApplied = Signal(Scenario)

    startInjectionRequested = Signal()

    stopInjectionRequested = Signal()

    OBJECT_COUNT = 18

    def __init__(self):

        super().__init__()

        self.injection_running = False

        self._create_ui()

        self._populate_table()

    # ----------------------------------------------------------

    def _create_ui(self):

        layout = QVBoxLayout(self)

        #
        # Title
        #

        title = QLabel("Scenario")

        title.setStyleSheet(
            "font-size:16px;font-weight:bold;"
        )

        layout.addWidget(title)

        #
        # Table
        #

        self.table = QTableWidget(
            self.OBJECT_COUNT,
            5,
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Enable",
                "Type",
                "X (cm)",
                "Y (cm)",
                "Slot",
            ]
        )

        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch,
        )

        layout.addWidget(self.table)

        #
        # Buttons
        #

        button_layout = QHBoxLayout()

        self.load_button = QPushButton("Load CSV")

        self.apply_button = QPushButton("Apply Scenario")

        button_layout.addWidget(self.load_button)

        button_layout.addStretch()

        button_layout.addWidget(self.apply_button)

        layout.addLayout(button_layout)

        #
        # Status Frame
        #

        frame = QFrame()

        frame.setFrameShape(QFrame.StyledPanel)

        status_layout = QVBoxLayout(frame)

        status_title = QLabel("Injection")

        status_title.setStyleSheet(
            "font-size:15px;font-weight:bold;"
        )

        status_layout.addWidget(status_title)

        self.status_label = QLabel("⚪ Stopped")

        self.scenario_label = QLabel(
            "Scenario : None"
        )

        self.object_label = QLabel(
            "Objects : 0"
        )

        status_layout.addWidget(self.status_label)

        status_layout.addWidget(self.scenario_label)

        status_layout.addWidget(self.object_label)

        self.toggle_button = QPushButton(
            "Start Injection"
        )

        self.toggle_button.setMinimumHeight(40)

        status_layout.addWidget(
            self.toggle_button
        )

        layout.addWidget(frame)

        #
        # Connections
        #

        self.load_button.clicked.connect(
            self.load_csv
        )

        self.apply_button.clicked.connect(
            self.apply_scenario
        )

        self.toggle_button.clicked.connect(
            self.toggle_injection
        )

    # ----------------------------------------------------------

    def _populate_table(self):

        for row in range(self.OBJECT_COUNT):

            enable = QCheckBox()

            self.table.setCellWidget(
                row,
                0,
                enable,
            )

            combo = QComboBox()

            combo.addItems(
                [
                    "Car",
                    "Truck",
                    "Bike",
                ]
            )

            self.table.setCellWidget(
                row,
                1,
                combo,
            )

            x = QDoubleSpinBox()

            x.setRange(
                0,
                13000,
            )

            x.setDecimals(1)

            self.table.setCellWidget(
                row,
                2,
                x,
            )

            y = QDoubleSpinBox()

            y.setRange(
                -1000,
                1000,
            )

            y.setDecimals(1)

            self.table.setCellWidget(
                row,
                3,
                y,
            )

            slot = QTableWidgetItem(
                str(row + 1)
            )

            slot.setFlags(
                Qt.ItemIsEnabled
            )

            slot.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                4,
                slot,
            )

    # ----------------------------------------------------------

    def apply_scenario(self):

        scenario = Scenario()

        scenario.name = "Manual Scenario"

        mapping = {
            "Car": ObjectType.CAR,
            "Truck": ObjectType.TRUCK,
            "Bike": ObjectType.BIKE,
        }

        for row in range(self.OBJECT_COUNT):

            enabled = self.table.cellWidget(
                row,
                0,
            ).isChecked()

            if not enabled:
                continue

            obj = DetectedObject(

                slot=row + 1,

                object_type=mapping[
                    self.table.cellWidget(
                        row,
                        1,
                    ).currentText()
                ],

                x=self.table.cellWidget(
                    row,
                    2,
                ).value(),

                y=self.table.cellWidget(
                    row,
                    3,
                ).value(),

            )

            scenario.add_object(obj)

        self.scenario_label.setText(
            f"Scenario : {scenario.name}"
        )

        self.object_label.setText(
            f"Objects : {scenario.object_count()}"
        )

        self.scenarioApplied.emit(
            scenario
        )

    # ----------------------------------------------------------

    def load_csv(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Scenario",
            "",
            "CSV (*.csv)",
        )

        if not filename:
            return

        try:

            with open(
                filename,
                newline="",
            ) as file:

                reader = csv.DictReader(file)

                for row, csv_row in enumerate(reader):

                    if row >= self.OBJECT_COUNT:
                        break

                    self.table.cellWidget(
                        row,
                        0,
                    ).setChecked(
                        csv_row["Enable"] in ["1", "True", "true"]
                    )

                    self.table.cellWidget(
                        row,
                        1,
                    ).setCurrentText(
                        csv_row["Type"]
                    )

                    self.table.cellWidget(
                        row,
                        2,
                    ).setValue(
                        float(csv_row["X"])
                    )

                    self.table.cellWidget(
                        row,
                        3,
                    ).setValue(
                        float(csv_row["Y"])
                    )

        except Exception as e:

            QMessageBox.critical(
                self,
                "CSV Error",
                str(e),
            )

    # ----------------------------------------------------------

    def toggle_injection(self):

        if self.injection_running:

            self.stopInjectionRequested.emit()

        else:

            self.startInjectionRequested.emit()

    # ----------------------------------------------------------

    def injection_started(self):

        self.injection_running = True

        self.status_label.setText(
            "🟢 Running"
        )

        self.toggle_button.setText(
            "Stop Injection"
        )

    # ----------------------------------------------------------

    def injection_stopped(self):

        self.injection_running = False

        self.status_label.setText(
            "⚪ Stopped"
        )

        self.toggle_button.setText(
            "Start Injection"
        )