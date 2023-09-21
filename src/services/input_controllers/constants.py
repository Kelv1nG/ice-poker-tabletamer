from pynput import mouse
import win32con

BTN_X1_MOUSE_DATA = 65536
BTN_X2_MOUSE_DATA = 131072
BTN_X_PRESS = 523

SUPPRESSED_EVENTS = [
    mouse.Listener.WM_XBUTTONDOWN,
    mouse.Listener.WM_XBUTTONUP,

    mouse.Listener.WM_MBUTTONDOWN,
    mouse.Listener.WM_MBUTTONUP,

    mouse.Listener.WM_RBUTTONDOWN,
    mouse.Listener.WM_RBUTTONUP,

    mouse.Listener.WM_MBUTTONDOWN,
    mouse.Listener.WM_MBUTTONUP
]

# to be used for event_filtering / suppressing in pynput
MOUSE_MESSAGE_DATA_TO_BUTTON_MAP = {
    (BTN_X_PRESS, BTN_X1_MOUSE_DATA): 'Button.x1', # msg press, data.mousedata
    (BTN_X_PRESS, BTN_X2_MOUSE_DATA): 'Button.x2',
    (win32con.WM_RBUTTONDOWN, 0): 'Button.right',
    (win32con.WM_MBUTTONDOWN, 0): 'Button.middle'
}
