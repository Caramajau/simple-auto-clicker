from pyautogui import moveTo, click, position, Point
from time import sleep
import keyboard
from threading import Thread, Event

class MouseHandler:
    def __init__(self) -> None:
        self.__is_recording: bool = False
        self.__recorded_positions: list[Point] = []
        self.__stop_event: Event = Event()

        keyboard.on_press_key("r", self.__toggle_recording)
        keyboard.on_press_key("e", self.__record_mouse_position)
        keyboard.on_press_key("a", self.__on_start_press)
        keyboard.on_press_key("s", self.__on_stop_press)
        keyboard.on_press_key("d", self.__on_reset_press)

        keyboard.wait("esc")

    def __toggle_recording(self, event: keyboard.KeyboardEvent) -> None:
        print("Toggled recording.")
        self.__is_recording = not self.__is_recording
    
    def __record_mouse_position(self, event:keyboard.KeyboardEvent) -> None:
        point_to_add: Point = position()
        print(f"Point to add: {point_to_add}")
        self.__recorded_positions.append(point_to_add)
        print(f"All points: {self.__recorded_positions}")

    def __click_recorded_mouse_positions(self) -> None:
        """Click continuously recorded mouse positions until the stop event is set."""
        while not self.__stop_event.is_set():
            for position in self.__recorded_positions:
                moveTo(position)
                click()

    def __on_start_press(self, event: keyboard.KeyboardEvent) -> None:
        """Starts the continuous mouse clicking in a separate thread."""
        if not self.__stop_event.is_set():
            print("Start key pressed. Beginning action...")
            # Ensure the event is cleared
            self.__stop_event.clear()  
            action_thread = Thread(target=self.__click_recorded_mouse_positions)
            action_thread.start()

    def __on_stop_press(self, event: keyboard.KeyboardEvent) -> None:
        """Stops the continuous mouse clicking."""
        print("Stop key pressed. Stopping action...")
        self.__stop_event.set() 

    def __on_reset_press(self, event: keyboard.KeyboardEvent) -> None:
        """Resets the stop event."""
        print("Reset key pressed. Reseting action...")
        self.__stop_event.clear()
