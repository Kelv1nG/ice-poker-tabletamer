import pyautogui


class ConfigureTable:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.top = 0
        self.left = 0
        self.table = None

    def configure_single_table(self, table_name: str):
        """
        table_name: application name to be grabbed
        """
        self.table = pyautogui.getWindowsWithTitle(table_name)[0]
        self.width = self.table.width
        self.height = self.table.height


def get_all_tables(table_name: str):
    """
    table_name: application name to be grabbed
    """
    return pyautogui.getWindowsWithTitle(table_name)


config_table = ConfigureTable()
config_table.configure_single_table("SNG Tracker")
print(config_table.table)
print(config_table.width)
print(config_table.height)
