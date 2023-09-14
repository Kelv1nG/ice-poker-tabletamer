from typing import Generic, TypeVar

from utils.configuration_parser import (
    IConfigurationParser,
    LayoutConfigurationParser,
    TableConfigurationParser,
)
from widgets.table_layout.table_template import TableTemplate

T = TypeVar("T", bound=TableTemplate)


class TableLayOutManager(Generic[T]):
    _shared_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._shared_instance:
            cls._shared_instance = super(TableLayOutManager, cls).__new__(cls)
        return cls._shared_instance

    def __init__(
        self,
        table_configuration_parser: type[IConfigurationParser],
        layout_configuration_parser: type[IConfigurationParser],
    ):
        self.table_templates: list[T] = []
        self.table_configuration_parser = table_configuration_parser
        self.layout_configuration_parser = layout_configuration_parser

    @classmethod
    def get_instance(
        cls,
        table_configuration_parser: type[IConfigurationParser],
        layout_configuration_parser: type[IConfigurationParser],
    ):
        if not cls._shared_instance:
            cls._shared_instance = TableLayOutManager(
                table_configuration_parser=table_configuration_parser,
                layout_configuration_parser=layout_configuration_parser,
            )
        return cls._shared_instance

    @property
    def table_settings(self) -> dict:
        return self.table_configuration_parser.read_configuration()

    @property
    def layout_settings(self) -> dict:
        return self.layout_configuration_parser.read_configuration()

    @property
    def table_configurations(self) -> dict:
        return self.layout_configuration_parser.read_configuration()[
            "table_configurations"
        ]

    def save_table_configuration(self):
        table_configurations = dict()
        for index, table in enumerate(self.table_templates):
            table_configurations["slot_" + str(index + 1)] = {
                "top": table.geometry().top(),
                "left": table.geometry().left(),
            }
        self.layout_configuration_parser.write_configuration(
            table_configurations=table_configurations
        )

    def save_table_count(self, table_count: int):
        self.layout_configuration_parserr.write_configuration(table_count=table_count)

    def show_templates(
        self, cls_table_template: type[T], cls_main_table_template: type[T]
    ):
        """
        table_template is a widget
        """
        self.table_templates = []  # destroy any widget so not to repopulate it again

        main_table_template = cls_main_table_template(
            left=self.table_configurations["slot_1"]["left"],
            top=self.table_configurations["slot_1"]["top"],
            table_height=self.table_settings.get("table_height", 0),
            table_width=self.table_settings.get("table_width", 0),
            number_label=1,
        )
        self.table_templates.append(main_table_template)
        for number_label in range(2, self.layout_settings.get("table_count", 1) + 1):
            left = self.table_configurations.get("slot_" + str(number_label), {}).get(
                "left", 0
            )
            top = self.table_configurations.get("slot_" + str(number_label), {}).get(
                "top", 0
            )
            table_template = cls_table_template(
                left=left,
                top=top,
                table_height=self.table_settings.get("table_height", 0),
                table_width=self.table_settings.get("table_width", 0),
                number_label=number_label,
            )
            self.table_templates.append(table_template)
        [table_template.show() for table_template in reversed(self.table_templates)]


table_layout_manager = TableLayOutManager.get_instance(
    table_configuration_parser=TableConfigurationParser,
    layout_configuration_parser=LayoutConfigurationParser,
)
