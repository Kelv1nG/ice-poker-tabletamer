import time

import pygetwindow as gw
from PyQt6.QtCore import QObject, pyqtSignal

from services.layout.layout_manager import table_layout_manager
from services.tables.events import EventType
from services.tables.table_config import table_configuration
from services.tables.table_manager import TableManager
from services.input_controllers.mouse_listener import mouse_listener
from services.tables.entities import Buttons
from services.input_controllers.mouse_controller import mouse_controller
from services.input_controllers.entities import key_states
from services.tables import exceptions as table_exceptions



table_manager = TableManager(
    table_layout_manager=table_layout_manager,
    table_configuration=table_configuration,
)

mouse_listener.start() # start mouse listener to handle mouse events

class Task(QObject):
    stop_signal = pyqtSignal(bool)
    exception_signal = pyqtSignal(object)

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
        self.stop_signal.emit(True)

    def handle_event(self, event_type: EventType, window: gw.Window):
        table_manager.handle_event(event_type=event_type, window=window)


class AssignButtonCoordinates(Task):
    def __init__(self, button_type: Buttons):
        super().__init__()
        self.button_type = button_type

    def run(self):
        time.sleep(0.25)
        while not self.is_stopped:
            if key_states.left_button_pressed:
                point = mouse_controller.get_mouse_coordinates()
                try:
                    table_configuration.configure_button_coordinates(button_type=self.button_type, coordinates=(point.x, point.y))
                except table_exceptions.ButtonOutsideWindowError as e:
                    self.exception_signal.emit(e)
                finally:
                    self.stop_signal.emit(True)
                    break
