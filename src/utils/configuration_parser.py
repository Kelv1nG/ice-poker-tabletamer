import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigurationParser:
    @classmethod
    def read_table_configuration(cls):
        with open(BASE_DIR / "settings.json") as settings:
            file_contents = settings.read()
            parsed_settings = json.loads(file_contents)
            return parsed_settings["table_configuration"]

    @classmethod
    def write_table_configuration(cls):
        ...
