from __future__ import annotations
from tkinter import Event
from typing import Optional

from ..Vector2d import Vector2d

from .ETKBaseObject import ETKBaseObject, ETKEvents
from .ETKBaseWidget import ETKBaseWidget


class ETKEventData:
    __ATTRIBUTES = {"sender": ETKBaseObject, "event": ETKEvents, "tk_event": Event, "child_sender": ETKBaseWidget, "rel_pos": Vector2d, "abs_pos": Vector2d, "state": str | int, "btn_num": int, "keysym": str, "keycode": int, "keychar": str}

    def __init__(self, sender: ETKBaseObject, event: ETKEvents, *, tk_event: Optional[Event] = None, child_sender: Optional[ETKBaseWidget] = None, rel_pos: Optional[Vector2d] = None, abs_pos: Optional[Vector2d] = None, state: Optional[str | int] = None, btn_num: Optional[int] = None, keysym: Optional[str] = None, keycode: Optional[int] = None, keychar: Optional[str] = None) -> None:  # type:ignore
        self.sender = sender
        self.event = event
        self.tk_event = tk_event  # type:ignore
        self.child_sender = child_sender
        self.rel_pos = rel_pos
        self.abs_pos = abs_pos
        self.state = state
        self.btn_num = btn_num
        self.keysym = keysym
        self.keycode = keycode
        self.keychar = keychar

    def __str__(self) -> str:
        attr: list[str] = []
        for a in self.__ATTRIBUTES.keys():
            if (v := getattr(self, a)) is not None:
                attr.append(f"{a}: {repr(v)}")
        return f"ETKEventData<{'; '.join(attr)}>"

    def __repr__(self) -> str:
        st = self.__str__()
        st = st[:st.find("<") + 1] + f"self: {object.__repr__(self)}; " + st[st.find("<") + 1:]
        return st
