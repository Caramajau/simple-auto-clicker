from pyautogui import moveTo, click, position, Point
import keyboard
from threading import Thread, Event
from model.event_system import EventSystem
from model.events import Events

class MouseHandler:
    def __init__(self) -> None:
        self.__is_recording: bool = False
        self.__recorded_positions: list[Point] = []
        self.__stop_event: Event = Event()

        self.__start_key: str = "a"
        self.__reset_key: str = "d"

        keyboard.on_press_key("r", self.__toggle_recording)
        keyboard.on_press_key("e", self.__record_mouse_position)
        keyboard.on_press_key("w", self.__clear_recorded_mouse_positions)
        keyboard.on_press_key(self.__start_key, self.__start_mouse_clicking)
        keyboard.on_press_key("s", self.__stop_mouse_clicking)
        keyboard.on_press_key(self.__reset_key, self.__reset_stop_event)

        keyboard.wait("esc")

    def __toggle_recording(self, _: keyboard.KeyboardEvent) -> None:
        """Toggles whether mouse clicks are being recorded."""
        self.__is_recording = not self.__is_recording
        EventSystem.invoke_event(Events.TOGGLE_RECORDING)
    
    def __record_mouse_position(self, _: keyboard.KeyboardEvent) -> None:
        """Adds current mouse position to recorded positions."""
        point_to_add: Point = position()
        self.__recorded_positions.append(point_to_add)
        EventSystem.invoke_event(Events.RECORD_MOUSE_CLICK, point_to_add, self.__recorded_positions)

    def __clear_recorded_mouse_positions(self, _: keyboard.KeyboardEvent) -> None:
        """Clear the recorded positions."""
        self.__recorded_positions.clear()
        EventSystem.invoke_event(Events.CLEAR_MOUSE_POSITIONS)

    def __click_recorded_mouse_positions(self) -> None:
        """Click continuously recorded mouse positions until the stop event is set."""
        while not self.__stop_event.is_set():
            for position in self.__recorded_positions:
                moveTo(position)
                click()

    def __start_mouse_clicking(self, _: keyboard.KeyboardEvent) -> None:
        """Start the continuous mouse clicking in a separate thread."""
        if not self.__stop_event.is_set():
            # Ensure the event is cleared
            self.__stop_event.clear()  
            action_thread = Thread(target=self.__click_recorded_mouse_positions)
            action_thread.start()
            EventSystem.invoke_event(Events.START_MOUSE_CLICKING, self.__recorded_positions)

    def __stop_mouse_clicking(self, _: keyboard.KeyboardEvent) -> None:
        """Stop the continuous mouse clicking."""
        self.__stop_event.set() 
        EventSystem.invoke_event(Events.STOP_MOUSE_CLICKING, self.__reset_key, self.__start_key)

    def __reset_stop_event(self, _: keyboard.KeyboardEvent) -> None:
        """Reset the stop event."""
        self.__stop_event.clear()
        EventSystem.invoke_event(Events.RESET_STOP_EVENT)
