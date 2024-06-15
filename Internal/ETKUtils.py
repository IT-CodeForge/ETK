from __future__ import annotations
import sys
from tkinter import Event, Tk
import traceback
from typing import TYPE_CHECKING, Any, Callable, Optional

from ..Vector2d import Vector2d

if TYPE_CHECKING:
    from .ETKEventData import ETKEventData

def gen_col_from_int(col: Optional[int]) -> str:
    if col is None:
        return ""
    hold_str = hex(col)[2:]
    if len(hold_str) < 6:
        hold_str = "0"*(6-len(hold_str)) + hold_str
    return "#" + hold_str


def exec_event_callback(callback_function: Callable[[], Any] | Callable[[ETKEventData], Any], event_data: ETKEventData) -> None:
    err_1 = ""
    try:
        callback_function(event_data)  # type:ignore
        return
    except TypeError as ex:
        err_1 = traceback.format_exc()
        if str(ex).find("positional argument") == -1:
            raise ex
    try:
        callback_function()  # type:ignore
    except TypeError as ex:
        if str(ex).find("positional argument") == -1:
            raise ex
        ret_val = callback_function.__code__.co_varnames
        name = callback_function.__name__  # type:ignore
        print(err_1, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise TypeError(
            f"invalid parametercount for event function ({name}) (can only be 0, 1 (self, cls, etc not included)), parameter: {ret_val}")


def get_rel_event_pos(event: Event, scale_factor: float) -> Vector2d:  # type:ignore
    return Vector2d(event.x, event.y) / scale_factor


def get_abs_event_pos(event: Event, root_tk: Tk, scale_factor: float) -> Vector2d:  # type:ignore
    return (Vector2d(event.x_root, event.y_root) - Vector2d(root_tk.winfo_rootx(), root_tk.winfo_rooty())) / scale_factor