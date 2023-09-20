from pynput import keyboard

from services.tables.entities import Buttons
from services.tables.table_config import table_configuration
from services.tables.table_manager import table_manager
from services.utilities import WindowsSelector

from .hotkeys_config import hotkey_configuration
from .mouse_controller import mouse_controller


class HotkeyManager:
    def __init__(
        self,
        hotkey_configuration=hotkey_configuration
    ):
        self.hotkey_configuration = hotkey_configuration
        self.keyboard_listener = None
        self.key_to_action = {}
        self.relative_coordinates = {}

    @property
    def hotkeys(self):
        return self.hotkey_configuration.hotkeys

    def win32_event_filter(self, msg, data):
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
        simulates left click and gets active window
        """
        mouse_controller.left_click()
        window = WindowsSelector.get_active_window()
        if window:
            slot = table_manager.slot_manager.get_slot_from_window(window)
            if slot:
                return slot.left, slot.top
        return None

    def on_press(self, key):
        if hasattr(key, "char") and key.char is not None:
            key_char = key.char
            action = self.key_to_action.get(
                key_char.upper(), self.key_to_action.get(key_char, None)
            )
            if action:
                self.handle_action(action)

    def start(self):
        self.update_relative_button_coordinates()

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press, win32_event_filter=self.win32_event_filter
        )
        self.populate_reverse_hotkeys()
        self.keyboard_listener.start()

    def stop(self):
        self.keyboard_listener.stop()
        self.keyboard_listener = None

    def move_to_amount_field(self, slot_coord: tuple[int, int]):
        """
        move the cursor to the amount field for a given slot.
        """
        button_coord = self.get_button_coordinate(slot_coord, button_type=Buttons.AMOUNT)
        mouse_controller.move_to_coordinates(button_coord[0], button_coord[1])

    def perform_base_action(
        self, button_type: Buttons, move_to_amount_field: bool = False
    ):
        """
        basic action when a hotkey is pressed

        simulates left click of button and moves the cursor afterwards whether the action
        requires to put in a desired amount
        """
        orig_mouse_coord = mouse_controller.get_mouse_coordinates()
        slot_coord = self.get_slot_coordinates()
        if not slot_coord:
            return

        button_coord = self.get_button_coordinate(
            slot_coord, button_type=button_type
        )
        mouse_controller.move_to_coordinates(button_coord[0], button_coord[1])
        mouse_controller.left_click()

        if move_to_amount_field:
            self.move_to_amount_field(slot_coord)
        else:
            mouse_controller.move_to_coordinates(orig_mouse_coord[0], orig_mouse_coord[1])

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
