import pyautogui as pa

pa.PAUSE = 0.01


class MouseController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MouseController, cls).__new__(cls)
        return cls._instance

    def get_mouse_coordinates(self):
        return pa.position()

    def left_click(self) -> None:
        pa.click()

    def move_to_coordinates(self, x: int, y: int) -> None:
        pa.moveTo(x, y)


mouse_controller = MouseController()
