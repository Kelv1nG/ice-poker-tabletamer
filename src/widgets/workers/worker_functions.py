from time import sleep

from services.layout.layout_manager import table_layout_manager
from services.tables.entities import AppName
from services.tables.table_manager import table_configuration
from services.tables.table_tracker import ProcessTracker
from services.tables.utilities import WindowsSelector
from widgets.workers.worker import WorkerFunction


class ProcessWorker(WorkerFunction):
    def __init__(self):
        super().__init__()
        self.process_tracker = ProcessTracker(
            table_layout_manager=table_layout_manager,
            table_configuration=table_configuration,
        )

    def run(self):
        self.process_tracker.arrange_layout_on_start()
        while not self.is_stopped:
            print("hello")
            sleep(1)
