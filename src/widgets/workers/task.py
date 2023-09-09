from services.layout.layout_manager import table_layout_manager
from services.tables.entities import AppName
from services.tables.table_config import table_configuration
from services.tables.table_manager import TableManager
from services.tables.utilities import WindowsSelector
from services.tables.events import EventType
import pygetwindow as gw

from PyQt6.QtCore import QObject, pyqtSignal

import time

table_manager = TableManager(
            table_layout_manager=table_layout_manager,
            table_configuration=table_configuration,
        )


class Task(QObject):
    stop_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.is_stopped = False

        self.stop_signal.connect(self.handle_stop_signal)

    def run(self):
        """
        method should be overridden by subclasses to define the actual task
        """
        raise NotImplementedError("Run not implemented")

    def handle_stop_signal(self, stop_flag: bool):
        self.is_stopped = stop_flag


class TrackProcess(Task):
    event_signal = pyqtSignal(EventType, gw.Window)

    def __init__(self):
        super().__init__()
        self.event_signal.connect(self.handle_event)

    def run(self):
        table_manager.initialize_tracked_windows()
        table_manager.arrange_layout_on_start()
        while not self.is_stopped:
            event_type, window = table_manager.get_event()
            if event_type is not None:
                self.event_signal.emit(event_type, window)

    def handle_event(self, event_type: EventType, window: gw.Window):
        table_manager.handle_event(event_type=event_type, window=window)
