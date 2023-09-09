class KeyStates:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(KeyStates, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.left_button_pressed = False


key_states = KeyStates()
