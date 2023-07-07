import sys

from PyQt6.QtWidgets import QApplication
from overlay import Overlay


class OverlayManager:
    def __init__(self):
        ...

    def create_overlay(self):
        app = QApplication.instance()
        overlay = Overlay(None)
        overlay.showNormal()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay_manager = OverlayManager()
    overlay_manager.create_overlay()
    app.exec()
