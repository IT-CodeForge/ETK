from typing import Any

from ..ETKMainWindow import ETKMain
from ..Vector2d import Vector2d
from .ETKBaseTkWidget import ETKBaseTkWidget
from .ETKUtils import gen_col_from_int


class ETKBaseTkWidgetText(ETKBaseTkWidget):
    def __init__(self, *, main: ETKMain, text: str, pos: Vector2d, size: Vector2d, visibility: bool, background_color: int, text_color: int, outline_color: int, outline_thickness: int, **kwargs: Any) -> None:
        self._text = "" if text != "" else "-"
        self._text_color = 0 if text_color != 0 else 1
        self.multiline = getattr(self, "multiline", False)

        super().__init__(main=main, pos=pos, size=size, visibility=visibility, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

        self.text_color = text_color
        self.text = text

    # region Properties

    @property
    def text(self) -> str:
        return self._tk_object.cget("text")

    @text.setter
    def text(self, value: str) -> None:
        if self._text == value:
            return
        if not self.multiline:
            value = value.replace("\n", "").replace("\r", "")
        self._text = value
        self._main.scheduler.schedule_action(self._update_text)

    @property
    def text_color(self) -> int:
        return int(self._tk_object["fg"][1:], 16)

    @text_color.setter
    def text_color(self, value: int) -> None:
        if self._text_color == value:
            return
        self._text_color = value
        self._update_text_color()

    # endregion
    # region Methods
        
    def _update_text(self):
        self._tk_object.config(text=self._text)  # type:ignore
    
    def _update_text_color(self):
        self._tk_object.configure(fg=gen_col_from_int(self._text_color))  # type:ignore

    #endregion
