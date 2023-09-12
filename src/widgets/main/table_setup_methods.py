from PyQt6.QtWidgets import QMessageBox

from services.tables import exceptions as table_exceptions
from services.tables.entities import Buttons
from services.tables.table_config import table_configuration
from widgets.main.main_thread import run_task
from widgets.utils.popup import PopupMessage
from widgets.workers.task import AssignButtonCoordinates
from widgets.workers.worker import Worker

MESSAGES = {
    "NO_TABLE_FOUND": "No table found, please verify if search string matches table name",
    "TABLE_DETECTED": "Table Detected, Current height: {table_height}, width: {table_width}",
    "TABLE_SETTING_SAVED": "Successfully saved table settings",
    "BUTTON_COORDINATES_OUT_OF_BOUNDS": "Button Coordinate is outside the target window",
}

BUTTON_DISPLAY_MAP = {
    Buttons.FOLD: "fold_coord",
    Buttons.CHECK_CALL: "check_call_coord",
    Buttons.BET: "bet_coord",
    Buttons.RAISE: "raise_coord",
    Buttons.AMOUNT: "amount_coord",
}


def search_table(ui):
    table_name = ui.table_string_search.text()
    try:
        table_configuration.configure_single_table(table_name)
    except table_exceptions.NoTableFound:
        PopupMessage(
            title="No Table Found",
            message=MESSAGES["NO_TABLE_FOUND"],
            icon=QMessageBox.Icon.Warning,
        )
    else:
        table_height = str(table_configuration.current_height)
        table_width = str(table_configuration.current_width)
        PopupMessage(
            title="Table Detected",
            message=MESSAGES["TABLE_DETECTED"].format(
                table_height=table_height, table_width=table_width
            ),
        )


def update_coordinates_display(button_type: Buttons, ui):
    x_coord, y_coord = table_configuration.current_button_coordinates.get(
        button_type.value, (0, 0)
    )
    attribute = getattr(ui, BUTTON_DISPLAY_MAP[button_type])
    if attribute:
        attribute.setText(f"{str(x_coord)}, {str(y_coord)}")


def show_unbounded_coordinates_popup(exc):
    if isinstance(exc, table_exceptions.ButtonOutsideWindowError):
        PopupMessage(
            title="Unbounded Coordinates",
            message=MESSAGES["BUTTON_COORDINATES_OUT_OF_BOUNDS"],
        )


def grab_coordinate(self, button_type: Buttons, ui):
    def update_display():
        update_coordinates_display(button_type=button_type, ui=ui)

    worker = Worker(task=AssignButtonCoordinates(button_type=button_type))
    worker.exception_signal.connect(show_unbounded_coordinates_popup)
    worker.finished.connect(update_display)
    run_task(self, worker=worker)


def grab_fold(self, ui):
    grab_coordinate(self=self, button_type=Buttons.FOLD, ui=ui)


def grab_check_call(self, ui):
    grab_coordinate(self=self, button_type=Buttons.CHECK_CALL, ui=ui)


def grab_bet(self, ui):
    grab_coordinate(self=self, button_type=Buttons.BET, ui=ui)


def grab_raise(self, ui):
    grab_coordinate(self=self, button_type=Buttons.RAISE, ui=ui)


def grab_amount(self, ui):
    grab_coordinate(self=self, button_type=Buttons.AMOUNT, ui=ui)


def load_coordinates(ui):
    for button in Buttons:
        update_coordinates_display(button, ui)


def load_settings(ui):
    table_configuration.load_settings()
    load_coordinates(ui)
    table_height = str(table_configuration.height)
    table_width = str(table_configuration.width)
    table_search_string = table_configuration.search_string

    ui.table_height.setText(table_height)
    ui.table_width.setText(table_width)
    ui.table_string_search.setText(table_search_string)


def save_settings(ui):
    table_configuration.save_settings()
    table_height = str(table_configuration.height)
    table_width = str(table_configuration.width)
    ui.table_height.setText(table_height)
    ui.table_width.setText(table_width)
    PopupMessage(
        title="Table Settings Saved",
        message=MESSAGES["TABLE_SETTING_SAVED"],
        icon=QMessageBox.Icon.Information,
    )
