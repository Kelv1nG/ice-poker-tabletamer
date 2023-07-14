from services.layout.layout_manager import table_layout_manager
from widgets.table_layout.table_template import MainTableTemplate, TableTemplate


def show_layout():
    table_layout_manager.show_templates(
        cls_table_template=TableTemplate, cls_main_table_template=MainTableTemplate
    )
