from unittest.mock import MagicMock, patch

import pytest

from services.tables.exceptions import NoTableFound
from services.tables.table_config import (IConfigurationParser,
                                          TableConfiguration)


@pytest.fixture
def mock_configuration_parser():
    # Fixture to create a mocked ConfigurationParser instance
    return MagicMock(spec=IConfigurationParser)


def test_singleton_instance(mock_configuration_parser):
    table_config_1 = TableConfiguration(mock_configuration_parser)
    table_config_2 = TableConfiguration(mock_configuration_parser)

    assert table_config_1 is table_config_2


def test_configure_single_table_found(mock_configuration_parser):
    # Replace pyautogui.getWindowsWithTitle with a MagicMock
    mock_table = MagicMock()
    mock_table.width = 800
    mock_table.height = 600
    with patch("pyautogui.getWindowsWithTitle", return_value=[mock_table]):
        table_config = TableConfiguration(mock_configuration_parser)
        table_config.configure_single_table("test_table_name")

        assert table_config._width == 800
        assert table_config._height == 600
        mock_table.activate.assert_called_once()


def test_configure_single_table_not_found(mock_configuration_parser):
    # Test for the case when the table is not found
    with patch("pyautogui.getWindowsWithTitle", return_value=[]):
        table_config = TableConfiguration(mock_configuration_parser)
        with pytest.raises(NoTableFound):
            table_config.configure_single_table("non_existent_table")


def test_load_settings(mock_configuration_parser):
    # Mock the ConfigurationParser's read_table_configuration method
    mock_table_settings = {
        "table_width": 800,
        "table_height": 600,
        "search_string": "test_search_string",
    }
    mock_configuration_parser.read_table_configuration.return_value = (
        mock_table_settings
    )

    table_config = TableConfiguration(mock_configuration_parser)
    table_config.load_settings()

    assert table_config._width == 800
    assert table_config._height == 600
    assert table_config.search_string == "test_search_string"


def test_save_settings(mock_configuration_parser):
    table_config = TableConfiguration(mock_configuration_parser)

    table_config._width = 800
    table_config._height = 600
    table_config.search_string = "test_search_string"

    table_config.save_settings()

    mock_configuration_parser.write_table_configuration.assert_called_once_with(
        table_height=600, table_width=800, search_string="test_search_string"
    )
