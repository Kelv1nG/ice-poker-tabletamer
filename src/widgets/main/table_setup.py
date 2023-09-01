from PyQt6.QtWidgets import QMessageBox

from services.tables import exceptions as table_exceptions
from services.tables.table_manager import table_configuration
from widgets.utils.popup import PopupMessage

MESSAGES = {
    "NO_TABLE_FOUND": "No table found, please verify if search string matches table name",
    "TABLE_DETECTED": "Table Detected, Current height: {table_height}, width: {table_width}",
    "TABLE_SETTING_SAVED": "Successfully saved table settings",
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


def load_settings(ui):
    table_configuration.load_settings()
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
