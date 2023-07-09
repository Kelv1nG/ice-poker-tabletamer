import sys

from PyQt6.QtWidgets import QApplication

from widgets.main.main import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    app.exec()
