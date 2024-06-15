from tkinter import Widget as tk_widget
from typing import Any

from ..ETKMainWindow import ETKMain

from .ETKUtils import gen_col_from_int

from ..Vector2d import Vector2d
from .ETKBaseWidget import ETKBaseWidget
from .ETKBaseTkObject import ETKBaseTkObject


class ETKBaseTkWidget(ETKBaseTkObject, ETKBaseWidget):

    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, visibility: bool, background_color: int, outline_color: int, outline_thickness: int, **kwargs: Any) -> None:
        self._tk_object: tk_widget
        self._outline_color: int = 0 if outline_color != 0 else 1
        self._outline_thickness: int = 0 if outline_thickness != 0 else 1

        super().__init__(main=main, pos=pos, size=size, visibility=visibility, background_color=background_color, **kwargs)

        self.outline_thickness = outline_thickness
        self.outline_color = outline_color

    # region Properties

    @property
    def outline_color(self) -> int:
        return self._outline_color

    @outline_color.setter
    def outline_color(self, value: int) -> None:
        if self._outline_color == value:
            return
        self._outline_color = value
        self._main.scheduler.schedule_action(self._update_outline_color)

    @property
    def outline_thickness(self) -> int:
        return self._outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value: int) -> None:
        if self._outline_thickness == value:
            return
        self._outline_thickness = value
        self._main.scheduler.schedule_action(self._update_outline_thickness)

    # endregion
    # region Methods

    def _place_object(self) -> None:
        pos = self.abs_pos * self._main.scale_factor
        size = self.size * self._main.scale_factor
        self._tk_object.place(x=pos.x, y=pos.y, width=size.x, height=size.y)
    
    def _paint_object(self) -> None:
        if self.abs_visibility:
            self._place_object()

        # region update event methods

    def _update_pos(self) -> bool:
        if not super()._update_pos():
            return False
        self._paint_object()
        return True
    
    def _update_size(self) -> bool:
        if not super()._update_size():
            return False
        self._paint_object()
        return True

    def _update_visibility(self) -> bool:
        if not super()._update_visibility():
            return False
        if self.abs_visibility:
            self._paint_object()
        else:
            self._tk_object.place_forget()
            self._tk_object.update()
        return True
    
    def _update_outline_color(self) -> None:
        self._tk_object.configure(highlightbackground=gen_col_from_int(self._outline_color))  # type:ignore
    
    def _update_outline_thickness(self) -> None:
        self._tk_object.configure(highlightthickness=self._outline_thickness)  # type:ignore

    # endregion
    # endregion
