import sys

from overlay import Overlay
from PyQt6.QtWidgets import QApplication


class OverlayManager:
    def __init__(self):
        ...

    def create_overlay(self):
        overlay = Overlay()
        overlay.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay_manager = OverlayManager()
    overlay_manager.create_overlay()
    app.exec()
