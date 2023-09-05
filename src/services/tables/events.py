from enum import Enum


class EventType(Enum):
    NEW_WINDOW = 'new_window'
    ACTIVE_TAB_CHANGED = 'active_tab_changed'
    WINDOW_DELETED = 'window_deleted'
