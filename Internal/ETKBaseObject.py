from __future__ import annotations
from abc import abstractmethod

from .ETKUtils import exec_event_callback

from .SubclassableEnum import SubclassableEnum
from typing import TYPE_CHECKING, Any, Callable

from ..Vector2d import Vector2d

if TYPE_CHECKING:
    from .ETKMain import ETKMain
    from .ETKEventData import ETKEventData


class ETKEvents(SubclassableEnum):
    MOUSE_DOWN: ETKEvents
    MOUSE_UP: ETKEvents
    ENTER: ETKEvents
    LEAVE: ETKEvents
    MOUSE_MOVED: ETKEvents
    _values = {"MOUSE_DOWN": "<ButtonPress>", "MOUSE_UP": "<ButtonRelease>", "ENTER": "<Enter>", "LEAVE": "<Leave>", "MOUSE_MOVED": "<Motion>"}


class ETKBaseObject:
    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, visibility: bool, background_color: int) -> None:
        self._pos: Vector2d = Vector2d() if pos != Vector2d() else Vector2d(1)
        self._size: Vector2d = Vector2d() if size != Vector2d() else Vector2d(1)
        self.__background_color: int = 0 if background_color != 0 else 1
        self.__visibility: bool = not visibility
        self._main = main
        self._event_lib: dict[ETKEvents, list[Callable[[], Any] | Callable[[ETKEventData], Any]]] = {e: [] for e in ETKEvents}

        self.background_color = background_color
        self.pos = pos
        self.size = size
        self.visibility = visibility

    # region Properties

    @property
    def pos(self) -> Vector2d:
        return self._pos.copy()

    @pos.setter
    def pos(self, value: Vector2d) -> None:
        if self._pos == value:
            return
        self._pos = value
        self._main.scheduler.schedule_action(self._update_pos)


    @property
    def abs_pos(self) -> Vector2d:
        """READ-ONLY"""
        return self._pos.copy()

    @property
    def size(self) -> Vector2d:
        return self._size.copy()

    @size.setter
    def size(self, value: Vector2d) -> None:
        if self._size == value:
            return
        self._size = value
        self._main.scheduler.schedule_action(self._update_size)

    @property
    def visibility(self) -> bool:
        return self.__visibility

    @visibility.setter
    def visibility(self, value: bool) -> None:
        if self.__visibility == value:
            return
        self.__visibility = value
        self._main.scheduler.schedule_action(self._update_visibility)

    @property
    def abs_visibility(self) -> bool:
        """READ-ONLY"""
        return self.__visibility

    @property
    def background_color(self) -> int:
        return self.__background_color

    @background_color.setter
    def background_color(self, value: int) -> None:
        if self.__background_color == value:
            return
        self.__background_color = value
        self._main.scheduler.schedule_action(self._update_background_color)

    @property
    def events(self) -> dict[ETKEvents, list[Callable[..., Any]]]:
        """READ-ONLY"""
        return self._event_lib.copy()

    # endregion
    # region Methods

    @abstractmethod
    def _update_pos(self) -> bool:
        pass

    @abstractmethod
    def _update_size(self) -> bool:
        pass

    @abstractmethod
    def _update_visibility(self) -> bool:
        pass

    @abstractmethod
    def _update_background_color(self):
        pass

    # region Eventhandling Methods

    def add_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[ETKEventData], None]) -> None:
        self._event_lib[event_type].append(eventhandler)

    def remove_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[ETKEventData], None]) -> None:
        self._event_lib[event_type].remove(eventhandler)

    def _handle_event(self, event_data: ETKEventData, ignore_scheduler: bool = False) -> None:
        for c in self._event_lib[event_data.event]:
            if ignore_scheduler:
                exec_event_callback(c, event_data)
                continue
            self._main.scheduler.schedule_event(c, event_data)

    # endregion
    # endregion