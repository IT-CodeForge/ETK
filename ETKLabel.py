from tkinter import END, Event, EventType, Text
from typing import Any

from .Internal.ETKMain import ETKMain
from .Vector2d import Vector2d
from .Internal.ETKBaseTkWidgetText import ETKBaseTkWidgetText


class ETKLabel(ETKBaseTkWidgetText):
    class EVENTS(ETKBaseTkWidgetText.EVENTS):
        pass

    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: Vector2d = Vector2d(80, 17), text: str = "Label", *, multiline: bool = True, visibility: bool = True, background_color: int = 0xEEEEEE, text_color: int = 0, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self._tk_object: Text = Text(main.root_tk_object)  # type:ignore
        self._send_button_event_break = True
        self.multiline = multiline

        super().__init__(main=main, pos=pos, size=size, text=text, visibility=visibility, background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

        self._tk_object["state"] = "disabled"
        self.add_event(self.EVENTS.MOUSE_DOWN, lambda: None)
        self._tk_object.configure(cursor="")

    # region Properties

    @ETKBaseTkWidgetText.text.getter
    def text(self) -> str:
        return self._tk_object.get("1.0", 'end-1c')

    # endregion
    # region Methods

    def _update_text(self):
        state = self._tk_object["state"]
        self._tk_object["state"] = "normal"
        self._tk_object.delete(1.0, END)
        self._tk_object.insert(1.0, self._text)
        self._tk_object["state"] = state

    def _handle_tk_event(self, event: Event) -> str | None:  # type:ignore
        super()._handle_tk_event(event)  # type:ignore
        match event.type:
            case EventType.ButtonPress:
                if self._send_button_event_break:
                    return "break"
            case _:
                pass

    # endregion
