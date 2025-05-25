from typing import Final, Mapping
from model.json_handler import JSONHandler


class OptionHandler:
    TOGGLE_RECORDING_KEY: Final[str] = "toggleRecording"
    RECORD_MOUSE_POSITION_KEY: Final[str] = "recordMousePosition"
    CLEAR_RECORDED_POSITIONS_KEY: Final[str] = "clearRecordedPosition"
    START_KEY: Final[str] = "start"
    STOP_KEY: Final[str] = "stop"
    DELAY_KEY: Final[str] = "delay"

    __DEFAULT_OPTIONS: Final[Mapping[str, str | float]] = {
        TOGGLE_RECORDING_KEY: "r",
        RECORD_MOUSE_POSITION_KEY: "g",
        CLEAR_RECORDED_POSITIONS_KEY: "c",
        START_KEY: "j",
        STOP_KEY: "k",
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

    def get_stop_key(self) -> str:
        return str(self.get_option_value(OptionHandler.STOP_KEY))

    def get_delay(self) -> float:
        return float(self.get_option_value(OptionHandler.DELAY_KEY))

    def get_option_value(self, option: str) -> str | float:
        try:
            return self.__options[option]
        except KeyError:
            return OptionHandler.__DEFAULT_OPTIONS[option]

    @staticmethod
    def get_default_options() -> Mapping[str, str | float]:
        return OptionHandler.__DEFAULT_OPTIONS
