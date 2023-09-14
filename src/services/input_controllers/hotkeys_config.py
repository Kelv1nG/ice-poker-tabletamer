from utils.configuration_parser import IConfigurationParser, HotkeyConfigurationParser
from services.tables.table_config import table_configuration
from services.tables.entities import Buttons
from . import exceptions as hotkey_exceptions


class HotkeyConfiguration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HotkeyConfiguration, cls).__new__(cls)
        return cls._instance

    def __init__(self, configuration_parser: IConfigurationParser):
        self.hotkeys = {}
        self.configuration_parser = configuration_parser

        self.load_settings() # load initial set hotkeys

    def load_settings(self):
        self.hotkeys = self.configuration_parser.read_configuration()

    def check_for_hk_duplicates(self) -> None:
        hotkey_values = [value for value in self.hotkeys.values() if value != '']
        if len(set(hotkey_values)) < len(hotkey_values):
            raise hotkey_exceptions.DuplicateHotkeysError

    def save_settings(self, hotkeys: dict):
        self.hotkeys = hotkeys
        self.check_for_hk_duplicates()
        self.configuration_parser.write_configuration(hotkeys=self.hotkeys)




hotkey_configuration = HotkeyConfiguration(configuration_parser=HotkeyConfigurationParser)
