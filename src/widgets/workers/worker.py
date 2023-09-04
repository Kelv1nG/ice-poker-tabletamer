import time
from abc import ABC, abstractmethod

from PyQt6.QtCore import QObject, pyqtSignal


class WorkerFunction(QObject):
    stop_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.is_stopped = False

        self.stop_signal.connect(self.handle_stop_signal)

    def run(self):
        raise NotImplementedError("Run not implemented")

    def handle_stop_signal(self, stop_flag: bool):
        self.is_stopped = stop_flag


class Worker(QObject):
    finished = pyqtSignal()
    stop_signal = pyqtSignal(bool)

    def __init__(self, worker_function: WorkerFunction):
        super().__init__()
        self.worker_function = worker_function

    def run(self):
        self.stop_signal.connect(self.worker_function.stop_signal)
        self.worker_function.run()

    def stop(self):
        self.stop_signal.emit(True)
        self.finished.emit()  # for cleanup
