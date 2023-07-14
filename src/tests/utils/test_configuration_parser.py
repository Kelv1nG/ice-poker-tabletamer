import json
from pathlib import Path

import pytest

from utils.configuration_parser import ConfigurationParser

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def table_settings_file(tmp_path):
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


@pytest.fixture
def layout_settings_file(tmp_path):
    # create a temporary file for testing
    settings_path = tmp_path / "layout_settings.json"
    settings_data = {
        "layout_configuration": {
            "table_count": 2,
            "table_configurations": {"slot_1": {"top": 5, "left": 6}},
        }
    }
    with open(settings_path, "w") as file:
        file.write(json.dumps(settings_data))
    yield settings_path


def test_read_table_configuration(table_settings_file):
    # Test reading table configuration from the settings file
    parsed_settings = ConfigurationParser.read_table_configuration(
        filename=str(table_settings_file)
    )
    assert parsed_settings["table_height"] == 5
    assert parsed_settings["table_width"] == 5
    assert parsed_settings["search_string"] == "SNG Tracker"


def test_write_table_configuration(table_settings_file):
    # Test writing table configuration to the settings file
    ConfigurationParser.write_table_configuration(
        filename=str(table_settings_file),
        table_height=10,
        table_width=10,
        search_string="New String",
    )

    # Read the updated settings file
    parsed_settings = ConfigurationParser.read_table_configuration(
        filename=str(table_settings_file)
    )
    assert parsed_settings["table_height"] == 10
    assert parsed_settings["table_width"] == 10
    assert parsed_settings["search_string"] == "New String"


def test_read_layout_configuration(layout_settings_file):
    # Test reading layout configuration from the settings file
    parsed_settings = ConfigurationParser.read_layout_configuration(
        filename=str(layout_settings_file)
    )
    assert parsed_settings["table_count"] == 2
    assert parsed_settings["table_configurations"]["slot_1"]["top"] == 5
    assert parsed_settings["table_configurations"]["slot_1"]["left"] == 6


def test_write_layout_configuration(layout_settings_file):
    ConfigurationParser.write_layout_configuration(
        filename=str(layout_settings_file),
        table_count=8,
        table_configurations={"slot_1": {"top": 7}, "slot_2": {"top": 23}},
    )

    parsed_settings = ConfigurationParser.read_layout_configuration(
        filename=str(layout_settings_file)
    )
    assert parsed_settings["table_count"] == 8
    assert parsed_settings["table_configurations"]["slot_1"]["top"] == 7
    assert parsed_settings["table_configurations"]["slot_2"]["top"] == 23
