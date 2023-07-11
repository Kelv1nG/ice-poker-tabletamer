import pyautogui

from utils.configuration_parser import ConfigurationParser

from . import exceptions


class TableConfiguration:
    def __init__(self, configuration_parser: ConfigurationParser):
        self.width = 0
        self.height = 0
        self.search_string = ""
        self.table = None
        self.table_settings = None
        self.configuration_parser = configuration_parser

        self.load_settings()

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
            self.width = self.table.width
            self.height = self.table.height

    def load_settings(self):
        self.table_settings = self.configuration_parser.read_table_configuration()
        self.width = self.table_settings.get("table_width", 0)
        self.height = self.table_settings.get("table_height", 0)
        self.search_string = self.table_settings.get("search_string", "")

    def save_settings(self):
        self.configuration_parser.write_table_configuration(
            table_height=self.height,
            table_width=self.width,
            search_string=self.search_string,
        )


table_configuration = TableConfiguration(ConfigurationParser)
