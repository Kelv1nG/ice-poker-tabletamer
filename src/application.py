import sys

from PyQt6.QtWidgets import QApplication

from widgets.main.main import MainWindow

import logging

logger = logging.getLogger('unhandled_exceptions_logger')
logger.setLevel(logging.ERROR)

log_file = 'log.txt'
file_handler = logging.FileHandler(log_file)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def log_unhandled_exception(exc_type, exc_value, exc_traceback):
    logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

if __name__ == "__main__":
    sys.excepthook = log_unhandled_exception
    app = QApplication(sys.argv)
    main_window = MainWindow()
    app.exec()
    sys.exit(app.exec())
