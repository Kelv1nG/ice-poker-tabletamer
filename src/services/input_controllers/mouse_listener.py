from pynput import mouse

from .entities import key_states


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        key_states.left_button_pressed = pressed


mouse_listener = mouse.Listener(on_click=on_click)
