from PyQt6.QtCore import QObject, pyqtSignal

from widgets.workers.task import Task


class Worker(QObject):
    finished = pyqtSignal()
    stop_signal = pyqtSignal(bool)

    def __init__(self, task: Task):
        super().__init__()
        self.task = task

    def run(self):
        self.stop_signal.connect(self.task.stop_signal)
        self.task.run()

    def stop(self):
        self.stop_signal.emit(True)
        self.finished.emit()  # for cleanup
