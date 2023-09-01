from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget


class TableTemplate(QWidget):
    def __init__(
        self,
        left: int,
        top: int,
        table_width: int,
        table_height: int,
        number_label: int,
    ):
        super().__init__()
        self.number_label = number_label
        self.setGeometry(left, top, table_width, table_height)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.setWindowTitle(
            "CurbYourTables Slot #{number}".format(number=str(self.number_label))
        )
        self.init_ui()

    def minimumSizeHint(self):
        return self.size()

    def maximumSizeHint(self):
        return self.size()

    def resizeEvent(self, event):
        self.setFixedSize(self.geometry().size())

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        layout = QVBoxLayout()

        # Add the number label
        number_label = QLabel(str(self.number_label))
        font = QFont()
        font.setPointSize(20)
        number_label.setFont(font)
        layout.addWidget(number_label, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        main_layout.addLayout(layout)

        # Set layout
        self.setLayout(main_layout)
