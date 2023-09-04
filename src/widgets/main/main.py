from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from . import layout_setup, main_setup, table_setup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = "assets/main_window.ui"
        self.ui = uic.loadUi(ui_file_path, self)
        self.setWindowTitle("CurbYourTables")

        # init methods
        table_setup.load_settings(self.ui)
        layout_setup.load_settings(self.ui)
        main_setup.hide_labels_on_stop(self.ui)

        self._worker = None
        self._thread = None

        self.connect_buttons()
        self.show()

    def connect_buttons(self):
        def setup_table():
            self.ui.table_setup_search.clicked.connect(
                lambda: table_setup.search_table(self.ui)
            )
            self.ui.table_setup_save.clicked.connect(
                lambda: table_setup.save_settings(self.ui)
            )

        def visualize_grid():
            self.ui.visualize_grid.clicked.connect(layout_setup.show_layout)

        def add_reduce_tables():
            self.ui.add_table_count.clicked.connect(
                lambda: layout_setup.add_table_count(self.ui)
            )
            self.ui.reduce_table_count.clicked.connect(
                lambda: layout_setup.reduce_table_count(self.ui)
            )

        def connect_application_start():
            self.ui.start_button.clicked.connect(
                lambda: main_setup.on_start(self, self.ui)
            )

        setup_table()
        visualize_grid()
        add_reduce_tables()
        connect_application_start()
