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

    @property
    def window_center_coordinates(self) -> tuple[int, int]:
        if self.window:
            return (self.window.centery, self.window.centerx)
        return (0, 0)

    @property
    def slot_center_coordinates(self) -> tuple[int, int]:
        return (self.top - self.height / 2, self.left + self.width / 2)


    @property
    def is_center_outside_slot_boundary(self):
        if self.window:
            outside_x_boundary =  self.window.centerx < self.left or self.window.centerx > (self.left + self.width)
            outside_y_boundary = self.window.centery < self.top or self.window.centery > (self.top + self.height)
            return (outside_x_boundary or outside_y_boundary)
        return False
