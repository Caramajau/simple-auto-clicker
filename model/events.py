from enum import Enum, auto, unique


# Events and not Event to not conflict with threading's Event.
@unique
class Events(Enum):
    PROGRAM_START = auto()
    TOGGLE_RECORDING = auto()
    RECORD_MOUSE_CLICK = auto()
    CLEAR_MOUSE_POSITIONS = auto()
    START_MOUSE_CLICKING = auto()
    STOP_MOUSE_CLICKING = auto()
