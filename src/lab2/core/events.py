from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Type


class EventArgs(ABC):
    pass


class Event:
    def __init__(self):
        self._handlers: List[Callable[[Any, EventArgs], None]] = []

    def subscribe(self, handler: Callable[[Any, EventArgs], None]):
        if handler not in self._handlers:
            self._handlers.append(handler)

    def unsubscribe(self, handler: Callable[[Any, EventArgs], None]):
        if handler in self._handlers:
            self._handlers.remove(handler)

    def emit(self, sender: Any, args: EventArgs):
        for handler in self._handlers:
            handler(sender, args)


class AnimalEventArgs(EventArgs):
    def __init__(self, animal: Any, message: str):
        self.animal = animal
        self.message = message


class HungerEventArgs(AnimalEventArgs):
    pass


class DeathEventArgs(AnimalEventArgs):
    pass


class HappyEventArgs(AnimalEventArgs):
    pass
