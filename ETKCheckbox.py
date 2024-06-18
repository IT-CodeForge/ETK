from __future__ import annotations
from typing import Any

from .Internal.ETKEventData import ETKEventData

from .Internal.ETKMain import ETKMain

from .Vector2d import Vector2d
from .Internal.ETKBaseTkWidgetButton import ETKBaseTkWidgetButton
from tkinter import Checkbutton, IntVar


class ETKCheckbox(ETKBaseTkWidgetButton):
    class Events(ETKBaseTkWidgetButton.Events):
        CHECKED: ETKCheckbox.Events
        UNCHECKED: ETKCheckbox.Events
        TOGGLED: ETKCheckbox.Events
        _values = {"CHECKED": "<Custom>", "UNCHECKED": "<Custom>", "TOGGLED": "<Custom>"}

    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: Vector2d = Vector2d(70, 18), text: str = "Checkbox", state: bool = False, *, visibility: bool = True, enabled: bool = True, background_color: int = 0xEEEEEE, text_color: int = 0x0, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__state_var = IntVar()
        self.__state = not state
        self.__ignore_next_change_event: bool = False
        self._create_outline(main.root_tk_object)
        self._tk_object: Checkbutton = Checkbutton(  # type:ignore
            self._outline, variable=self.__state_var)
        super().__init__(main=main, pos=pos, size=size, text=text, visibility=visibility, enabled=enabled, background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)
        self._event_lib.update({e: [] for e in self.Events if e not in self._event_lib.keys()})
        self.__state_var.trace_add("write", self.__checkbox_event_handler)
        self.state = state

    # region Properties

    @property
    def state(self) -> bool:
        return bool(self.__state_var.get())

    @state.setter
    def state(self, value: bool) -> None:
        if self.state == value:
            return
        self.__state = value
        self._main.scheduler.schedule_action(self.__update_state)

    # endregion
    # region Methods

    def __update_state(self):
        self.__ignore_next_change_event = True
        self.__state_var.set(self.__state)

    def __checkbox_event_handler(self, *args: str) -> None:
        if self.__ignore_next_change_event:
            self.__ignore_next_change_event = False
            return
        self._handle_event(ETKEventData(self, self.Events.TOGGLED))
        if self.state:
            self._handle_event(ETKEventData(self, self.Events.CHECKED))
        else:
            self._handle_event(ETKEventData(self, self.Events.UNCHECKED))

    # endregion
