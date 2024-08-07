from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)

from services.layout.layout_manager import table_layout_manager
from widgets.utils.popup import PopupMessage

from .table_template import TableTemplate


class MainTableTemplate(TableTemplate):
    def __init__(
        self,
        left: int,
        top: int,
        table_width: int,
        table_height: int,
        number_label: int,
    ):
        super().__init__(
            left=left,
            top=top,
            table_width=table_width,
            table_height=table_height,
            number_label=number_label,
        )
        self.init_ui()

    def connect_buttons(self):
        self.save_button.clicked.connect(self.save)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        layout = QVBoxLayout()

        # Add the number label
        number_label = QLabel(str(self.number_label))
        font = QFont()
        font.setPointSize(20)
        number_label.setFont(font)
        layout.addWidget(number_label, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        # Add a spacer item to center-align the label
        spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout.addItem(spacer)

        # Add wrapped text label
        text_label = QLabel(
            "This is what your grid looks like.\nYou can arrange the slots if you wish,\n"
            "Simply drag them wherever you want.\nClick Save when finished"
        )
        text_label.setWordWrap(True)
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label)

        # Add Save button
        self.save_button = QPushButton("save")
        layout.addWidget(self.save_button)

        main_layout.addLayout(layout)

        # Set layout
        self.setLayout(main_layout)

        self.connect_buttons()

    def save(self):
        table_layout_manager.save_table_configuration()
        PopupMessage(
            title="Layout Saved",
            message="Successfully Saved TableLayouts",
            icon=QMessageBox.Icon.Information,
        )
