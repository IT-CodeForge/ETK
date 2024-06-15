import math
from tkinter import Canvas
from typing import Any
from .Vector2d import Vector2d
from .ETKCanvasItem import ETKCanvasItem


class ETKCanvasOval(ETKCanvasItem):
    def __init__(self, canvas: Canvas, center: Vector2d, radius_x: int, radius_y: int, background_color: int, outline_color: int, **kwargs: Any) -> None:
        self._center = center
        temp_pointlist: list[Vector2d] = self.__poly_oval(
            center, radius_x, radius_y)
        super().__init__(canvas, temp_pointlist,
                               background_color, outline_color, **kwargs)
        self._item_type = "oval"

    # region Properties

    @ETKCanvasItem.pos.getter
    def pos(self) -> Vector2d:
        return self._center.copy()

    # endregion
    # region Methods

    def __poly_oval(self, center: Vector2d, radius_x: int, radius_y: int) -> list[Vector2d]:
        """generates the cornerpoints, for a polygon which symbolizes the oval"""
        # steps is the number of corners the polygon has
        steps = int((radius_x * radius_y) / 4)
        point_list: list[Vector2d] = []
        theta = 0
        for _ in range(steps):
            my_point = center + \
                Vector2d(radius_x * math.cos(theta),
                         radius_y * math.sin(theta))
            point_list.append(my_point)
            theta += (2*math.pi) / steps
        return point_list

    # endregion
