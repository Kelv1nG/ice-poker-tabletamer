import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LayoutDirection.LeftToRight,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                QtCore.QSize(220, 32),
                screen_geometry,
            )
        )

    def mousePressEvent(self, event):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    app.exec()
