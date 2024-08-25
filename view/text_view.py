from model.event_system import EventSystem
from model.events import Events
from pyautogui import Point

class TextView():
    def __init__(self) -> None:
        EventSystem.add_listener(Events.TOGGLE_RECORDING, self.__handle_toggle_recording)
        EventSystem.add_listener(Events.RECORD_MOUSE_CLICK, self.__handle_record_mouse_click)
        EventSystem.add_listener(Events.CLEAR_MOUSE_POSITIONS, self.__handle_clear_mouse_positions)
        EventSystem.add_listener(Events.START_MOUSE_CLICKING, self.__handle_start_mouse_clicking)
        EventSystem.add_listener(Events.STOP_MOUSE_CLICKING, self.__handle_stop_mouse_clicking)
        EventSystem.add_listener(Events.RESET_STOP_EVENT, self.__handle_reset_stop_event)

    def __handle_toggle_recording(self) -> None:
        print("Toggled recording.")

    def __handle_record_mouse_click(self, position_to_add: Point, all_positions: list[Point]) -> None:
        print(f"Added position: {position_to_add}")
        print(f"All recorded positions are now: {all_positions}")

    def __handle_clear_mouse_positions(self) -> None:
        print("Mouse positions cleared.")

    def __handle_start_mouse_clicking(self, all_positions: list[Point]) -> None:
        print("Started clicking recorded positions:")
        for position in all_positions:
            print(position)

    def __handle_stop_mouse_clicking(self, reset_key: str, start_key: str) -> None:
        print(f"Stopped clicking recorded positions, press {reset_key} and then {start_key} to start the clicking again.")

    def __handle_reset_stop_event(self) -> None:
        print("Mouse clicking can now be started again.")
