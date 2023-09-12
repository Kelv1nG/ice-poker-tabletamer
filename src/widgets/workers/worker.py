from PyQt6.QtCore import QObject, pyqtSignal

from widgets.workers.task import Task


class Worker(QObject):
    finished = pyqtSignal()
    stop_signal = pyqtSignal(bool)
    exception_signal = pyqtSignal(object)

    def __init__(self, task: Task):
        super().__init__()
        self.task = task

    def run(self):
        self.stop_signal.connect(self.task.stop_signal)
        self.task.stop_signal.connect(self.finish) # for cleaning up thread
        self.task.exception_signal.connect(self.handle_exception)

        self.task.run()

    def stop(self): # for sending signal to task
        self.stop_signal.emit(True)
        self.finished.emit()

    def finish(self):
        self.finished.emit()

    def handle_exception(self, object):
        self.exception_signal.emit(object)
