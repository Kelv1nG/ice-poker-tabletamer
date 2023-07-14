import sys

from overlay import Overlay
from PyQt6.QtWidgets import QApplication


class OverlayManager:
    def __init__(self):
        ...

    def create_overlay(self):
        overlay = Overlay()
        overlay.show()
