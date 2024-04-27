import math
from tkinter import Canvas
from ETKV2.vector2d import vector2d
from .ETKCanvasItem import ETKCanvasItem

class ETKCanvasOval(ETKCanvasItem):
    def __init__(self, canvas: Canvas, center:vector2d, radius_x:int, radius_y:int, background_color:int=0x00FF00, outline_color:int=0x000000) -> None:
        self._center = center
        temp_pointlist: list[vector2d] = self.__poly_oval(center, radius_x, radius_y)
        ETKCanvasItem.__init__(self, canvas,temp_pointlist , background_color, outline_color)
    
    @ETKCanvasItem.pos.getter
    def pos(self)->vector2d:
        return self._center
    
    def __poly_oval(self, center:vector2d, radian_x:int, radian_y:int)->list[vector2d]:
        """generates the cornerpoints, for a polygon which symbolizes the oval"""
        #steps is the number of corners the polygon has
        steps = int((radian_x * radian_y) / 4)
        point_list: list[vector2d] = []
        theta = 0
        for _ in range(steps):
            my_point = center + vector2d(radian_x * math.cos(theta), radian_y * math.sin(theta))
            point_list.append(my_point)
            theta += (2*math.pi) / steps
        return point_list