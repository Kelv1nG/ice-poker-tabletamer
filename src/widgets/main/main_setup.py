from time import sleep

from widgets.main.main_thread import run_task
from widgets.workers.worker import Worker
from widgets.workers.task import TrackProcess

START = "Start!"
STOP = "Stop"


def hide_labels_on_stop(ui):
    ui.running_label.hide()
    ui.table_count_label.hide()
    ui.table_count_display.hide()


def show_labels_on_start(ui):
    ui.running_label.show()
    ui.table_count_label.show()
    ui.table_count_display.show()


def on_start(self, ui):
    text = ui.start_button.text()
    if text == START:
        show_labels_on_start(ui)
        run_task(self, Worker(task=TrackProcess()))

        ui.start_button.setText(STOP)
    elif text == STOP:
        hide_labels_on_stop(ui)
        self._worker.stop()

        ui.start_button.setText(START)
