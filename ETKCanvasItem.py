from __future__ import annotations
import math
from .Internal.ETKUtils import gen_col_from_int
from tkinter import Canvas
from typing import Callable, Optional
from .Vector2d import Vector2d


class ETKCanvasItem:
    def __init__(self, canvas: Canvas, pointlist: list[Vector2d], background_color: int, outline_color: int) -> None:
        self._tk_object: Canvas = canvas
        self._pointlist: list[Vector2d] = pointlist
        self._rotation: float = 0
        self._isdeleted = False
        self._background_color: str = gen_col_from_int(background_color)
        self._outline_color: str = gen_col_from_int(outline_color)
        self._item_type: str = "polygon"
        tkinter_pointlist: list[tuple[float, float]] = [
            (vector.x, vector.y) for vector in self._pointlist]
        self.itemId: int = self._tk_object.create_polygon(
            tkinter_pointlist, fill=self._background_color, outline=self._outline_color)

    # region Properties

    @property
    def pos(self) -> Vector2d:
        return self._pointlist[0].copy()

    @pos.setter
    def pos(self, value: Vector2d) -> None:
        self.__check_if_deleted()
        move_vec = value - self.pos
        for index, point in enumerate(self._pointlist):
            self._pointlist[index] = point + move_vec
        self.__transform_shape()

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, value: float) -> None:
        self.__check_if_deleted()
        for index, point in enumerate(self._pointlist):
            self._pointlist[index] = self.pos + \
                (point - self.pos).rotate(value - self.rotation)
        self._rotation = value
        if self._rotation >= 2 * math.pi:
            self.rotation -= 2 * math.pi
        self.__transform_shape()

    @property
    def background_color(self) -> int:
        return int(self._background_color[1:], 16)

    @background_color.setter
    def background_color(self, value: Optional[int]) -> None:
        self.__check_if_deleted()
        self._background_color = gen_col_from_int(value)
        self.__redraw_shape()

    @property
    def outline_color(self) -> int:
        return int(self._outline_color[1:], 16)

    @outline_color.setter
    def outline_color(self, value: int) -> None:
        self.__check_if_deleted()
        self._outline_color = gen_col_from_int(value)
        self.__redraw_shape()

    @property
    def canvasitem_type(self) -> str:
        "READ-ONLY"
        return self._item_type

    # endregion
    # region Methods

    def find_intersections(self, shape: ETKCanvasItem) -> list[Vector2d]:
        solution_list: list[Vector2d] = []
        other_pointlist = shape._pointlist + [shape._pointlist[0]]
        my_pointlist = self._pointlist + [self._pointlist[0]]
        for i in range(len(my_pointlist) - 1):
            for n in range(len(other_pointlist) - 1):
                p1 = my_pointlist[i]
                p2 = my_pointlist[i + 1]
                p3 = other_pointlist[n]
                p4 = other_pointlist[n + 1]
                intersection = self.__find_intersection(p1, p2, p3, p4)
                if intersection != None and intersection not in solution_list:
                    solution_list.append(intersection)
        return solution_list

    def is_point_in_shape(self, point: Vector2d) -> bool:
        solution = self. __winding_numbers(point)
        if solution == 0:
            return False
        else:
            return True

    def __winding_numbers(self, point: Vector2d) -> float:
        direction_vec: Vector2d = Vector2d(1, 0)
        p3 = point
        x_list = [vector.x for vector in self._pointlist]
        y_list = [vector.y for vector in self._pointlist]
        distance_to_bounding_box = Vector2d(max(x_list), min(y_list))

        retval = 0.0

        p4 = point + direction_vec.normalize() * distance_to_bounding_box
        for index in range(len(self._pointlist)):
            p1 = Vector2d(self._pointlist[index].x, self._pointlist[index].y)
            p2 = Vector2d(self._pointlist[index + 1].x,
                          self._pointlist[index + 1].y)
            sol = self.__find_intersection(p1, p2, p3, p4)
            if sol is None:
                continue
            poly_edge_dir = p2 - p1
            sign = (poly_edge_dir*Vector2d(0, 1)).normalize().y
            if sol in [p1, p2]:
                retval += 0.5 * sign
            else:
                retval += sign

        return retval

    def __find_intersection(self, p1: Vector2d, p2: Vector2d, p3: Vector2d, p4: Vector2d) -> Optional[Vector2d]:
        s1 = p2 - p1
        s2 = p4 - p3

        denominator = s1.crossproduct(s2)

        if denominator == 0:
            return None

        s = p3 - p1
        t = s.crossproduct(s2) / denominator
        u = s.crossproduct(s1) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection = p1 + t * s1
            return intersection
        else:
            return None

    def __transform_shape(self) -> None:
        tkinter_pointlist: list[float] = self.__get_tkinter_pointlist()
        self._tk_object.coords(self.itemId, tkinter_pointlist)

    def __redraw_shape(self) -> None:
        self._tk_object.delete(self.itemId)
        tkinter_pointlist: list[float] = self.__get_tkinter_pointlist()
        # self._tk_object.create_polygon([(0.0,0.0),(10.0,10.0),(0.0,10.0)])
        self.itemId = self._tk_object.create_polygon(
            tkinter_pointlist, fill=self._background_color, outline=self._outline_color)

    def __get_tkinter_pointlist(self) -> list[float]:
        getx: Callable[[Vector2d], float] = lambda vector: vector.x
        gety: Callable[[Vector2d], float] = lambda vector: vector.y
        return [f(point) for point in self._pointlist for f in (getx, gety)]

    def __check_if_deleted(self) -> None:
        if self._isdeleted:
            raise RuntimeError(f"cannot modify the deleted Canvasitem {self}")

    # endregion
