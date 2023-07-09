import pyautogui

from utils.configuration_parser import ConfigurationParser

from . import exceptions


class TableConfiguration:
    def __init__(self, configuration_parser: ConfigurationParser):
        self.width = 0
        self.height = 0
        self.search_string = ''
        self.table = None
        self.configuration_parser = configuration_parser
        self.load_settings()

    def configure_single_table(self, table_name: str):
        """
        table_name: application name to be grabbed
        """
        try:
            self.table = pyautogui.getWindowsWithTitle(table_name)[0]
        except IndexError:
            raise exceptions.NoTableFound
        else:
            self.width = self.table.width
            self.height = self.table.height

    def load_settings(self):
        settings = self.configuration_parser.read_table_configuration()
        self.width = settings.get('table_width', 0)
        self.height = settings.get('table_height', 0)
        self.search_string = settings.get('search_string', '')


def get_all_tables(table_name: str):
    """
    table_name: application name to be grabbed
    """
    return pyautogui.getWindowsWithTitle(table_name)


table_configuration = TableConfiguration(ConfigurationParser)
