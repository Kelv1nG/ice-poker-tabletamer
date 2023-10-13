import pygetwindow as gw

from services.tables.entities import AppName


class WindowsSelector:
    @staticmethod
    def get_windows_by_app_name(app_name: AppName) -> list[gw.Window] | None:
        return gw.getWindowsWithTitle(app_name.value)

    @staticmethod
    def get_active_tab_title(app_name: AppName, process_window: gw.Window) -> str:
        match app_name.value:
            case AppName.CHROME.value:
                return process_window.title.split(" - Google Chrome")[0]
            case AppName.FIREFOX.value:
                return process_window.title

    @staticmethod
    def filter_windows_by_tab_title(
        tab_title: str, process_windows: list[gw.Window]
    ) -> list[gw.Window]:
        return [
            window
            for window in process_windows
            if tab_title
            in WindowsSelector.get_active_tab_title(
                app_name=AppName.CHROME, process_window=window
            )
        ]

    @staticmethod
    def get_center_for_windows(
        windows: list[gw.Window],
    ) -> list[tuple[int, int, gw.Window]]:
        center_coordinates = []
        for window in windows:
            value = (window.centery, window.centerx, window)
            center_coordinates.append(value)
        return center_coordinates

    @staticmethod
    def get_active_window() -> gw.Window:
        return gw.getActiveWindow()
