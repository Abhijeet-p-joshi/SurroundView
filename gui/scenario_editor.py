from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QDoubleSpinBox,
    QCheckBox,
    QHeaderView,
    QMessageBox,
)

from models import DetectedObject, ObjectType
from injection.scenario import Scenario

class ScenarioEditor(QWidget):
    """
    Scenario editor used in Injection mode.

    - Displays 18 configurable objects.
    - Allows enabling/disabling each object.
    - Allows importing a CSV scenario.
    - Emits Apply Scenario when requested.
    """

    scenarioApplied = Signal(Scenario)
    csvLoaded = Signal(str)

    OBJECT_COUNT = 18

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumWidth(470)

        self._create_ui()
        self._populate_default_rows()

    # ==========================================================
    # UI
    # ==========================================================

    def _create_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Scenario Editor")
        title.setStyleSheet(
            "font-size:16px;"
            "font-weight:bold;"
        )

        layout.addWidget(title)

        self.table = QTableWidget(
            self.OBJECT_COUNT,
            5
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Enable",
                "Object Type",
                "X (cm)",
                "Y (cm)",
                "Slot",
            ]
        )

        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()

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
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.load_csv_button = QPushButton(
            "Load CSV"
        )

        self.apply_button = QPushButton(
            "Apply Scenario"
        )

        button_layout.addWidget(
            self.load_csv_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.apply_button
        )

        layout.addLayout(button_layout)

        self.load_csv_button.clicked.connect(
            self.load_csv
        )

        self.apply_button.clicked.connect(
            self.apply_scenario
        )

    # ==========================================================
    # Default Table
    # ==========================================================

    def _populate_default_rows(self):

        for row in range(self.OBJECT_COUNT):

            # Enable

            enabled = QCheckBox()
            enabled.setChecked(False)

            self.table.setCellWidget(
                row,
                0,
                enabled
            )

            # Type

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
                combo
            )

            # X

            x = QDoubleSpinBox()

            x.setRange(0, 13000)

            x.setDecimals(1)

            x.setSuffix(" cm")

            x.setValue(0)

            self.table.setCellWidget(
                row,
                2,
                x
            )

            # Y

            y = QDoubleSpinBox()

            y.setRange(-1000, 1000)

            y.setDecimals(1)

            y.setSuffix(" cm")

            y.setValue(0)

            self.table.setCellWidget(
                row,
                3,
                y
            )

            # Slot

            slot_item = QTableWidgetItem(
                str(row + 1)
            )

            slot_item.setFlags(
                Qt.ItemIsEnabled
            )

            slot_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                4,
                slot_item
            )

    # ==========================================================
    # CSV
    # ==========================================================

    def load_csv(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Scenario",
            "",
            "CSV (*.csv)"
        )

        if not filename:
            return

        try:

            import csv

            with open(
                filename,
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row, csv_row in enumerate(reader):

                    if row >= self.OBJECT_COUNT:
                        break

                    enable = self.table.cellWidget(row, 0)
                    obj = self.table.cellWidget(row, 1)
                    x = self.table.cellWidget(row, 2)
                    y = self.table.cellWidget(row, 3)

                    enable.setChecked(
                        csv_row.get(
                            "Enable",
                            "1"
                        )
                        in ["1", "True", "true"]
                    )

                    obj.setCurrentText(
                        csv_row.get(
                            "Type",
                            "Car"
                        )
                    )

                    x.setValue(
                        float(
                            csv_row.get(
                                "X",
                                0
                            )
                        )
                    )

                    y.setValue(
                        float(
                            csv_row.get(
                                "Y",
                                0
                            )
                        )
                    )

            self.csvLoaded.emit(filename)

        except Exception as e:

            QMessageBox.critical(
                self,
                "CSV Error",
                str(e)
            )

    # ==========================================================
    # Scenario
    # ==========================================================

    def apply_scenario(self):

        scenario = Scenario(
            name="Manual Scenario"
        )

        type_map = {
            "Car": ObjectType.CAR,
            "Truck": ObjectType.TRUCK,
            "Bike": ObjectType.BIKE,
        }

        for row in range(self.OBJECT_COUNT):

            enabled = self.table.cellWidget(
                row,
                0
            ).isChecked()

            if not enabled:
                continue

            obj_type = self.table.cellWidget(
                row,
                1
            ).currentText()

            x = self.table.cellWidget(
                row,
                2
            ).value()

            y = self.table.cellWidget(
                row,
                3
            ).value()

            scenario.add_object(

                DetectedObject(

                    slot=row + 1,

                    object_type=type_map[obj_type],

                    x=x,

                    y=y,

                )

            )

        if not scenario.is_valid():

            QMessageBox.warning(
                self,
                "Invalid Scenario",
                "Scenario validation failed."
            )

            return

        self.scenarioApplied.emit(scenario)