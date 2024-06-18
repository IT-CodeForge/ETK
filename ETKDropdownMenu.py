from __future__ import annotations

from typing import Any

from .Internal.ETKEventData import ETKEventData

from .Internal.ETKMain import ETKMain
from .Vector2d import Vector2d
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from tkinter import OptionMenu, StringVar
from tkinter import _setit  # type:ignore


class ETKDropdownMenu(ETKBaseTkWidgetDisableable):
    class EVENTS(ETKBaseTkWidgetDisableable.EVENTS):
        CHANGED: ETKDropdownMenu.EVENTS
        _values = {"CHANGED": "<Custom>"}

    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: Vector2d = Vector2d(70, 18), options: list[str] = [], start_value: str = "", *, visibility: bool = True, enabled: bool = True, background_color: int = 0xEEEEEE, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__selected_var = StringVar(value=start_value)
        self.__selected = start_value
        if len(options) == 0:
            options = [""]
        self.__options = options
        self._tk_object = OptionMenu(main.root_tk_object, self.__selected_var, *options)
        self.__ignore_next_change_event = False

        super().__init__(main=main, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

        self.__selected_var.trace("w", self.__clicked_changed)  # type:ignore
        self._event_lib.update({e: [] for e in self.EVENTS if e not in self._event_lib.keys()})

    @property
    def options(self) -> list[str]:
        return self.__options

    @options.setter
    def options(self, value: list[str]) -> None:
        if self.__options == value:
            return
        if len(value) == 0:
            value = [""]
        self.__options = value
        self._main.scheduler.schedule_action(self.__update_options)

    @property
    def selected(self) -> str:
        return self.__selected_var.get()

    @selected.setter
    def selected(self, value: str) -> None:
        if self.selected == value:
            return
        self.__selected = value
        self._main.scheduler.schedule_action(self.__update_selected)

    def __update_selected(self):
        self.__ignore_next_change_event = True
        self.__selected_var.set(self.__selected)

    def __update_options(self):
        self._tk_object['menu'].delete(0, 'end')
        for st in self.__options:
            self._tk_object['menu'].add_command(label=st, command=_setit(self.__selected_var, st))
        if self.selected not in self.__options:
            self.selected = self.__options[0]

    def __clicked_changed(self, *args: str) -> None:
        if not self.__ignore_next_change_event:
            self._handle_event(ETKEventData(self, self.EVENTS.CHANGED))
        else:
            self.__ignore_next_change_event = False
