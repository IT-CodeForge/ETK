from typing import Any

from .Internal.ETKMain import ETKMain
from .Vector2d import Vector2d
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .ETKCanvasItem import ETKCanvasItem
from .ETKCanvasRectangle import ETKCanvasRectangle
from .ETKCanvasSquare import ETKCanvasSquare
from .ETKCanvasOval import ETKCanvasOval
from .ETKCanvasCircle import ETKCanvasCircle
from .ETKCanvasLine import ETKCanvasLine
from tkinter import Canvas
from .Internal.ETKBaseObject import ETKEvents

class ETKCanvasEvents(ETKEvents):
    pass


class ETKCanvas(ETKBaseTkWidgetDisableable):
    def __init__(self, main: ETKMain, pos: Vector2d, size: Vector2d, *, visibility: bool = True, enabled: bool = True, background_color: int = 0xFFFFFF, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self._tk_object: Canvas = Canvas(main.root_tk_object, highlightthickness=0)  # type:ignore
        self.__canvas_items: list[ETKCanvasItem] = []
        super().__init__(main=main, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

    # region Properties

    @property
    def canvas_items(self) -> list[ETKCanvasItem]:
        """READ-ONLY"""
        return self.__canvas_items.copy()

    # endregion

    # region Methods

    def draw_square(self, top_left: Vector2d, side_length: int, background_color: int = 0xFF0000, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasSquare(self._tk_object, top_left, side_length, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_rectangle(self, top_left: Vector2d, bottom_right: Vector2d, background_color: int = 0xFF0000, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasRectangle(self._tk_object, top_left, bottom_right, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_circle(self, center: Vector2d, radius: int, background_color: int = 0x00FF00, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasCircle(self._tk_object, center, radius, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_oval(self, center: Vector2d, radius_x: int, radius_y: int, background_color: int = 0x00FF00, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasOval(self._tk_object, center, radius_x, radius_y, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_polygon(self, corner_list: list[Vector2d], background_color: int = 0x0000FF, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasItem(self._tk_object, corner_list, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_line(self, start_point: Vector2d, end_point: Vector2d, thickness: float = 2, background_color: int = 0x000000, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasLine(self._tk_object, start_point, end_point, thickness, background_color, outline_color))
        return self.__canvas_items[-1]

    def delete_item(self, item: ETKCanvasItem) -> None:
        for index, canvas_item in enumerate(self.__canvas_items):
            if canvas_item == item:
                self.delete_item_at_index(index)
                break

    def delete_item_at_index(self, index: int) -> None:
        self.__canvas_items[index]._isdeleted = True  # type:ignore
        del self.__canvas_items[index]

    def clear(self) -> None:
        for index, canvasitem in enumerate(self.__canvas_items):
            canvasitem._isdeleted = True  # type:ignore
            del self.__canvas_items[index]

    # endregion
