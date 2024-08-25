from typing import Callable
from model.events import Events

class EventSystem:
    __listeners: dict[Events, list[Callable]] = {}
    
    @classmethod
    def add_listener(cls, event_type: Events, listener: Callable) -> None:
        if event_type not in cls.__listeners:
            cls.__listeners[event_type] = []
        cls.__listeners[event_type].append(listener)

    @classmethod
    def remove_listener(cls, event_type: Events, listener: Callable) -> None:
        if event_type in cls.__listeners:
            cls.__listeners[event_type].remove(listener)

    @classmethod
    def dispatch(cls, event_type: Events, *args, **kwargs) -> None:
        if event_type in cls.__listeners:
            for listener in cls.__listeners[event_type]:
                listener(*args, **kwargs)
