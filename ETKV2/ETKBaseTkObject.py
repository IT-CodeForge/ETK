from tkinter import Event, EventType
from typing import Any, Callable, Final, Optional

from .vector2d import vector2d
from .ETKBaseObject import ETKBaseObject, Events, BaseEvents
from .ETKUtils import gen_col_from_int


class ETKBaseTkObject(ETKBaseObject):
    _TK_EVENTTYPE_TRANSLATION: Final = {
        EventType.KeyPress: "<KeyPress>",
        EventType.KeyRelease: "<KeyRelease>",
        EventType.ButtonPress: "<ButtonPress>",
        EventType.ButtonRelease: "<ButtonRelease>",
        EventType.Motion: "<Motion>",
        EventType.Enter: "<Enter>",
        EventType.Leave: "<Leave>",
        EventType.Configure: "<Configure>"
    }  # NOTE!!!!

    def __init__(self, pos: vector2d, size: vector2d, background_color: int = 0xAAAAAA) -> None:
        ETKBaseObject.__init__(self, pos, size)
        self._tk_object: Any
        self.background_color = background_color

    @property
    def background_color(self) -> int:
        return int(self._background_color[1:], 16)

    @background_color.setter
    def background_color(self, value: Optional[int]) -> None:
        self._background_color = gen_col_from_int(value)
        self._tk_object.configure(background=self._background_color)

    def add_event(self, event_type: Events, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, Events, Any]], None]):
        if len(self._event_lib[event_type]) == 0:
            self._tk_object.bind(
                event_type.value, self._handle_tk_event)  # type:ignore
        ETKBaseObject.add_event(self, event_type, eventhandler)

    def remove_event(self, event_type: Events, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, Events, Any]], None]):
        if len(self._event_lib[event_type]) == 0:
            self._tk_object.unbind(event_type.value)
        ETKBaseObject.remove_event(self, event_type, eventhandler)

    def _handle_tk_event(self, event: Event) -> None:  # type:ignore
        match self._TK_EVENTTYPE_TRANSLATION[event.type]:
            case "<ButtonPress>":
                event_type = BaseEvents.MOUSE_DOWN
            case "<ButtonRelease>":
                event_type = BaseEvents.MOUSE_UP
            case "<Enter>":
                event_type = BaseEvents.ENTER
            case "<Leave>":
                event_type = BaseEvents.LEAVE
            case _:
                raise ValueError(f"invalid event {event}")

        self._handle_event(event_type, event)  # type:ignore
