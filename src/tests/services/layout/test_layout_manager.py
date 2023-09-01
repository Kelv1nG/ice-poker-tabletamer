from unittest.mock import MagicMock

import pytest
from PyQt6 import QtCore

from services.layout.layout_manager import TableLayOutManager
from utils.configuration_parser import IConfigurationParser
from widgets.table_layout.main_table_template import MainTableTemplate
from widgets.table_layout.table_template import TableTemplate


@pytest.fixture
def mock_configuration_parser():
    # Fixture to create a mocked IConfigurationParser instance
    return MagicMock(spec=IConfigurationParser)


@pytest.fixture
def mock_table_template():
    # Fixture to create a mocked TableTemplate instance
    return MagicMock(spec=TableTemplate)


@pytest.fixture
def mock_main_table_template():
    return MagicMock(spec=MainTableTemplate)


def test_singleton_instance(mock_configuration_parser):
    table_layout_manager_1 = TableLayOutManager.get_instance(mock_configuration_parser)
    table_layout_manager_2 = TableLayOutManager.get_instance(mock_configuration_parser)

    assert table_layout_manager_1 is table_layout_manager_2


def test_table_settings(mock_configuration_parser):
    # Test table_settings property
    table_layout_manager = TableLayOutManager(mock_configuration_parser)
    mock_configuration_parser.read_table_configuration.return_value = {
        "table_height": 5,
        "table_width": 10,
    }

    assert table_layout_manager.table_settings == {"table_height": 5, "table_width": 10}


def test_layout_settings(mock_configuration_parser):
    # Test layout_settings property
    table_layout_manager = TableLayOutManager(mock_configuration_parser)
    mock_configuration_parser.read_layout_configuration.return_value = {
        "table_count": 2,
        "table_configurations": {"slot_1": {"top": 5, "left": 10}},
    }

    assert table_layout_manager.layout_settings == {
        "table_count": 2,
        "table_configurations": {"slot_1": {"top": 5, "left": 10}},
    }


def test_table_configurations(mock_configuration_parser):
    # Test table_configurations property
    table_layout_manager = TableLayOutManager(mock_configuration_parser)
    mock_configuration_parser.read_layout_configuration.return_value = {
        "table_configurations": {"slot_1": {"top": 5, "left": 10}},
    }

    assert table_layout_manager.table_configurations == {
        "slot_1": {"top": 5, "left": 10}
    }


def test_save_table_configuration(mock_configuration_parser, mock_table_template):
    # Test save_table_configuration method
    table_layout_manager = TableLayOutManager(mock_configuration_parser)
    table_layout_manager.table_templates = [mock_table_template]

    mock_table_template.geometry.return_value = QtCore.QRect(5, 10, 100, 50)

    table_layout_manager.save_table_configuration()

    mock_configuration_parser.write_layout_configuration.assert_called_once_with(
        table_configurations={"slot_1": {"top": 10, "left": 5}}
    )


def test_save_table_count(mock_configuration_parser):
    # Test save_table_count method
    table_layout_manager = TableLayOutManager(mock_configuration_parser)
    table_layout_manager.save_table_count(4)

    mock_configuration_parser.write_layout_configuration.assert_called_once_with(
        table_count=4
    )


# def test_show_templates(
#     mock_configuration_parser, mock_table_template, mock_main_table_template
# ):
#     # Set up the return value for the read_table_configuration method
#     mock_configuration_parser.read_table_configuration.return_value = {
#         "table_height": 100,
#         "table_width": 200,
#     }

#     # Set up the return value for the geometry method of mock_table_template
#     mock_table_template.geometry.return_value = QtCore.QRect(0, 0, 200, 100)

#     # Test show_templates method
#     table_layout_manager = TableLayOutManager(mock_configuration_parser)

#     mock_configuration_parser.read_layout_configuration.return_value = {
#         "table_count": 3,
#         "table_configurations": {
#             "slot_1": {"top": 5, "left": 10},
#             "slot_2": {"top": 30, "left": 20},
#             "slot_3": {"top": 50, "left": 40},
#         },
#     }

#     table_layout_manager.show_templates(mock_table_template, mock_main_table_template)

#     assert mock_table_template.setGeometry.call_args_list == [
#         ((10, 5, 200, 100),),
#         ((20, 30, 200, 100),),
#         ((40, 50, 200, 100),),
#     ]
