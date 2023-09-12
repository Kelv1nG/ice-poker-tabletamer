import math

import pygetwindow as gw

from services.input_controllers.entities import key_states
from services.layout.layout_manager import TableLayOutManager

from . import exceptions
from .entities import Slot
from .events import EventType
from .table_config import TableConfiguration
from .utilities import AppName, WindowsSelector


class SlotManager:
    """
    class to manage slots and window allocation.
    """

    def __init__(self):
        self._slots: dict[str, Slot] = {}

    def allocate_window_to_slot(self, slot_num: str, window: gw.Window) -> None:
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
                self._slots[slot_num].window = window
                self._slots[slot_num].resize_window()
                self._slots[slot_num].move_to_assigned_slot()
            else:
                raise exceptions.SlotAlreadyOccupied(slot_num)
        else:
            raise exceptions.InvalidSlotNum(slot_num)

    def deallocate_window_from_slot(self, slot_num: str) -> gw.Window:
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
                window, slot.window = slot.window, None
                return window
            else:
                raise exceptions.EmptySlot(slot_num)
        else:
            raise exceptions.InvalidSlotNum(slot_num)

    def add_window_to_empty_slot(self, window: gw.Window) -> None:
        """
        args:
            window: window to be allocated
        """
        empty_slots = {
            key: value for key, value in self.slots.items() if value.window is None
        }
        if len(empty_slots) > 0:
            # assign to first empty slot in order
            slot_num = next(iter(empty_slots.keys()))
            self.allocate_window_to_slot(slot_num=slot_num, window=window)

    def remove_window_from_slot(self, window: gw.Window) -> None:
        """
        args:
            window: window to be deallocated
        """
        for slot_num, slot in self.slots.items():
            if slot.window == window:
                self.deallocate_window_from_slot(slot_num)

    def get_closest_slot_to_window(
        self, window: gw.Window, assign_to_empty_slot: bool = False
    ) -> str:
        """
        gets the closest slot num given a window

        args:
            window: window in which distance will be calculated
            assign_to_empty_slot (bool, optional): Whether to assign to an empty slot. Defaults to False.
        returns:
            str: closest slot num
        """
        window_center = (window.centery, window.centerx)

        # Filter the slots based on the assign_to_empty_slot flag
        if assign_to_empty_slot:
            filtered_slots = {
                slot_num: slot
                for slot_num, slot in self._slots.items()
                if slot.window is None
            }
        else:
            filtered_slots = self._slots

        # Find the closest slot
        closest_slot_num = min(
            filtered_slots,
            key=lambda slot_num: self.calculate_distance(
                win_coord=window_center,
                slot_coord=filtered_slots[slot_num].slot_center_coordinates,
            ),
        )

        return closest_slot_num

    def assign_window_to_closest_slot(self, window: gw.Window):
        """
        Assigns a window to the closest slot.

        If the closest slot is occupied, it swaps the windows between the slots.
        else just moves it to the closest slot
        """
        closest_slot_num = self.get_closest_slot_to_window(window)
        orig_slot_num = self.get_slot_num_from_window(window)

        closest_slot = self._slots[closest_slot_num]

        if closest_slot.window is not None:
            # swap the windows between the slots
            deallocated_window = self.deallocate_window_from_slot(closest_slot_num)
            self.allocate_window_to_slot(slot_num=closest_slot_num, window=window)
            self.deallocate_window_from_slot(orig_slot_num)
            self.allocate_window_to_slot(
                slot_num=orig_slot_num, window=deallocated_window
            )
        elif closest_slot.window is None:
            # assign the window to the closest slot
            self.deallocate_window_from_slot(orig_slot_num)
            self.allocate_window_to_slot(slot_num=closest_slot_num, window=window)

    def assign_window_to_closest_empty_slot(self, window: gw.Window):
        closest_slot_num = self.get_closest_slot_to_window(
            window=window, assign_to_empty_slot=True
        )
        self.allocate_window_to_slot(slot_num=closest_slot_num, window=window)

    def get_center_for_each_slot(self) -> dict[str, tuple[int, int]]:
        """
        calculate the center coordinates for each slot.

        returns:
            dict: A dictionary mapping each slot number to its center coordinates.
        """
        center_coordinates = {}
        for slot_num, slot in self._slots.items():
            center_coordinates[slot_num] = slot.slot_center_coordinates
        return center_coordinates

    def get_slot_from_window(self, window: gw.Window) -> Slot | None:
        for slot in self.slots.values():
            if slot.window == window:
                return slot
        return None

    def get_slot_num_from_window(self, window: gw.Window) -> str | None:
        for slot_num, slot in self.slots.items():
            if slot.window == window:
                return slot_num
        return None

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
            (win_coord[0] - slot_coord[0]) ** 2 + (win_coord[1] - slot_coord[1]) ** 2
        )

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
        return WindowsSelector.filter_windows_by_tab_title(
            tab_title=self.table_configuration.search_string, process_windows=windows
        )

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
        new_windows = [
            window
            for window in self.get_target_windows()
            if window not in self.tracked_windows
        ]

        if (
            len(new_windows) > 1
        ):  # Program assumed to detect only 1 window at a time per cycle
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
        deleted_windows = [
            window
            for window in self.tracked_windows
            if window not in self.get_target_windows()
        ]

        if len(deleted_windows) > 1:
            raise exceptions.MultipleWindowsDetected

        if deleted_windows:
            deleted_window = deleted_windows[0]
            self.tracked_windows.remove(deleted_window)

        return bool(deleted_windows), deleted_windows[0] if deleted_windows else (
            False,
            None,
        )

    def is_window_moved(self) -> tuple[bool, gw.Window | None]:
        """
        Check if any window has been moved from its original position.

        returns:
            tuple: A tuple containing two elements:
                - A boolean value indicating whether any window has been moved.
                - If a window has been moved, it returns the moved window; otherwise, it returns None.
        """
        for slot in self.slot_manager.slots.values():
            if slot.window:
                current_position = slot.window.left, slot.window.top
                if current_position != (slot.left, slot.top):
                    return True, slot.window
        return False, None

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
                    distance = self.slot_manager.calculate_distance(
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

    def get_event(self) -> tuple[EventType | None, gw.Window | None]:
        has_new_window, new_window = self.is_new_window_detected()
        is_window_terminated, terminated_window = self.is_window_terminated()
        is_window_moved, moved_window = self.is_window_moved()

        if has_new_window:
            return EventType.NEW_WINDOW, new_window
        elif is_window_terminated:
            return EventType.WINDOW_TERMINATED, terminated_window
        elif is_window_moved:
            return EventType.WINDOW_MOVED, moved_window
        return None, None

    def handle_event(self, event_type: EventType, window: gw.Window):
        match event_type:
            case EventType.NEW_WINDOW:
                self.handle_new_window_event(window)
            case EventType.WINDOW_TERMINATED:
                self.handle_window_terminated_event(window)
            case EventType.WINDOW_MOVED:
                self.handle_window_moved_event(window)

    def handle_new_window_event(self, window: gw.Window):
        self.slot_manager.assign_window_to_closest_empty_slot(window)

    def handle_window_terminated_event(self, window: gw.Window):
        """
        deallocates the window if its assigned to a slot
        """
        self.slot_manager.remove_window_from_slot(window)
        # check if a window in tracked_windows is unallocated and allocate it to a slot
        unallocated_window = self.get_unallocated_window()
        if unallocated_window:
            self.slot_manager.add_window_to_empty_slot(unallocated_window)

    def handle_window_moved_event(self, window: gw.Window):
        slot = self.slot_manager.get_slot_from_window(window=window)
        if not key_states.left_button_pressed:  # check if left mouse button is released
            if slot.is_center_outside_slot_boundary:
                self.slot_manager.assign_window_to_closest_slot(window=window)
            else:
                slot.move_to_assigned_slot()
