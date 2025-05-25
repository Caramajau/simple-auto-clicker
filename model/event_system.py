from typing import Callable, Final
from model.events import Events

class EventSystem:
    __listeners: Final[dict[Events, list[Callable[..., None]]]] = {}
    
    @classmethod
    def add_listener(cls, event_type: Events, listener: Callable[..., None]) -> None:
        """Add a listener to an event according to event_type"""
        if event_type not in cls.__listeners:
            cls.__listeners[event_type] = []
        cls.__listeners[event_type].append(listener)

    @classmethod
    def remove_listener(cls, event_type: Events, listener: Callable[..., None]) -> None:
        """Remove a listener to an event according to event_type"""
        if event_type in cls.__listeners:
            cls.__listeners[event_type].remove(listener)

    @classmethod
    def invoke_event(cls, event_type: Events, *args: object, **kwargs: object) -> None:
        """Call every listener added to event_type with given args and kwargs"""
        if event_type in cls.__listeners:
            for listener in cls.__listeners[event_type]:
                listener(*args, **kwargs)
