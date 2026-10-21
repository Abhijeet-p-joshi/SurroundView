from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SurroundView")
        self.resize(1200, 800)

        self._create_ui()

    def _create_ui(self):
        central_widget = QWidget()

        layout = QVBoxLayout()

        label = QLabel("SurroundView")
        layout.addWidget(label)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.statusBar().showMessage("Ready")