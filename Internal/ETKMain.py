from tkinter import Tk
from .ETKScheduler import ETKScheduler

class ETKMain:
    def __init__(self, root_tk_object: Tk, scheduler: ETKScheduler, scale_factor: float) -> None:
        self.__root_tk_object: Tk = root_tk_object
        self.__scheduler: ETKScheduler = scheduler
        self.__scale_factor: float = scale_factor

    @property
    def root_tk_object(self) -> Tk:
        """READ-ONLY"""
        return self.__root_tk_object

    @property
    def scheduler(self) -> ETKScheduler:
        """READ-ONLY"""
        return self.__scheduler

    @property
    def scale_factor(self) -> float:
        """READ-ONLY"""
        return self.__scale_factor