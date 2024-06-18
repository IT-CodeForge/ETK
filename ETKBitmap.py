from .Internal.ETKMain import ETKMain
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKUtils import gen_col_from_int
from .Vector2d import Vector2d
from tkinter import PhotoImage, Label
from typing import Any, Iterable


class ETKBitmap(ETKBaseTkWidgetDisableable):
    class Events(ETKBaseTkWidgetDisableable.Events):
        pass

    def __init__(self, main: ETKMain, pos: Vector2d, size: Vector2d, *, visibility: bool = True, enabled: bool = True, background_color: int = 0xAAAAAA, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__bitmap = PhotoImage(width=int(size.x), height=int(size.y))
        self._tk_object: Label = Label(  # type:ignore
            main.root_tk_object, text="", image=self.__bitmap)
        super().__init__(main=main, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

    # region Methods

    def _update_size(self) -> bool:
        if not super()._update_size():
            return False
        self.__bitmap.configure(width=int(self.size.x), height=int(self.size.y))
        return True

    def __getitem__(self, index: Vector2d | Iterable[int]) -> int:
        if type(index) not in [Vector2d, Iterable]:
            raise TypeError(
                f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        my_index: Iterable[int]
        if type(index) == Vector2d:
            my_index = [int(index.x), int(index.y)]
        else:
            my_index = index  # type:ignore
        red, green, blue = self.__bitmap.get(*my_index)
        color = blue + (green << 8) + (red << 16)
        return color

    def __setitem__(self, index: Vector2d | Iterable[int], value: int) -> None:
        if type(index) not in [Vector2d, Iterable]:
            raise TypeError(
                f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        my_index: tuple[int, int]
        if type(index) == Vector2d:
            my_index = (int(index.x), int(index.y))
        else:
            my_index = tuple(index)  # type:ignore
        color = gen_col_from_int(value)
        self.__bitmap.put(color, my_index)
        self._tk_object.configure(image=self.__bitmap)

    def clear(self) -> None:
        self.__bitmap.blank()

    # endregion
