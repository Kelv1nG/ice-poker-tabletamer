
import math

from utilities import AppName, WindowsSelector
from services.layout.layout_manager import TableLayOutManager
from services.tables.table_manager import TableConfiguration
from . import exceptions
from dataclasses import dataclass
import pygetwindow as gw


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
    window: gw.Window | None


class SlotManager:
    """
    A class to manage slots and window allocation.
    """
    def __init__(self):
        """
        Initialize the SlotManager class to manage window slots and allocation.
        """
        self._slots: dict[str, Slot] = {}

    def allocate_window_to_slot(self, slot_num: str, process_window: gw.Window) -> None:
        """
        Allocate a window to a specified slot.

        Args:
            slot_num (str): Slot number to allocate the window to.
            process_window (gw.Window): The window to be allocated.

        Raises:
            exceptions.SlotAlreadyOccupied: If the slot is already occupied by a window.
            exceptions.InvalidSlotNum: If the provided slot number is invalid.
        """
        if slot_num in self._slots:
            if self._slots[slot_num].window is None:
                self._slots[slot_num].window = process_window
            else:
                raise exceptions.SlotAlreadyOccupied(slot_num)
        else:
            raise exceptions.InvalidSlotNum(slot_num)

    def deallocate_slot(self, slot_num: str) -> None:
        """
        Deallocate a window from a specified slot.

        Args:
            slot_num (str): Slot number to deallocate the window from.

        Raises:
            exceptions.EmptySlot: If the slot is already empty (no window allocated).
            exceptions.InvalidSlotNum: If the provided slot number is invalid.
        """
        if slot_num in self._slots:
            slot_info = self._slots[slot_num]
            if slot_info.window:
                slot_info.window = None
            else:
                raise exceptions.EmptySlot(slot_num)
        else:
            raise exceptions.InvalidSlotNum(slot_num)

    def get_center_for_each_slot(self) -> dict[str, tuple[int, int]]:
        """
        Calculate the center coordinates for each slot.

        Returns:
            dict: A dictionary mapping each slot number to its center coordinates.
        """
        center_coordinates = {}
        for slot_num, value in self._slots.items():
            center_coordinates[slot_num] = (value.top / 2, value.left / 2)
        return center_coordinates

    @property
    def slots(self) -> dict[str, Slot]:
        return self._slots

    @slots.setter
    def slots(self, table_configurations: dict[str, Slot]) -> None:
        self._slots = table_configurations

class ProcessTracker:
    def __init__(
        self,
        table_layout_manager: TableLayOutManager,
        table_configuration: TableConfiguration,
    ):
        self.table_layout_manager = table_layout_manager
        self.table_configuration = table_configuration
        self.slot_manager = SlotManager()

    @property
    def table_layout(self):
        return self.table_layout_manager.table_configurations

    @property
    def table_height(self):
        return self.table_configuration.height

    @property
    def table_width(self):
        return self.table_configuration.width

    @property
    def table_search_string(self):
        return self.table_configuration.search_string

    def intialize_slots(self):
        self.slot_manager.slots = self.table_layout

    def arrange_layout_on_start(self, windows: list[gw.Window]):
        def calculate_distance(win_coord: tuple[int, int], slot_coord: tuple[int, int]) -> int:
            """
            Calculate the distance between two points in a two-dimensional space.

            Args:
                win_coord (tuple[int, int]): Center coordinates of the window as (center_y, center_x).
                slot_coord (tuple[int, int]): Center coordinates of the slot as (center_y, center_x).

            Returns:
                int: The distance between the center of the window and the center of the slot coordinates.
            """
            return math.sqrt((win_coord[0] - slot_coord[0])^2 + (win_coord[1] - slot_coord[1])^2)

        def assign_windows_to_slots():
            slot_center_coordinates = self.slot_manager.get_center_for_each_slot()
            windows_center_coordinates = WindowsSelector.get_center_for_windows(windows)

            for windows_coord in windows_center_coordinates:
                min_distance = 0

                for slot_coord in slot_center_coordinates:
                    distance = calculate_distance((windows_coord[0], windows_coord[1]), (slot_coord[0], slot_coord[1]))




        self.initialize_slots()





    def track_process(self, app_name: str):
        table_configurations = self.table_layout_manager.table_configurations
        print(table_configurations)
        # loop through each google chrome instance find closest match to configuration


# def track_processes(app_name: str, table_positions: dict, table_layout: dict):
#     original_positions = {}  # Dictionary to store the original positions of windows

#     while True:
#         windows = get_windows_by_title(app_name)
#         for window in windows:
#             pid = window._hWnd  # Get the process ID (window handle) as PID

#             # Check if the window's position has changed
#             if pid not in original_positions:
#                 # Store the original position for the window
#                 original_positions[pid] = (window.left, window.top)
#             else:
#                 # Compare the current position with the original position
#                 original_left, original_top = original_positions[pid]
#                 current_left, current_top = window.left, window.top

#                 if original_left != current_left or original_top != current_top:
#                     print(f"Window with PID {pid} has moved.")

#             # Get the active tab title for the Chrome/Firefox instance
#             active_tab_title = get_active_tab_title(app_name, window)
#             print(f"Window title: {window.title}, Active tab title: {active_tab_title}")

#         time.sleep(1)
