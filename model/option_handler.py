from typing import Final
from model.json_handler import JSONHandler


class OptionHandler:
    __TOGGLE_RECORDING_KEY: Final[str] = "toggleRecording"
    __RECORD_MOUSE_POSITION_KEY: Final[str] = "recordMousePosition"
    __CLEAR_RECORDED_POSITIONS_KEY: Final[str] = "clearRecordedPosition"
    __START_KEY: Final[str] = "start"
    __STOP_KEY: Final[str] = "stop"
    __DELAY_KEY: Final[str] = "delay"

    __DEFAULT_OPTIONS: Final[dict[str, str | float]] = {
        __TOGGLE_RECORDING_KEY: "r",
        __RECORD_MOUSE_POSITION_KEY: "g",
        __CLEAR_RECORDED_POSITIONS_KEY: "c",
        __START_KEY: "j",
        __STOP_KEY: "k",
        __DELAY_KEY: 0.1
    }

    def __init__(self, options_file_path: str = "data/options.json") -> None:
        json_handler: JSONHandler = JSONHandler(options_file_path)
        self.__options: dict[str, str | float] = json_handler.read_json()
        if len(self.__options) == 0:
            self.__options = OptionHandler.__DEFAULT_OPTIONS
            json_handler.write_json(OptionHandler.__DEFAULT_OPTIONS)

    def get_toggle_recording_key(self) -> str:
        return str(self.__options[OptionHandler.__TOGGLE_RECORDING_KEY])

    def get_record_mouse_position_key(self) -> str:
        return str(self.__options[OptionHandler.__RECORD_MOUSE_POSITION_KEY])

    def get_clear_recorded_positions_key(self) -> str:
        return str(self.__options[OptionHandler.__CLEAR_RECORDED_POSITIONS_KEY])

    def get_start_key(self) -> str:
        return str(self.__options[OptionHandler.__START_KEY])

    def get_stop_key(self) -> str:
        return str(self.__options[OptionHandler.__STOP_KEY])

    def get_delay(self) -> float:
        return float(self.__options[OptionHandler.__DELAY_KEY])

    @staticmethod
    def get_default_options() -> dict[str, str | float]:
        return OptionHandler.__DEFAULT_OPTIONS
