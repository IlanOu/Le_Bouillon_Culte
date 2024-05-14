from enum import Enum

class StateJoystick(Enum):
    UP = 1
    DOWN = 2

class Joystick:

    _current_state = StateJoystick.UP

    @staticmethod
    def get_current_state():
        return Joystick._current_state

    @staticmethod
    def set_current_state(new_state):
        Joystick._current_state = new_state
        

