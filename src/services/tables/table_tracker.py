import math
from dataclasses import dataclass

import pygetwindow as gw

from services.layout.layout_manager import TableLayOutManager

from . import exceptions
from .entities import Slot
from .table_manager import TableConfiguration
from .utilities import AppName, WindowsSelector


class SlotManager:
    """
    A class to manage slots and window allocation.
    """

    def __init__(self):
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

    def initialize_slots(self):
        """
        load the json data from configuration into slot objects
        """
        slot_dict = {}
        for key, value in self.table_layout.items():
            slot_dict[key] = Slot(
                top=value["top"],
                left=value["left"],
                height=self.table_configuration.height,
                width=self.table_configuration.width,
            )
        self.slot_manager.slots = slot_dict

    def get_target_windows(self) -> list[gw.Window]:
        windows = WindowsSelector.get_windows_by_app_name(AppName.CHROME)
        return WindowsSelector.filter_windows_by_tab_title(tab_title=self.table_configuration.search_string, process_windows=windows)

    def arrange_layout_on_start(self):
        def calculate_distance(
            win_coord: tuple[int, int], slot_coord: tuple[int, int]
        ) -> int:
            """
            Calculate the distance between two points in a two-dimensional space.

            Args:
                win_coord (tuple[int, int]): Center coordinates of the window as (center_y, center_x).
                slot_coord (tuple[int, int]): Center coordinates of the slot as (center_y, center_x).

            Returns:
                int: The distance between the center of the window and the center of the slot coordinates.
            """
            return math.sqrt(
                (win_coord[0] - slot_coord[0]) ** 2
                + (win_coord[1] - slot_coord[1]) ** 2
            )

        def assign_windows_to_slots() -> dict[str, Slot]:
            """
            Calculates all distances of slots to windows, assigns min distance of a window to a slot until
            all slots are taken or all windows are assigned
            """
            windows = self.get_target_windows()

            slot_center_coordinates = self.slot_manager.get_center_for_each_slot()
            windows_center_coordinates = WindowsSelector.get_center_for_windows(windows)

            # list of assigned windows to keep track of
            assigned_windows = []
            assigned_slots = []

            # calculate all distances for each target window and slot
            slot_distances_pair = {}
            for slot_num, slot_coord in slot_center_coordinates.items():
                distances = {}
                for (
                    win_coord_y,
                    win_coord_x,
                    target_window,
                ) in windows_center_coordinates:
                    distance = calculate_distance(
                        win_coord=(win_coord_y, win_coord_x), slot_coord=slot_coord
                    )
                    distances[distance] = target_window
                slot_distances_pair[slot_num] = distances

            # sort distances for each slot in ascending order
            for slot_num, distances in slot_distances_pair.items():
                sorted_distances = sorted(distances.items(), key=lambda x: x[0])

                # assign to the closest available slot
                for distance, target_window in sorted_distances:
                    if (
                        target_window not in assigned_windows
                        and slot_num not in assigned_slots
                    ):
                        self.slot_manager.allocate_window_to_slot(
                            slot_num, target_window
                        )
                        assigned_windows.append(target_window)
                        assigned_slots.append(slot_num)
            return self.slot_manager.slots

        def move_windows_to_slots():
            for slot in self.slot_manager.slots.values():
                slot.move_to_assigned_slot()

        def resize_windows():
            for slot in self.slot_manager.slots.values():
                slot.resize_window()

        self.initialize_slots()
        assign_windows_to_slots()
        move_windows_to_slots()
        resize_windows()

    def track_process(self, app_name: str):
        table_configurations = self.table_layout_manager.table_configurations
        # loop through each google chrome instance find closest match to configuration


if __name__ == "__main__":
    from services.layout.layout_manager import table_layout_manager
    from services.tables.table_manager import table_configuration

    process_tracker = ProcessTracker(
        table_configuration=table_configuration,
        table_layout_manager=table_layout_manager,
    )

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
