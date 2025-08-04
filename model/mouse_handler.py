from threading import Event, Thread
from time import sleep

from keyboard import KeyboardEvent, on_press_key, wait
from win32api import GetCursorPos, SetCursorPos, mouse_event  # type: ignore
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP

from model.event_system import EventSystem
from model.events import Events
from model.option_handler import OptionHandler


class MouseHandler:
    def __init__(self) -> None:
        self.__is_recording: bool = True
        self.__recorded_positions: list[tuple[int, int]] = []
        self.__start_click_event: Event = Event()
        self.__clicking_event: Event = Event()

        self.__option_handler: OptionHandler = OptionHandler()

        on_press_key(
            self.__option_handler.get_toggle_recording_key(),
            self.__toggle_recording,
        )
        on_press_key(
            self.__option_handler.get_record_mouse_position_key(),
            self.__record_mouse_position,
        )
        on_press_key(
            self.__option_handler.get_clear_recorded_positions_key(),
            self.__clear_recorded_mouse_positions,
        )
        on_press_key(self.__option_handler.get_start_key(), self.__start_mouse_clicking)
        on_press_key(self.__option_handler.get_stop_key(), self.__stop_mouse_clicking)

        EventSystem.invoke_event(
            Events.PROGRAM_START,
            self.__option_handler.get_toggle_recording_key(),
            self.__option_handler.get_record_mouse_position_key(),
            self.__option_handler.get_clear_recorded_positions_key(),
            self.__option_handler.get_start_key(),
            self.__option_handler.get_stop_key(),
            self.__option_handler.get_exit_key(),
        )

        wait(self.__option_handler.get_exit_key())

    def __toggle_recording(self, _: KeyboardEvent) -> None:
        """Toggle whether mouse clicks are being recorded."""
        self.__is_recording = not self.__is_recording
        EventSystem.invoke_event(Events.TOGGLE_RECORDING, self.__is_recording)

    def __record_mouse_position(self, _: KeyboardEvent) -> None:
        """Add current mouse position to recorded positions."""
        if self.__is_recording:
            point_to_add: tuple[int, int] = GetCursorPos()
            self.__recorded_positions.append(point_to_add)
            EventSystem.invoke_event(
                Events.RECORD_MOUSE_CLICK, point_to_add, self.__recorded_positions
            )

    def __clear_recorded_mouse_positions(self, _: KeyboardEvent) -> None:
        """Clear the recorded positions."""
        self.__recorded_positions.clear()
        EventSystem.invoke_event(Events.CLEAR_MOUSE_POSITIONS)

    def __click_recorded_mouse_positions(self) -> None:
        """Click continuously recorded mouse positions until the stop event is set."""
        while not self.__clicking_event.is_set():
            for position in self.__recorded_positions:
                SetCursorPos(position)
                self.__click(self.__option_handler.get_delay())

        self.__start_click_event.clear()

    @staticmethod
    def __click(delay: float) -> None:
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
            EventSystem.invoke_event(
                Events.START_MOUSE_CLICKING, self.__recorded_positions
            )

    def __stop_mouse_clicking(self, _: KeyboardEvent) -> None:
        """Stop the continuous mouse clicking."""
        self.__clicking_event.set()
        EventSystem.invoke_event(
            Events.STOP_MOUSE_CLICKING, self.__option_handler.get_start_key()
        )
