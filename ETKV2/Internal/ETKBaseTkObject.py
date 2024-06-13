from __future__ import annotations
from tkinter import Event, EventType
from typing import TYPE_CHECKING, Any, Callable

from .ETKUtils import gen_col_from_int, get_abs_event_pos  # type:ignore

from ..Vector2d import Vector2d
from .ETKBaseObject import ETKBaseObject, ETKEvents

if TYPE_CHECKING:
    from ..ETKMainWindow import ETKMain


class ETKBaseTkObject(ETKBaseObject):
    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, visibility: bool, background_color: int, **kwargs: Any) -> None:
        self._tk_object: Any

        super().__init__(main=main, pos=pos, size=size, visibility=visibility, background_color=background_color, **kwargs)

        self._tk_object.configure(borderwidth=0)

    # region Methods

    def __del__(self) -> None:
        self.visibility = False

    def _update_background_color(self):
        self._tk_object.configure(background=gen_col_from_int(self.background_color))

    # region Eventhandling Methods

    def add_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        if event_type.value != "<Custom>":
            if len(self._event_lib[event_type]) == 0:
                self._tk_object.bind(
                    event_type.value, self._handle_tk_event)  # type:ignore
        super().add_event(event_type, eventhandler)

    def remove_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        super().remove_event(event_type, eventhandler)
        if event_type.value != "<Custom>":
            if len(self._event_lib[event_type]) == 0:
                self._tk_object.unbind(event_type.value)

    def _handle_tk_event(self, event: Event) -> None:  # type:ignore
        ev_data = tuple()
        match event.type:
            case EventType.ButtonPress:
                event_type = ETKEvents.MOUSE_DOWN
                ev_data = (event.state, event.num, get_abs_event_pos(event, self._main.root_tk_object))
            case EventType.ButtonRelease:
                event_type = ETKEvents.MOUSE_UP
                ev_data = (event.state, event.num, get_abs_event_pos(event, self._main.root_tk_object))
            case EventType.Enter:
                event_type = ETKEvents.ENTER
                ev_data = (event.focus, get_abs_event_pos(event, self._main.root_tk_object))
            case EventType.Leave:
                event_type = ETKEvents.LEAVE
                ev_data = (event.focus, get_abs_event_pos(event, self._main.root_tk_object))
            case EventType.Motion:
                event_type = ETKEvents.MOUSE_MOVED
                ev_data = (event.state, get_abs_event_pos(event, self._main.root_tk_object))
            case _:
                raise ValueError(f"invalid event {event}")

        self._handle_event(event_type, *ev_data)

    # endregion
    # endregion
