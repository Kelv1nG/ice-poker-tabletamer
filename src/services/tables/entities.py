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
    window: gw.Window | None = None
