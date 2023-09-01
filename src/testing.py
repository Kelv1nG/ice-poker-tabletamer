from services.layout.layout_manager import table_layout_manager
from services.tables.table_manager import table_configuration
from services.tables.table_tracker import ProcessTracker
from services.tables.utilities import WindowsSelector
from services.tables.entities import AppName

if __name__ == "__main__":
    process_tracker = ProcessTracker(
        table_layout_manager=table_layout_manager,
        table_configuration=table_configuration,
    )
    windows = WindowsSelector.get_windows_by_app_name(app_name=AppName.CHROME)
    process_tracker.initialize_slots()
    a = WindowsSelector.get_active_tab_title(app_name=AppName.CHROME, process_window=windows[0])
    process_tracker.arrange_layout_on_start(windows=windows)
