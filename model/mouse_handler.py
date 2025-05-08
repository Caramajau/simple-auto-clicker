from win32api import GetCursorPos, SetCursorPos, mouse_event # type: ignore
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
from keyboard import on_press_key, wait, KeyboardEvent
from threading import Thread, Event
from model.event_system import EventSystem
from model.events import Events
from time import sleep

class MouseHandler:
    def __init__(self) -> None:
        self.__is_recording: bool = False
        self.__recorded_positions: list[tuple[int, int]] = []
        self.__start_click_event: Event = Event()
        self.__clicking_event: Event = Event()

        self.__toggle_recording_key: str = "r"
        self.__record_mouse_position_key: str = "g"
        self.__clear_recorded_positions_key: str = "c"
        self.__start_key: str = "j"
        self.__stop_key: str = "k"
        self.__reset_key: str = "l"

        on_press_key(self.__toggle_recording_key, self.__toggle_recording)
        on_press_key(self.__record_mouse_position_key, self.__record_mouse_position)
        on_press_key(self.__clear_recorded_positions_key, self.__clear_recorded_mouse_positions)
        on_press_key(self.__start_key, self.__start_mouse_clicking)
        on_press_key(self.__stop_key, self.__stop_mouse_clicking)
        on_press_key(self.__reset_key, self.__reset_stop_event)

        EventSystem.invoke_event(Events.PROGRAM_START, self.__toggle_recording_key, 
                                 self.__record_mouse_position_key, self.__clear_recorded_positions_key,
                                 self.__start_key, self.__stop_key, self.__reset_key)

        wait("esc")

    def __toggle_recording(self, _: KeyboardEvent) -> None:
        """Toggle whether mouse clicks are being recorded."""
        self.__is_recording = not self.__is_recording
        EventSystem.invoke_event(Events.TOGGLE_RECORDING)
    
    def __record_mouse_position(self, _: KeyboardEvent) -> None:
        """Add current mouse position to recorded positions."""
        if self.__is_recording:
            point_to_add: tuple[int, int] = GetCursorPos()
            self.__recorded_positions.append(point_to_add)
            EventSystem.invoke_event(Events.RECORD_MOUSE_CLICK, point_to_add, self.__recorded_positions)

    def __clear_recorded_mouse_positions(self, _: KeyboardEvent) -> None:
        """Clear the recorded positions."""
        self.__recorded_positions.clear()
        EventSystem.invoke_event(Events.CLEAR_MOUSE_POSITIONS)

    def __click_recorded_mouse_positions(self) -> None:
        """Click continuously recorded mouse positions until the stop event is set."""
        while not self.__clicking_event.is_set():
            for position in self.__recorded_positions:
                SetCursorPos(position)
                self.__click()

        self.__start_click_event.clear()

    @staticmethod
    def __click(delay: float = 0.1) -> None:
        """Click the screen where the mouse pointer is and then cause a delay"""
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)
        sleep(delay)

    def __start_mouse_clicking(self, _: KeyboardEvent) -> None:
        """Start the continuous mouse clicking in a separate thread."""
        if not self.__start_click_event.is_set():
            self.__start_click_event.set()
             # Ensure the event is cleared
            self.__clicking_event.clear()
            action_thread = Thread(target=self.__click_recorded_mouse_positions)
            action_thread.start()
            EventSystem.invoke_event(Events.START_MOUSE_CLICKING, self.__recorded_positions)

    def __stop_mouse_clicking(self, _: KeyboardEvent) -> None:
        """Stop the continuous mouse clicking."""
        self.__clicking_event.set() 
        EventSystem.invoke_event(Events.STOP_MOUSE_CLICKING, self.__reset_key, self.__start_key)

    def __reset_stop_event(self, _: KeyboardEvent) -> None:
        """Reset the stop event."""
        # self.__start_lock.clear()
        EventSystem.invoke_event(Events.RESET_STOP_EVENT)
