from __future__ import annotations
from tkinter import Event, EventType
from typing import Any

from .Internal.ETKEventData import ETKEventData

from .Internal.ETKMain import ETKMain

from .Vector2d import Vector2d
from .ETKLabel import ETKLabel
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable


class ETKEdit(ETKBaseTkWidgetDisableable, ETKLabel):
    class EVENTS(ETKLabel.EVENTS):
        CHANGED: ETKEdit.EVENTS
        CHANGED_DELAYED: ETKEdit.EVENTS
        _values = {"CHANGED": "<KeyRelease>", "CHANGED_DELAYED": "<KeyRelease>"}

    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: Vector2d = Vector2d(80, 17), text: str = "Edit", *, multiline: bool = False, visibility: bool = True, enabled: bool = True, background_color: int = 0xEEEEEE, text_color: int = 0, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__old_text: str = ""
        self.__delay_cycles: int = -1

        super().__init__(main=main, pos=pos, size=size, text=text, multiline=multiline, visibility=visibility, enabled=enabled,
                         background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

        self._tk_object["state"] = "normal"
        self._event_lib.update({e: [] for e in self.EVENTS if e not in self._event_lib.keys()})
        self.add_event(self.EVENTS.CHANGED, lambda: None)

    # region Methods

    def _update_text(self):
        super()._update_text()
        self.__old_text = self._text

    def _update_enabled(self) -> bool:
        if not super()._update_enabled():
            return False
        if self.abs_enabled:
            self._send_button_event_break = False
            self._tk_object.configure(cursor="xterm")
        else:
            self._send_button_event_break = True
            self._tk_object.configure(cursor="")
        return True

    def __send_delayed_changed_event(self, event: Event) -> None:  # type:ignore
        if self.__delay_cycles == 0:
            self._handle_event(ETKEventData(self, self.EVENTS.CHANGED_DELAYED, tk_event=event))
        self.__delay_cycles -= 1

    def _handle_tk_event(self, event: Event) -> None | str:  # type:ignore
        match event.type:
            case EventType.KeyRelease:
                if self.abs_enabled and self.text != self.__old_text:
                    if not self.multiline:
                        self.text = self.text
                    self.__delay_cycles += 1
                    self._handle_event(ETKEventData(self, self.EVENTS.CHANGED, tk_event=event))
                    self._tk_object.after(1000, self.__send_delayed_changed_event, event)  # type:ignore
                    self.__old_text = self.text
                return
            case _:
                pass
        return super()._handle_tk_event(event)  # type:ignore

    # endregion
