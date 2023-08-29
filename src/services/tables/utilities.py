
import pygetwindow as gw
import enum


class AppName(enum.Enum):
    FIREFOX = "Mozilla Firefox"
    CHROME = "Google Chrome"


class WindowsSelector:
    @staticmethod
    def get_windows_by_title(title: str) -> list[gw.Window] | None:
        return gw.getWindowsWithTitle(title)

    @staticmethod
    def get_active_tab_title(app_name: str, process_window: gw.Window) -> str | None:
        def get_tab_title(process_window: gw.Window, app_name: str):
            match app_name:
                case AppName.CHROME.value:
                    return process_window.title.split(" - Google Chrome")[0]
                case AppName.FIREFOX.value:
                    return process_window.title

        if process_window:
            active_tab_title = get_tab_title(process_window, app_name)
            return active_tab_title
        return None

    @staticmethod
    def get_center_for_windows(
        windows: list[gw.Window],
    ) -> list[tuple[int, int, gw.Window]]:
        center_coordinates = []
        for window in windows:
            value = (window.centery, window.centerx, window)
            center_coordinates.append(value)
        return center_coordinates
