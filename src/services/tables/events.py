from enum import Enum


class EventType(Enum):
    NEW_WINDOW = 'new_window'
    WINDOW_TERMINATED = 'window_terminated'
    WINDOW_MOVED = 'window_moved'
