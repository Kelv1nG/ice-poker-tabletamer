import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigurationParser:
    @classmethod
    def read_table_configuration(cls, *, filename="table_settings.json"):
        with open(BASE_DIR / "settings" / filename) as settings:
            file_contents = settings.read()
            parsed_settings = json.loads(file_contents)
            return parsed_settings["table_configuration"]

    @classmethod
    def write_table_configuration(cls, *, filename="table_settings.json", **kwargs):
        with open(BASE_DIR / "settings" / filename) as file:
            file_contents = file.read()
            parsed_settings = json.loads(file_contents)

        parsed_settings["table_configuration"] = kwargs

        with open(BASE_DIR / "settings" / filename, "w") as file:
            json_string = json.dumps(parsed_settings, indent=4)
            file.write(json_string)

    @classmethod
    def read_layout_configuration(cls, *, filename="layout_settings.json"):
        with open(BASE_DIR / "settings" / filename) as settings:
            file_contents = settings.read()
            parsed_settings = json.loads(file_contents)
            return parsed_settings["layout_configuration"]

    @classmethod
    def write_layout_configuration(cls, *, filename="layout_settings.json", **kwargs):
        with open(BASE_DIR / "settings" / filename) as file:
            file_contents = file.read()
            parsed_settings = json.loads(file_contents)

        parsed_settings["layout_configuration"] = kwargs

        with open(BASE_DIR / "settings" / filename, "w") as file:
            json_string = json.dumps(parsed_settings, indent=4)
            file.write(json_string)
