import math
from typing import Any
from .ETKCanvasItem import ETKCanvasItem
from tkinter import Canvas
from .Vector2d import Vector2d


class ETKCanvasLine(ETKCanvasItem):
    def __init__(self, canvas: Canvas, start_point: Vector2d, end_point: Vector2d, thickness: float, background_color: int, outline_color: int, **kwargs: Any) -> None:
        self.__start_point = start_point
        direction_vector = end_point - start_point
        thickness_vector = direction_vector.rotate(
            -0.5*math.pi).normalize() * 0.5 * thickness
        temp_pointlist: list[Vector2d] = [start_point + thickness_vector, end_point +
                                          thickness_vector, end_point - thickness_vector, start_point - thickness_vector]
        super().__init__(canvas, temp_pointlist,
                               background_color, outline_color, **kwargs)
        self._item_type = "line"

    # region Properties

    @ETKCanvasItem.pos.getter
    def pos(self) -> Vector2d:
        return self.__start_point.copy()

    # endregion
