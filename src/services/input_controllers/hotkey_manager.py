from pynput import keyboard, mouse

from services.tables.entities import Buttons
from services.tables.table_config import table_configuration
from services.tables.table_manager import table_manager
from services.utilities import WindowsSelector

from .hotkeys_config import hotkey_configuration
from .mouse_controller import mouse_controller

import threading
from . import constants


class HotkeyManager:
    def __init__(
        self,
        hotkey_configuration=hotkey_configuration
    ):
        self.hotkey_configuration = hotkey_configuration
        self.keyboard_listener = None
        self.mouse_listener = None
        self.key_to_action = {}
        self.relative_coordinates = {}
        self.thread = None

    @property
    def hotkeys(self):
        return self.hotkey_configuration.hotkeys

    def mouse_event_filter(self, msg, data):
        """
        if click is coming from user data.flags = 0
        else if its done programmatically data.flags = 1

        Returning False would mean events wont be propagated to the
        rest of the system while suppress event completely suppresses the event
        i.e right clicking browser

        Additionally, actions related to suppressing browser interactions
        are handled within this function.
        """
        if msg in constants.SUPPRESSED_EVENTS and self.mouse_listener:
            button = constants.MOUSE_MESSAGE_DATA_TO_BUTTON_MAP.get((msg, data.mouseData), None)
            if (action := self.get_action_from_button(button)):
                self.start_action_thread(action)
            self.mouse_listener.suppress_event()
        if data.flags:
            return False

    def keyboard_event_filter(self, msg, data):
        if data.flags:
            return False

    def populate_reverse_hotkeys(self):
        """
        map and store the hotkey to an action for accessing it later on
        """
        self.key_to_action = {value: key for key, value in self.hotkeys.items()}
        for key, value in self.key_to_action.items():
            if key.isalnum():
                self.key_to_action[key] = value.upper()

    def update_relative_button_coordinates(self):
        """
        updates the relative coordinates of a button given a slot / window
        """
        for action, coordinate in table_configuration.button_coordinates.items():
            relative_coordinate = (
                coordinate[0] - table_configuration.left,
                coordinate[1] - table_configuration.top,
            )
            self.relative_coordinates[action] = relative_coordinate

    def get_button_coordinate(
        self, slot_coordinate: tuple[int, int], button_type: Buttons
    ) -> tuple[int, int]:
        """
        calculates button coordinate given a slot_coordinate

        returns:
            tuple[int, int]: a tuple of (x, y) coordinates
        """
        def get_absolute_coordinates(slot_coordinate, relative_coordinate):
            return (
                slot_coordinate[0] + relative_coordinate[0],
                slot_coordinate[1] + relative_coordinate[1],
            )
        return get_absolute_coordinates(
            slot_coordinate, self.relative_coordinates[button_type.value]
        )

    def get_slot_coordinates(self) -> tuple[int, int] | None:
        """
        Simulates a left click and retrieves the active window. If a slot is found within the window,
        this function returns a tuple containing the (x, y) coordinates of the slot.

        returns:
            tuple[int, int] | None: A tuple of (x, y) coordinates if a slot is found,
            or None if no slot is detected.
        """
        mouse_controller.left_click()
        window = WindowsSelector.get_active_window()
        if window:
            slot = table_manager.slot_manager.get_slot_from_window(window)
            if slot:
                return slot.left, slot.top
        return None

    def get_action_from_button(self, button) -> str | None:
        action = self.key_to_action.get(str(button))
        return action

    def start_action_thread(self, action):
        """
        Start a new thread to handle the given action.
        """
        self.thread = threading.Thread(target=self.handle_action, args=(action,))
        self.thread.start()

    def on_press(self, key):
        if hasattr(key, "char") and key.char is not None:
            key_char = key.char
            action = self.key_to_action.get(
                key_char.upper(), self.key_to_action.get(key_char, None)
            )
            if action:
                self.handle_action(action)

    def on_click(self, x, y, button, pressed):
        if pressed and (action := self.get_action_from_button(button)):
            self.start_action_thread(action)

    def start(self):
        self.update_relative_button_coordinates()

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press, win32_event_filter=self.keyboard_event_filter
        )
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click, win32_event_filter=self.mouse_event_filter
        )
        self.populate_reverse_hotkeys()
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self):
        self.keyboard_listener.stop()
        self.keyboard_listener = None
        self.mouse_listener.stop()
        self.mouse_listener = None

    def move_to_amount_field(self, slot_coord: tuple[int, int]):
        """
        move the cursor to the amount field associated with a given slot.

        args:
            slot_coord (tuple[int, int]): A tuple containing the (x, y) coordinates of the slot.
        """
        button_coord_x, button_coord_y = self.get_button_coordinate(slot_coord, button_type=Buttons.AMOUNT)
        mouse_controller.move_to_coordinates(button_coord_x, button_coord_y)

    def perform_base_action(
        self, button_type: Buttons, move_to_amount_field: bool = False
    ):
        """
        basic action when a hotkey is pressed

        simulates left click of button and moves the cursor afterwards whether the action
        requires to put in a desired amount
        """
        orig_mouse_coord_x, orig_mouse_coord_y = mouse_controller.get_mouse_coordinates()
        slot_coord = self.get_slot_coordinates()
        if not slot_coord:
            return

        button_coord_x, button_coord_y = self.get_button_coordinate(
            slot_coord, button_type=button_type
        )
        mouse_controller.move_to_coordinates(button_coord_x, button_coord_y)
        mouse_controller.left_click()

        if move_to_amount_field:
            self.move_to_amount_field(slot_coord)
        else:
            mouse_controller.move_to_coordinates(orig_mouse_coord_x, orig_mouse_coord_y)

    def perform_fold(self):
        self.perform_base_action(button_type=Buttons.FOLD)

    def perform_check_call(self):
        self.perform_base_action(button_type=Buttons.CHECK_CALL)

    def perform_raise(self):
        self.perform_base_action(button_type=Buttons.RAISE, move_to_amount_field=True)

    def perform_bet(self):
        self.perform_base_action(button_type=Buttons.BET, move_to_amount_field=True)

    def handle_action(self, action: str):
        match action:
            case Buttons.FOLD.value:
                self.perform_fold()
            case Buttons.CHECK_CALL.value:
                self.perform_check_call()
            case Buttons.BET.value:
                self.perform_bet()
            case Buttons.RAISE.value:
                self.perform_raise()


hotkey_manager = HotkeyManager(hotkey_configuration=hotkey_configuration)
