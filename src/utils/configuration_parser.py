import json
from abc import ABC, abstractmethod
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class IConfigurationParser(ABC):
    @abstractmethod
    def read_configuration(self, filename: str, *args, **kwargs):
        pass

    @abstractmethod
    def write_configuration(self, filename: str, *args, **kwargs):
        pass


class TableConfigurationParser(IConfigurationParser):
    @staticmethod
    def read_configuration(filename="table_settings.json", *args, **kwargs):
        with open(BASE_DIR / "settings" / filename) as settings:
            file_contents = settings.read()
            parsed_settings = json.loads(file_contents)
            return parsed_settings["table_configuration"]

    @staticmethod
    def write_configuration(filename="table_settings.json", *args, **kwargs):
        with open(BASE_DIR / "settings" / filename) as file:
            file_contents = file.read()
            parsed_settings = json.loads(file_contents)

        parsed_settings["table_configuration"] = kwargs

        with open(BASE_DIR / "settings" / filename, "w") as file:
            json_string = json.dumps(parsed_settings, indent=4)
            file.write(json_string)


class LayoutConfigurationParser(IConfigurationParser):
    @staticmethod
    def read_configuration(filename="layout_settings.json", *args, **kwargs):
        with open(BASE_DIR / "settings" / filename) as settings_file:
            file_contents = settings_file.read()
            parsed_settings = json.loads(file_contents)
            return parsed_settings.get("layout_configuration", {})

    @staticmethod
    def write_configuration(filename="layout_settings.json", *args, **kwargs):
        with open(BASE_DIR / "settings" / filename) as file:
            file_contents = file.read()
            parsed_settings = json.loads(file_contents)

        layout_configuration = parsed_settings.get("layout_configuration", {})

        # Update the "table_count" and "table_configurations" in layout_configuration
        layout_configuration["table_count"] = kwargs.get(
            "table_count", layout_configuration["table_count"]
        )
        layout_configuration["table_configurations"] = kwargs.get(
            "table_configurations", layout_configuration["table_configurations"]
        )

        # Update the "layout_configuration" in the main parsed_settings
        parsed_settings["layout_configuration"] = layout_configuration

        with open(BASE_DIR / "settings" / filename, "w") as file:
            json_string = json.dumps(parsed_settings, indent=4)
            file.write(json_string)


class HotkeyConfigurationParser(IConfigurationParser):
    @staticmethod
    def read_configuration(filename="hotkey_settings.json", *args, **kwargs):
        with open(BASE_DIR / "settings" / filename) as settings_file:
            file_contents = settings_file.read()
            parsed_settings = json.loads(file_contents)
            return parsed_settings.get("hotkey_configuration", {})

    @staticmethod
    def write_configuration(filename="hotkey_settings.json", *args, **kwargs):
        with open(BASE_DIR / "settings" / filename) as file:
            file_contents = file.read()
            parsed_settings = json.loads(file_contents)

        parsed_settings["hotkey_configuration"] = kwargs['hotkeys']

        with open(BASE_DIR / "settings" / filename, "w") as file:
            json_string = json.dumps(parsed_settings, indent=4)
            file.write(json_string)
