from services.layout.layout_manager import table_layout_manager
from services.tables.entities import AppName
from services.tables.table_config import table_configuration
from services.tables.table_manager import ProcessTracker
from services.tables.utilities import WindowsSelector

if __name__ == "__main__":
    process_tracker = ProcessTracker(
        table_layout_manager=table_layout_manager,
        table_configuration=table_configuration,
    )
    windows = WindowsSelector.get_windows_by_app_name(app_name=AppName.CHROME)
    filtered_windows = WindowsSelector.filter_windows_by_tab_title('SNG Tracker', windows)
    print(filtered_windows)

    # process_tracker.initialize_slots()
    # a = WindowsSelector.get_active_tab_title(app_name=AppName.CHROME, process_window=windows[0])
    # print(windows)
    # process_tracker.arrange_layout_on_start(windows=windows)
