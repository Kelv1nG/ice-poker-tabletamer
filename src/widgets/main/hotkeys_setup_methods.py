from PyQt6.QtWidgets import QMessageBox

from services.input_controllers import exceptions as hotkey_exceptions
from services.input_controllers.hotkeys_config import hotkey_configuration
from widgets.constants import hotkeys as hk_constants
from widgets.utils.popup import PopupMessage

MESSAGES = {
    "DUPLICATE_HOTKEYS": "key duplication exist, please recheck",
    "HOTKEYS_SAVED": "Successfully saved hotkeys",
}


def load_settings(ui):
    populate_selections(ui)
    for hk_action, hk_value in hotkey_configuration.hotkeys.items():
        input_ui = getattr(ui, hk_constants.HOTKEYS_MAP[hk_action])
        if hk_value == "":
            input_ui.setCurrentText("-")
        else:
            input_ui.setCurrentText(str(hk_value))


def get_hotkeys_from_ui(ui) -> dict:
    hotkeys = {}
    for hk_action, hk_ui_attr in hk_constants.HOTKEYS_MAP.items():
        if hasattr(ui, hk_ui_attr):
            input_ui = getattr(ui, hk_ui_attr)
            hotkeys[hk_action] = (
                input_ui.currentText() if input_ui.currentText() != "-" else ""
            )
    return hotkeys


def populate_selections(ui):
    for cbox_name in hk_constants.HOTKEYS_MAP.values():
        if hasattr(ui, cbox_name):
            input_ui = getattr(ui, cbox_name)
            # alphabet only on toggle hotkeys
            if cbox_name == 'hk_toggle_hotkeys':
                for hk_option in hk_constants.ALPHABET:
                    input_ui.addItem(hk_option)
            else:
                for hk_option in hk_constants.HOTKEY_OPTIONS:
                    input_ui.addItem(hk_option)


def save_settings(ui):
    hotkeys = get_hotkeys_from_ui(ui)
    try:
        hotkey_configuration.save_settings(hotkeys=hotkeys)
    except hotkey_exceptions.DuplicateHotkeysError:
        PopupMessage(title="Duplicate Hotkeys", message=MESSAGES["DUPLICATE_HOTKEYS"])
    else:
        PopupMessage(
            title="Hotkeys Settings Saved",
            message=MESSAGES["HOTKEYS_SAVED"],
            icon=QMessageBox.Icon.Information,
        )
