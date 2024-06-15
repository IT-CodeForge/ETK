from tkinter import Canvas
from typing import Any
from .Vector2d import Vector2d
from .ETKCanvasItem import ETKCanvasItem


class ETKCanvasRectangle(ETKCanvasItem):
    def __init__(self, canvas: Canvas, top_left: Vector2d, bottom_right: Vector2d, background_color: int, outline_color: int, **kwargs: Any) -> None:
        temp_pointlist = [top_left, Vector2d(
            bottom_right.x, top_left.y), bottom_right, Vector2d(top_left.x, bottom_right.y)]
        super().__init__(canvas, temp_pointlist,
                               background_color, outline_color, **kwargs)
        self._item_type = "rectangle"
