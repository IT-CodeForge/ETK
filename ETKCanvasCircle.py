from tkinter import Canvas
from typing import Any
from .ETKCanvasOval import ETKCanvasOval
from .Vector2d import Vector2d


class ETKCanvasCircle(ETKCanvasOval):
    def __init__(self, canvas: Canvas, center: Vector2d, radius: int, background_color: int, outline_color: int, **kwargs: Any) -> None:
        super().__init__(canvas, center,
                               radius, radius, background_color, outline_color, **kwargs)
        self._item_type = "circle"
