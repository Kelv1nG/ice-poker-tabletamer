from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from . import layout_setup_methods, main_methods, table_setup_methods, hotkeys_setup_methods


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = "assets/main_window.ui"
        self.ui = uic.loadUi(ui_file_path, self)
        self.setWindowTitle("CurbYourTables")

        # init methods
        table_setup_methods.load_settings(self.ui)
        layout_setup_methods.load_settings(self.ui)
        main_methods.hide_labels_on_stop(self.ui)
        hotkeys_setup_methods.load_settings(self.ui)

        self._worker = None
        self._thread = None

        self.connect_buttons()
        self.show()

    def connect_buttons(self):
        def setup_table():
            self.ui.table_setup_search.clicked.connect(
                lambda: table_setup_methods.search_table(self.ui)
            )
            self.ui.table_setup_save.clicked.connect(
                lambda: table_setup_methods.save_settings(self.ui)
            )
            self.ui.table_setup_grab_fold.clicked.connect(
                lambda: table_setup_methods.grab_fold(self, self.ui)
            )
            self.ui.table_setup_grab_check_call.clicked.connect(
                lambda: table_setup_methods.grab_check_call(self, self.ui)
            )
            self.ui.table_setup_grab_bet.clicked.connect(
                lambda: table_setup_methods.grab_bet(self, self.ui)
            )
            self.ui.table_setup_grab_raise.clicked.connect(
                lambda: table_setup_methods.grab_raise(self, self.ui)
            )
            self.ui.table_setup_grab_amount.clicked.connect(
                lambda: table_setup_methods.grab_amount(self, self.ui)
            )

        def setup_hotkeys():
            self.ui.hotkeys_save.clicked.connect(
                lambda: hotkeys_setup_methods.save_settings(self.ui)
            )

        def visualize_grid():
            self.ui.visualize_grid.clicked.connect(layout_setup_methods.show_layout)

        def add_reduce_tables():
            self.ui.add_table_count.clicked.connect(
                lambda: layout_setup_methods.add_table_count(self.ui)
            )
            self.ui.reduce_table_count.clicked.connect(
                lambda: layout_setup_methods.reduce_table_count(self.ui)
            )

        def connect_application_start():
            self.ui.start_button.clicked.connect(
                lambda: main_methods.on_start(self, self.ui)
            )

        setup_table()
        setup_hotkeys()
        visualize_grid()
        add_reduce_tables()
        connect_application_start()
