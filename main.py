import sys

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from gui.main_window import MainWindow

from canoe.canoe_interface import CANoeInterface

def main():

    app = QApplication(sys.argv)

    canoe = CANoeInterface()

    if not canoe.is_measurement_running():

        QMessageBox.warning(
            None,
            "CANoe Measurement not running",
            "Please:\n"
            "1. Open your CANoe.\n"
            "2. Start Measurement (F9).\n"
            "3. Launch the application again."
        )

        sys.exit(0)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()