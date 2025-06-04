from typing import Final, Mapping

from keyboard import parse_hotkey
from model.json_handler import JSONHandler


class OptionHandler:
    TOGGLE_RECORDING_KEY: Final[str] = "toggleRecording"
    RECORD_MOUSE_POSITION_KEY: Final[str] = "recordMousePosition"
    CLEAR_RECORDED_POSITIONS_KEY: Final[str] = "clearRecordedPosition"
    START_KEY: Final[str] = "start"
    STOP_KEY: Final[str] = "stop"
    DELAY_KEY: Final[str] = "delay"
    EXIT_KEY: Final[str] = "exit"

    __DEFAULT_OPTIONS: Final[Mapping[str, str | float]] = {
        TOGGLE_RECORDING_KEY: "r",
        RECORD_MOUSE_POSITION_KEY: "g",
        CLEAR_RECORDED_POSITIONS_KEY: "c",
        START_KEY: "j",
        STOP_KEY: "k",
        EXIT_KEY: "esc",
        DELAY_KEY: 0.1,
    }

    def __init__(self, options_file_path: str = "data/options.json") -> None:
        json_handler: JSONHandler = JSONHandler(options_file_path)
        self.__options: Mapping[str, str | float] = json_handler.read_json()
        if len(self.__options) == 0:
            self.__options = OptionHandler.__DEFAULT_OPTIONS
            json_handler.write_json(OptionHandler.__DEFAULT_OPTIONS)

    def get_toggle_recording_key(self) -> str:
        return str(self.get_option_value(OptionHandler.TOGGLE_RECORDING_KEY))

    def get_record_mouse_position_key(self) -> str:
        return str(self.get_option_value(OptionHandler.RECORD_MOUSE_POSITION_KEY))

    def get_clear_recorded_positions_key(self) -> str:
        return str(self.get_option_value(OptionHandler.CLEAR_RECORDED_POSITIONS_KEY))

    def get_start_key(self) -> str:
        return str(self.get_option_value(OptionHandler.START_KEY))

    def get_exit_key(self) -> str:
        return str(self.get_option_value(OptionHandler.EXIT_KEY))

    def get_stop_key(self) -> str:
        return str(self.get_option_value(OptionHandler.STOP_KEY))

    def get_delay(self) -> float:
        return float(self.get_option_value(OptionHandler.DELAY_KEY))

    def get_option_value(self, option: str) -> str | float:
        try:
            selected_value: str | float = self.__options[option]
            if isinstance(selected_value, float):
                return selected_value

            selected_key: str = str(selected_value)
            return (
                selected_key
                if self.__is_valid_key(selected_key)
                else OptionHandler.__DEFAULT_OPTIONS[option]
            )
        except KeyError:
            return OptionHandler.__DEFAULT_OPTIONS[option]

    @staticmethod
    def __is_valid_key(key: str) -> bool:
        try:
            parse_hotkey(key)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_default_options() -> Mapping[str, str | float]:
        return OptionHandler.__DEFAULT_OPTIONS
