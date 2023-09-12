import pyautogui

from utils.configuration_parser import (ConfigurationParser,
                                        IConfigurationParser)

from . import exceptions
from .entities import Buttons


class TableConfiguration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TableConfiguration, cls).__new__(cls)
        return cls._instance

    def __init__(self, configuration_parser: type[IConfigurationParser]):
        self._current_width: int = 0
        self._current_height: int = 0
        self._search_string: str = ""
        self._top: int = 0  # table top/left coordinates
        self._left: int = 0
        self._button_coords = {}
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
    def button_coordinates(self):
        return self.configuration_parser.read_layout_configuration().get(
            "button_coordinates", {}
        )

    @property
    def search_string(self):
        return self.configuration_parser.read_table_configuration().get(
            "search_string", 0
        )

    @property
    def current_width(self):
        return self._current_width

    @property
    def current_height(self):
        return self._current_height

    @property
    def current_button_coordinates(self):
        return self._button_coords

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
            self._current_width = self.table.width
            self._current_height = self.table.height
            self._top = self.table.top
            self._left = self.table.left

    def configure_button_coordinates(
        self, button_type: Buttons, coordinates: tuple[int, int]
    ):
        x, y = coordinates
        outside_y = (y < self._top) or (y > (self._top + self._current_height))
        outside_x = (x < self._left) or (x > (self._left + self.current_width))
        if outside_y or outside_x:
            raise exceptions.ButtonOutsideWindowError
        self._button_coords[button_type.value] = coordinates

    def load_settings(self):
        self.table_settings = self.configuration_parser.read_table_configuration()
        self._current_width = self.table_settings.get("table_width", 0)
        self._current_height = self.table_settings.get("table_height", 0)
        self._search_string = self.table_settings.get("search_string", "")
        self._top = self.table_settings.get("top", 0)
        self._left = self.table_settings.get("left", 0)
        self._button_coords = self.table_settings.get("button_coordinates", {})

    def save_settings(self):
        self.configuration_parser.write_table_configuration(
            table_height=self._current_height,
            table_width=self._current_width,
            search_string=self._search_string,
            top=self._top,
            left=self._left,
            button_coordinates=self._button_coords,
        )


table_configuration = TableConfiguration(ConfigurationParser)
