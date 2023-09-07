import math
from dataclasses import dataclass

import pygetwindow as gw

from services.layout.layout_manager import TableLayOutManager

from . import exceptions
from .entities import Slot
from .table_config import TableConfiguration
from .utilities import AppName, WindowsSelector
from .events import EventType

class SlotManager:
    """
    class to manage slots and window allocation.
    """

    def __init__(self):
        self._slots: dict[str, Slot] = {}

    def allocate_window_to_slot(self, slot_num: str, process_window: gw.Window) -> None:
        """
        allocate a window to a specified slot.

        Args:
            slot_num (str): slot number to allocate the window to.
            process_window (gw.Window): window to be allocated.

        Raises:
            exceptions.SlotAlreadyOccupied: If the slot is already occupied by a window.
            exceptions.InvalidSlotNum: If the provided slot number is invalid.
        """
        if slot_num in self._slots:
            if self._slots[slot_num].window is None:
                self._slots[slot_num].window = process_window
                self._slots[slot_num].resize_window()
                self._slots[slot_num].move_to_assigned_slot()
            else:
                raise exceptions.SlotAlreadyOccupied(slot_num)
        else:
            raise exceptions.InvalidSlotNum(slot_num)

    def deallocate_slot(self, slot_num: str) -> None:
        """
        deallocate a window from a specified slot.

        args:
            slot_num (str): Slot number to deallocate the window from.

        raises:
            exceptions.EmptySlot: If the slot is already empty (no window allocated).
            exceptions.InvalidSlotNum: If the provided slot number is invalid.
        """
        if slot_num in self._slots:
            slot = self._slots[slot_num]
            if slot.window:
                slot.window = None
            else:
                raise exceptions.EmptySlot(slot_num)
        else:
            raise exceptions.InvalidSlotNum(slot_num)

    def add_window_to_empty_slot(self, window: gw.Window) -> None:
        """
        args:
            window: window to be allocated
        """
        empty_slots = {key: value for key, value in self.slots.items() if value.window is None}
        if len(empty_slots) > 0:
            # assign to first empty slot in order
            slot_num = next(iter(empty_slots.keys()))
            self.allocate_window_to_slot(slot_num=slot_num, process_window=window)

    def remove_window_from_slot(self, window: gw.Window) -> None:
        """
        args:
            window: window to be deallocated
        """
        for slot_num, slot in self.slots.items():
            if slot.window == window:
                self.deallocate_slot(slot_num)

    def get_center_for_each_slot(self) -> dict[str, tuple[int, int]]:
        """
        calculate the center coordinates for each slot.

        returns:
            dict: A dictionary mapping each slot number to its center coordinates.
        """
        center_coordinates = {}
        for slot_num, value in self._slots.items():
            center_coordinates[slot_num] = (value.top / 2, value.left / 2)
        return center_coordinates

    @property
    def allocated_windows(self) -> list[gw.Window]:
        return [slot.window for slot in self._slots.values() if slot.window is not None]

    @property
    def slots(self) -> dict[str, Slot]:
        return self._slots

    @slots.setter
    def slots(self, table_configurations: dict[str, Slot]) -> None:
        self._slots = table_configurations


class TableManager:
    """
    class for handling events and processes
    """
    def __init__(
        self,
        table_layout_manager: TableLayOutManager,
        table_configuration: TableConfiguration,
    ):
        self.table_layout_manager = table_layout_manager
        self.table_configuration = table_configuration
        self.slot_manager = SlotManager()

        self.tracked_windows: list[gw.Window] | list[None] = []

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

    def initialize_tracked_windows(self):
        self.tracked_windows = self.get_target_windows()

    def get_target_windows(self) -> list[gw.Window]:
        windows = WindowsSelector.get_windows_by_app_name(AppName.CHROME)
        return WindowsSelector.filter_windows_by_tab_title(tab_title=self.table_configuration.search_string, process_windows=windows)

    def get_unallocated_window(self) -> gw.Window | None:
        for window in self.tracked_windows:
            if window not in self.slot_manager.allocated_windows:
                return window
        return None

    def is_new_window_detected(self) -> tuple[bool, gw.Window | None]:
        """
        checks if a new window that satisfies the specified conditions is detected.

        function updates the list of tracked windows.

        Returns:
            A tuple containing two elements:
            1. A boolean value indicating whether a new window satisfying the conditions is detected.
            2. If a new window is detected, it returns the detected window;
            otherwise, it returns None to indicate no new window detected.
        """
        new_windows = [window for window in self.get_target_windows() if window not in self.tracked_windows]

        if len(new_windows) > 1:  # Program assumed to detect only 1 window at a time per cycle
            raise exceptions.MultipleWindowsDetected

        if new_windows:
            new_window = new_windows[0]
            self.tracked_windows.append(new_window)

        return bool(new_windows), new_windows[0] if new_windows else (False, None)

    def is_window_terminated(self) -> tuple[bool, gw.Window | None]:
        """
        checks if a tracked window is no longer satisfied based on certain conditions.
        This includes checking if the window is terminated or if its tab title has changed.

        function updates the list of tracked windows

        Returns:
            A tuple containing two elements:
            1. A boolean value indicating whether a tracked window is terminated or no longer satisfied.
            2. If a window is terminated or no longer satisfied, it returns the terminated window;
            otherwise, it returns None to indicate no terminated window.
        """
        deleted_windows = [window for window in self.tracked_windows if window not in self.get_target_windows()]

        if len(deleted_windows) > 1:
            raise exceptions.MultipleWindowsDetected

        if deleted_windows:
            deleted_window = deleted_windows[0]
            self.tracked_windows.remove(deleted_window)

        return bool(deleted_windows), deleted_windows[0] if deleted_windows else (False, None)

    def calculate_distance(
        self, win_coord: tuple[int, int], slot_coord: tuple[int, int]
    ) -> int:
        """
        calculate the distance between two points in a two-dimensional space (aka desktop coords lol).

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

    def arrange_layout_on_start(self):
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
                    distance = self.calculate_distance(
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

        self.initialize_slots()
        assign_windows_to_slots()

    def handle_event(self, event_type: EventType, window: gw.Window):
            match event_type:
                case EventType.NEW_WINDOW:
                    self.handle_new_window_event(window)
                case EventType.ACTIVE_TAB_CHANGED:
                    self.handle_active_tab_changed_event(window)
                case EventType.WINDOW_DELETED:
                    self.handle_window_terminated_event(window)

    def handle_new_window_event(self, window: gw.Window):
        self.slot_manager.add_window_to_empty_slot(window=window)

    def handle_active_tab_changed_event(self, window: gw.Window):
        pass

    def handle_window_terminated_event(self, window: gw.Window):
        """
        removes it from the tracked windows list and
        deallocates the window if its assigned to a slot
        """
        self.slot_manager.remove_window_from_slot(window)
        # check if a window in tracked_windows is unallocated and allocate it to a slot
        unallocated_window = self.get_unallocated_window()
        if unallocated_window:
            self.slot_manager.add_window_to_empty_slot(unallocated_window)



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
