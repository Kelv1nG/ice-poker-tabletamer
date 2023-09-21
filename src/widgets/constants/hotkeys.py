HOTKEYS_MAP = {
    "FOLD": "hk_fold",
    "CHECK_CALL": "hk_check_call",
    "BET": "hk_bet",
    "RAISE": "hk_raise",
    "ENABLE_DISABLE": "hk_enable_disable",
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

ALPHABET = [chr(i).upper() for i in range(ord("a"), ord("z") + 1)]
FKEYS = [f"F{i}" for i in range(1, 13)]
MOUSE_BUTTONS = [
    "Button.right",
    "Button.x1",
    "Button.x2",
    "Button.middle",
]

HOTKEY_OPTIONS = ["-"] + MOUSE_BUTTONS + ALPHABET
