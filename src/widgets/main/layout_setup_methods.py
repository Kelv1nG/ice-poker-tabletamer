from services.layout.layout_manager import table_layout_manager
from widgets.table_layout.main_table_template import MainTableTemplate
from widgets.table_layout.table_template import TableTemplate


def load_settings(ui):
    layout_settings = table_layout_manager.layout_settings
    ui.table_count_value.setText(str(layout_settings.get("table_count")))


def add_table_count(ui):
    init_table_count = table_layout_manager.layout_settings.get("table_count")
    new_table_count = init_table_count + 1
    table_layout_manager.save_table_count(new_table_count)

    ui.table_count_value.setText(str(new_table_count))


def reduce_table_count(ui):
    init_table_count = table_layout_manager.layout_settings.get("table_count")
    new_table_count = init_table_count - 1
    if new_table_count != 0:
        table_layout_manager.save_table_count(new_table_count)
        ui.table_count_value.setText(str(new_table_count))


def show_layout():
    table_layout_manager.show_templates(
        cls_table_template=TableTemplate, cls_main_table_template=MainTableTemplate
    )
