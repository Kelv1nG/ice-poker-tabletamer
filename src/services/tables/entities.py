import enum
from dataclasses import dataclass

import pygetwindow as gw


class AppName(enum.Enum):
    FIREFOX = "Mozilla Firefox"
    CHROME = "Google Chrome"


@dataclass
class Slot:
    """
    Represents a slot with its properties

    Attributes:
        top (int): Vertical position of the slot's top edge (in pixels).
        left (int): Horizontal position of the slot's left edge (in pixels).
        window (Optional[gw.Window]): Associated window object (if allocated).
    """

    top: int
    left: int
    height: int
    width: int
    window: gw.Window | None = None

    def move_to_assigned_slot(self):
        if self.window:
            self.window.moveTo(self.left, self.top)

    def resize_window(self):
        if self.window:
            self.window.width = self.width
            self.window.height = self.height
