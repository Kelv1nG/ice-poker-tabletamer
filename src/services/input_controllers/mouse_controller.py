import pyautogui as pa


class MouseController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MouseController, cls).__new__(cls)
        return cls._instance

    def get_mouse_coordinates(self):
        return pa.position()


mouse_controller = MouseController()
