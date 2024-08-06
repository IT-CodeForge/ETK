import sys
from threading import Thread, current_thread
import time
from tkinter import Tk
from traceback import format_exc
from typing import Any, Callable, Optional, Type

from .ETKEventData import ETKEventData

from .ETKBaseTkObject import ETKBaseTkObject

from .ETKUtils import exec_event_callback


class ETKScheduler:
    def __init__(self, tk: Tk, disabled: bool) -> None:
        self.__disabled = disabled
        self.except_exceptions: tuple[Type[Exception], ...] = tuple()
        self.except_exception_handler: Callable[[Exception], Optional[bool]] = lambda _: True
        self.__tk = tk
        self.__scheduled_events: list[tuple[Callable[..., Any], ETKEventData]] = []
        self.__scheduled_gui_actions: dict[Callable[..., Any], tuple[tuple[Any, ...], dict[str, Any]]] = {}
        self.__scheduled_non_gui_actions: dict[Callable[..., Any], tuple[tuple[Any, ...], dict[str, Any]]] = {}
        self.__thread = Thread(target=self.__handler, daemon=True)
        if not self.__disabled:
            self.__thread.start()

    def __schedule_action(self, scheduler_dict: dict[Callable[..., Any], tuple[tuple[Any, ...], dict["str", Any]]], callback: Callable[..., Any], *args: Any, **kwargs: Any):
        if current_thread() != self.__thread or self.__disabled:
            callback(*args, **kwargs)
            return

        if callback in scheduler_dict.keys():
            del scheduler_dict[callback]
        scheduler_dict.update({callback: (args, kwargs)})

    def schedule_action(self, callback: Callable[..., Any], *args: Any, **kwargs: Any):
        if hasattr(callback, "__self__") and callback.__self__ is not None and not isinstance(callback.__self__, ETKBaseTkObject):  # type:ignore
            self.__schedule_action(
                self.__scheduled_non_gui_actions, callback, *args, **kwargs)
        self.__schedule_action(
            self.__scheduled_gui_actions, callback, *args, **kwargs)

    def schedule_event(self, ev_callback: Callable[..., Any], event_data: ETKEventData):
        if self.__disabled:
            exec_event_callback(ev_callback, event_data)
            return
        self.__scheduled_events.append((ev_callback, event_data))

    def __handle_actions(self, scheduler_dict: dict[Callable[..., Any], tuple[tuple[Any, ...], dict["str", Any]]], ev_loop_callback: Callable[..., Any] = lambda: None):
        while len(scheduler_dict.keys()) != 0:
            ev_loop_callback()
            c2 = tuple(scheduler_dict.keys())[0]
            a2, kwa2 = scheduler_dict[c2]
            del scheduler_dict[c2]
            c2(*a2, **kwa2)

    def handle_actions(self):
        self.__handle_actions(self.__scheduled_non_gui_actions)
        self.__handle_actions(self.__scheduled_gui_actions, lambda: self.__handle_actions(
            self.__scheduled_non_gui_actions))

    def __handler(self):
        try:
            while True:
                begin_ns = time.time_ns()

                if len(self.__scheduled_gui_actions.keys()) != 0 or len(self.__scheduled_non_gui_actions.keys()) != 0:
                    raise RuntimeError

                while len(self.__scheduled_events) > 0:
                    c1, data = self.__scheduled_events[0]
                    self.__scheduled_events.pop(0)
                    exec_event_callback(c1, data)
                self.handle_actions()

                sleep_duration = 0.1
                duration = (time.time_ns() - begin_ns) / 10**9
                duration = sleep_duration if duration > sleep_duration else duration
                time.sleep(sleep_duration - duration)

        except self.except_exceptions as e:
            if self.except_exception_handler(e):
                try:
                    self.__tk.after(0, lambda: sys.exit(1))
                finally:
                    sys.exit(1)

        except Exception as e:
            print(format_exc(), file=sys.stderr)
            try:
                self.__tk.after(0, lambda: sys.exit(1))
            finally:
                sys.exit(1)
