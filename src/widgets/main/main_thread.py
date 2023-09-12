from PyQt6.QtCore import QThread


def run_task(self, worker):
    self._worker = worker
    self._thread = QThread(self)  # set the parent to mainApp
    self._worker.moveToThread(self._thread)

    self._worker.finished.connect(self._thread.quit)
    self._thread.finished.connect(self._thread.deleteLater)
    self._thread.started.connect(self._worker.run)
    self._thread.start()
