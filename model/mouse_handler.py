from pyautogui import moveTo, click, position, Point
from time import sleep
import keyboard
from threading import Thread, Event

class MouseHandler:
    def __init__(self) -> None:
        self.__recorded_positions: list[Point] = []
        self.__stop_event: Event = Event()

        keyboard.on_press_key("r", self.__on_start_press)
        keyboard.on_press_key("s", self.__on_stop_press)
        keyboard.on_press_key("c", self.__on_reset_press)
        keyboard.wait("esc")

    def __do_something(self) -> None:
        """Performs a continuous action until the stop event is set."""
        while not self.__stop_event.is_set():
            # Perform the action (e.g., printing a message)
            print("Doing something...")
            sleep(0.5)

    def __on_start_press(self, event: keyboard.KeyboardEvent) -> None:
        """Starts the continuous action in a separate thread."""
        if not self.__stop_event.is_set():
            print("Start key pressed. Beginning action...")
            # Ensure the event is cleared
            self.__stop_event.clear()  
            action_thread = Thread(target=self.__do_something)
            action_thread.start()

    def __on_stop_press(self, event: keyboard.KeyboardEvent) -> None:
        """Stops the continuous action."""
        print("Stop key pressed. Stopping action...")
        self.__stop_event.set() 

    def __on_reset_press(self, event: keyboard.KeyboardEvent) -> None:
        """Resets the stop event."""
        print("Reset key pressed. Reseting action...")
        self.__stop_event.clear()
