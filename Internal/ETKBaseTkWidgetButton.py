from tkinter import FLAT, LabelFrame, Tk
from typing import Any

from .ETKMain import ETKMain

from .ETKUtils import gen_col_from_int
from .ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .ETKBaseTkWidgetText import ETKBaseTkWidgetText
from ..Vector2d import Vector2d


class ETKBaseTkWidgetButton(ETKBaseTkWidgetDisableable, ETKBaseTkWidgetText):
    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, text: str, visibility: bool, enabled: bool, background_color: int, text_color: int, outline_color: int, outline_thickness: int, **kwargs: Any) -> None:
        self._outline: LabelFrame

        super().__init__(main=main, text=text, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

    # region Methods
    
    def _update_text_color(self):
        super()._update_text_color()
        self._tk_object.configure(disabledforeground=gen_col_from_int(self._text_color))  # type:ignore

    def _create_outline(self, tk: Tk) -> None:
        self._outline = LabelFrame(tk, relief=FLAT)

    def _update_visibility(self) -> bool:
        if not super()._update_visibility():
            return False
        if not self.abs_visibility:
            self._outline.place_forget()
            self._outline.update()
        return True
    
    def _update_outline_color(self):
        self._outline.configure(bg=gen_col_from_int(self._outline_color))  # type:ignore
    
    def _update_outline_thickness(self):
        self._outline.configure(bd=self._outline_thickness)  # type:ignore
        self._paint_object()

    def _place_object(self) -> None:
        pos = self.abs_pos * self._main.scale_factor
        size = self.size * self._main.scale_factor
        self._tk_object.place(x=0, y=0, width=size.x-2*self.outline_thickness, height=size.y-2*self.outline_thickness)
        self._outline.place(x=pos.x, y=pos.y, width=size.x, height=size.y)

    # endregion
