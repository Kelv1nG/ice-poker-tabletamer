from services.layout.layout_manager import table_layout_manager
from services.tables.entities import AppName
from services.tables.table_config import table_configuration
from services.tables.table_manager import ProcessManager
from services.tables.utilities import WindowsSelector

from PyQt6.QtCore import QObject, pyqtSignal

import time


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
    def __init__(self):
        super().__init__()
        self.process_tracker = ProcessManager(
            table_layout_manager=table_layout_manager,
            table_configuration=table_configuration,
        )

    def run(self):
        self.process_tracker.arrange_layout_on_start()
        t1 = time.time()
        i =0
        while not self.is_stopped:
            new = self.process_tracker.get_target_windows()
            print(new)
            i += 1
            if i == 1000:
                break
        t2 = time.time()
        print(t2-t1)
