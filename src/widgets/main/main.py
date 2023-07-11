from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from . import table_setup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = "assets/main_window.ui"
        self.ui = uic.loadUi(ui_file_path, self)
        self.setWindowTitle("CurbYourTables")

        # init methods
        table_setup.load_settings(self.ui)
        self.connect_buttons()
        self.show()

    def connect_buttons(self):
        def setup_table():
            self.ui.table_setup_search.clicked.connect(
                lambda: table_setup.search_table(self.ui)
            )
            self.ui.table_setup_save.clicked.connect(table_setup.save_settings)

        setup_table()
