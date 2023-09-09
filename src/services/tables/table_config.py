import pyautogui

from utils.configuration_parser import (ConfigurationParser,
                                        IConfigurationParser)

from . import exceptions


class TableConfiguration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TableConfiguration, cls).__new__(cls)
        return cls._instance

    def __init__(self, configuration_parser: type[IConfigurationParser]):
        self._width: int = 0
        self._height: int = 0
        self._search_string: str = ""
        self.table = None
        self.table_settings = None
        self.configuration_parser = configuration_parser

        self.load_settings()

    @property
    def width(self):
        return self.configuration_parser.read_table_configuration().get(
            "table_width", 0
        )

    @property
    def height(self):
        return self.configuration_parser.read_table_configuration().get(
            "table_height", 0
        )

    @property
    def search_string(self):
        return self.configuration_parser.read_table_configuration().get(
            "search_string", 0
        )

    @property
    def current_width(self):
        return self._width

    @property
    def current_height(self):
        return self._height

    @search_string.setter
    def set_search_string(self, search_string: str):
        self._search_string = search_string

    def configure_single_table(self, table_name: str):
        """
        table_name: application name to be grabbed
        """
        try:
            self.table = pyautogui.getWindowsWithTitle(table_name)[0]
            # bring table to top by using activate
            self.table.activate()
        except IndexError:
            raise exceptions.NoTableFound
        else:
            self._width = self.table.width
            self._height = self.table.height

    def load_settings(self):
        self.table_settings = self.configuration_parser.read_table_configuration()
        self._width = self.table_settings.get("table_width", 0)
        self._height = self.table_settings.get("table_height", 0)
        self._search_string = self.table_settings.get("search_string", "")

    def save_settings(self):
        self.configuration_parser.write_table_configuration(
            table_height=self._height,
            table_width=self._width,
            search_string=self._search_string,
        )


table_configuration = TableConfiguration(ConfigurationParser)
