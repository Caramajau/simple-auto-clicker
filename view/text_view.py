from typing import Mapping
from model.event_system import EventSystem
from model.events import Events

class TextView():
    def __init__(self) -> None:
        EventSystem.add_listener(Events.PROGRAM_START, self.__handle_program_start)
        EventSystem.add_listener(Events.TOGGLE_RECORDING, self.__handle_toggle_recording)
        EventSystem.add_listener(Events.RECORD_MOUSE_CLICK, self.__handle_record_mouse_click)
        EventSystem.add_listener(Events.CLEAR_MOUSE_POSITIONS, self.__handle_clear_mouse_positions)
        EventSystem.add_listener(Events.START_MOUSE_CLICKING, self.__handle_start_mouse_clicking)
        EventSystem.add_listener(Events.STOP_MOUSE_CLICKING, self.__handle_stop_mouse_clicking)

    def __handle_program_start(self, toggle_recording_key: str, 
                               record_mouse_click_key: str, clear_positions_key: str, 
                               start_key: str, stop_key: str) -> None:
        control_keys: Mapping[str, str] = {
            "Toggle recording (enabled on start)": toggle_recording_key,
            "Record mouse position": record_mouse_click_key,
            "Clear recorded positions": clear_positions_key,
            "Start clicking recorded positions": start_key,
            "Stop clicking recorded positions": stop_key
        }
        max_length: int = max(len(key) for key in control_keys)
        
        print("The controls are:")
        for info_text, key_name in control_keys.items():
            print(f"{info_text.rjust(max_length)} - {key_name}")
        print("To exit the application press ESC or close the console window.")

    def __handle_toggle_recording(self, is_recording: bool) -> None:
        print("Recording enabled." if is_recording else "Recording disabled.")

    def __handle_record_mouse_click(self, position_to_add: tuple[int, int], all_positions: list[tuple[int, int]]) -> None:
        print(f"Added position: {position_to_add}")
        print(f"All recorded positions are now: {all_positions}")

    def __handle_clear_mouse_positions(self) -> None:
        print("Mouse positions cleared.")

    def __handle_start_mouse_clicking(self, all_positions: list[tuple[int, int]]) -> None:
        print("Started clicking recorded positions:")
        for position in all_positions:
            print(position)

    def __handle_stop_mouse_clicking(self, start_key: str) -> None:
        print(f"Stopped clicking recorded positions, press {start_key} to start the clicking again.")
