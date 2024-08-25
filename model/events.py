from enum import Enum, unique, auto

# Events and not Event to not conflict with threading's Event.
@unique
class Events(Enum):
    TOGGLE_RECORDING = auto()
    RECORD_MOUSE_CLICK = auto()
    CLICK_RECORDED_MOUSE_POSITIONS = auto()
    CLEAR_MOUSE_POSITIONS = auto()
    START_MOUSE_CLICKING = auto()
    STOP_MOUSE_CLICKING = auto()
    RESET_STOP_EVENT = auto()
