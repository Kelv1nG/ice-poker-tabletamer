import json
from pathlib import Path

import pytest

from utils.configuration_parser import ConfigurationParser

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def settings_file(tmp_path):
    # Create a temporary settings file for testing
    # tmp_path is a pytest fixture for creating a temporary path
    settings_path = tmp_path / "table_settings.json"
    settings_data = {
        "table_configuration": {
            "table_height": 5,
            "table_width": 5,
            "search_string": "SNG Tracker",
        },
    }
    with open(settings_path, "w") as file:
        file.write(json.dumps(settings_data))
    yield settings_path


def test_read_table_configuration(settings_file):
    # Test reading table configuration from the settings file
    parsed_settings = ConfigurationParser.read_table_configuration(
        filename=str(settings_file)
    )
    print(parsed_settings)
    assert parsed_settings["table_height"] == 5
    assert parsed_settings["table_width"] == 5
    assert parsed_settings["search_string"] == "SNG Tracker"


def test_write_table_configuration(settings_file):
    # Test writing table configuration to the settings file
    ConfigurationParser.write_table_configuration(
        filename=str(settings_file),
        table_height=10,
        table_width=10,
        search_string="New String",
    )

    # Read the updated settings file
    parsed_settings = ConfigurationParser.read_table_configuration(
        filename=str(settings_file)
    )
    assert parsed_settings["table_height"] == 10
    assert parsed_settings["table_width"] == 10
    assert parsed_settings["search_string"] == "New String"
