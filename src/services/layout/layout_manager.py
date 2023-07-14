from typing import Any, Generic, TypeVar

from utils.configuration_parser import ConfigurationParser
from widgets.table_layout.table_template import MainTableTemplate, TableTemplate

T = TypeVar("T", bound=TableTemplate)


class TableLayOutManager(Generic[T]):
    def __init__(self, configuration_parser: type[ConfigurationParser]):
        self.table_templates: list[T] = []
        self.configuration_parser = configuration_parser
        self.table_settings: dict[Any, Any] = dict()
        self.layout_settings: dict[Any, Any] = dict()

        self.load_settings()

    def load_settings(self):
        self.table_settings = self.configuration_parser.read_table_configuration()
        self.layout_settings = self.configuration_parser.read_layout_configuration()

    def show_templates(
        self, cls_table_template: type[T], cls_main_table_template: type[T]
    ):
        """
        table_template is a widget
        """
        self.load_settings()  # reload settings to check if any changes have been made
        self.table_templates = []  # destroy any widget so not to repopulate it again

        main_table_template = cls_main_table_template(
            left=0,
            top=0,
            table_height=self.table_settings.get("table_height", 0),
            table_width=self.table_settings.get("table_width", 0),
            number_label=1,
        )
        self.table_templates.append(main_table_template)
        for number_label in range(2, self.layout_settings.get("table_count", 1) + 2):
            table_template = cls_table_template(
                left=0,
                top=0,
                table_height=self.table_settings.get("table_height", 0),
                table_width=self.table_settings.get("table_width", 0),
                number_label=number_label,
            )
            self.table_templates.append(table_template)
        self.table_templates.reverse()  # slot 1 should appear last and should be visible right away
        [table_template.show() for table_template in self.table_templates]


table_layout_manager: TableLayOutManager = TableLayOutManager(ConfigurationParser)
