from services.tables import exceptions as table_exceptions
from services.tables.table_manager import table_configuration
from widgets.utils.popup import PopupMessage
from PyQt6.QtWidgets import QMessageBox


MESSAGES = {
    'NO_TABLE_FOUND': 'No table found, please verify if search string matches table name'
}


def search_table(ui):
    table_name = ui.table_string_search.text()
    try:
        table_configuration.configure_single_table(table_name)
    except table_exceptions.NoTableFound:
        PopupMessage(
            title='No Table Found',
            message=MESSAGES['NO_TABLE_FOUND'],
            icon=QMessageBox.Icon.Warning
        )
    else:
        table_height = str(table_configuration.height)
        table_width = str(table_configuration.width)
        ui.table_height.setText(table_height)
        ui.table_width.setText(table_width)


def load_settings(ui):
    table_configuration.load_settings()
    table_height = str(table_configuration.height)
    table_width = str(table_configuration.width)
    table_search_string = table_configuration.search_string

    ui.table_height.setText(table_height)
    ui.table_width.setText(table_width)
    ui.table_string_search.setText(table_search_string)
