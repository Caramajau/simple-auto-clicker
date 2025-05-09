from typing import Final
from model.json_handler import JSONHandler


class OptionHandler:
    # TODO: extract key names to avoid duplication.
    __DEFAULT_OPTIONS: Final[dict[str, str | float]] = {
        "toggleRecording": "r",
        "recordMousePosition": "g",
        "clearRecordedPosition": "c",
        "start": "j",
        "stop": "k",
        "delay": 0.1
    }

    def __init__(self, options_file_path: str = "data/options.json") -> None:
        json_handler: JSONHandler = JSONHandler(options_file_path)
        self.__options: dict[str, str | float] = json_handler.read_json()
        if len(self.__options) == 0:
            self.__options = OptionHandler.__DEFAULT_OPTIONS
            json_handler.write_json(OptionHandler.__DEFAULT_OPTIONS)
            
    def get_toggle_recording_key(self) -> str:
        return str(self.__options["toggleRecording"])
    
    def get_record_mouse_position_key(self) -> str:
        return str(self.__options["recordMousePosition"])

    def get_clear_recorded_positions_key(self) -> str:
        return str(self.__options["clearRecordedPosition"])

    def get_start_key(self) -> str:
        return str(self.__options["start"])
    
    def get_stop_key(self) -> str:
        return str(self.__options["stop"])
    
    def get_delay(self) -> float:
        return float(self.__options["delay"])

    @staticmethod
    def get_default_options() -> dict[str, str | float]:
        return OptionHandler.__DEFAULT_OPTIONS
