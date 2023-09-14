from services.input_controllers import exceptions as hotkey_exceptions
from services.input_controllers.hotkeys_config import hotkey_configuration
from widgets.utils.popup import PopupMessage

HOTKEYS_MAP = {
    "FOLD": "hk_fold",
    "CHECK_CALL": "hk_check_call",
    "BET": "hk_bet",
    "RAISE": "hk_raise",
    "MOVE_TO_SLOT_1": "hk_move_to_slot_1",
    "MOVE_TO_SLOT_2": "hk_move_to_slot_2",
    "MOVE_TO_SLOT_3": "hk_move_to_slot_3",
    "MOVE_TO_SLOT_4": "hk_move_to_slot_4",
    "MOVE_TO_SLOT_5": "hk_move_to_slot_5",
    "MOVE_TO_SLOT_6": "hk_move_to_slot_6",
    "MOVE_TO_SLOT_7": "hk_move_to_slot_7",
    "MOVE_TO_SLOT_8": "hk_move_to_slot_8",
    "MOVE_TO_SLOT_9": "hk_move_to_slot_9",
    "MOVE_TO_SLOT_10": "hk_move_to_slot_10",
}

MESSAGES = {"DUPLICATE_HOTKEYS": "key duplication exist, please recheck"}


def load_settings(ui):
    for hk_action, hk_value in hotkey_configuration.hotkeys.items():
        input_ui = getattr(ui, HOTKEYS_MAP[hk_action])
        input_ui.setText(str(hk_value))


def get_hotkeys_from_ui(ui) -> dict:
    hotkeys = {}
    for hk_action, hk_ui_attr in HOTKEYS_MAP.items():
        input_ui = getattr(ui, hk_ui_attr)
        hotkeys[hk_action] = input_ui.text()
    return hotkeys


def save_settings(ui):
    hotkeys = get_hotkeys_from_ui(ui)
    try:
        hotkey_configuration.save_settings(hotkeys=hotkeys)
    except hotkey_exceptions.DuplicateHotkeysError:
        PopupMessage(title="Duplicate Hotkeys", message=MESSAGES["DUPLICATE_HOTKEYS"])
