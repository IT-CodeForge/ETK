from __future__ import annotations
from abc import abstractmethod
from tkinter import Event, Tk, EventType, font
from typing import Any, Callable, Optional

from .Internal.ETKUtils import get_abs_event_pos, get_rel_event_pos  # type:ignore

from .Internal.ETKScheduler import ETKScheduler

from .Vector2d import Vector2d
from .Internal.ETKBaseTkObject import ETKBaseTkObject
from .Internal.ETKBaseObject import ETKEvents
from .Internal.ETKEventData import ETKEventData


class ETKWindowEvents(ETKEvents):
    KEY_PRESSED: ETKWindowEvents
    KEY_RELEASED: ETKWindowEvents
    FOCUS_IN: ETKWindowEvents
    FOCUS_OUT: ETKWindowEvents
    START: ETKWindowEvents
    EXIT: ETKWindowEvents

    _values = {"KEY_PRESSED": "<KeyPress>", "KEY_RELEASED": "<KeyRelease>", "FOCUS_IN": "<FocusIn>", "FOCUS_OUT": "<FocusOut>", "START": "<Custom>", "EXIT": "<Custom>"}


class ETKMainWindow(ETKBaseTkObject):
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

    def __init__(self, pos: Vector2d = Vector2d(0, 0), size: Optional[Vector2d] = None, caption: str = "Window-Title", fullscreen: bool = True, *, visibility: bool = True, background_color: int = 0xAAAAAA, scheduler_disabled: bool = False, scale_factor: float = 1, **kwargs: Any) -> None:
        from .ETKCanvas import ETKCanvas
        self._tk_object: Tk = Tk()

        def raise_exception(exc: Exception, *_: Any):
            self.exit()
        self._tk_object.report_callback_exception = raise_exception #type:ignore

        self._main = ETKMain(self._tk_object, ETKScheduler(self._tk_object, scheduler_disabled), scale_factor)
        self.__topmost = False
        self.exit_locked = False
        self.exit_ignore_next = False
        self.__fullscreen = False
        self.canvas = ETKCanvas(self._main, Vector2d(), Vector2d())
        self.__caption = ""

        super().__init__(main=self._main, pos=pos, size=Vector2d(1920, 1080), background_color=background_color, visibility=visibility, **kwargs)

        self.canvas.outline_color = 0x0
        self.canvas.outline_thickness = 2
        self.caption = caption
        self.size = size
        self.fullscreen = fullscreen
        self._tk_object.protocol("WM_DELETE_WINDOW", self.exit)
        self._event_lib.update({e: [] for e in ETKWindowEvents if e not in self._event_lib.keys()})
        self._tk_object.bind(
            "<Configure>", self.__configure_event_handler)  # type:ignore

        default_font = font.nametofont("TkFixedFont")
        default_font.configure(size=int(10 * self._main.scale_factor))
        self._tk_object.option_add("*Font", default_font)  # type:ignore

        class InternalEvents(ETKEvents):
            INTERNAL_EVENT: ETKEvents
            _values = {"INTERNAL_EVENT": "<Custom>"}

        self._main.scheduler.schedule_event(lambda: self._add_elements(), ETKEventData(self, InternalEvents.INTERNAL_EVENT))
        self._main.scheduler.schedule_event(lambda: self._handle_event(ETKEventData(self, ETKWindowEvents.START)), ETKEventData(self, InternalEvents.INTERNAL_EVENT))

    # region Properties

    @ETKBaseTkObject.pos.setter
    def pos(self, value: Vector2d) -> None:
        ETKBaseTkObject.pos.fset(self, value)  # type:ignore
        self.fullscreen = False
        self._main.scheduler.schedule_action(self.__place_object)

    @property
    def abs_pos(self) -> Vector2d:
        """READ-ONLY"""
        return Vector2d(self._tk_object.winfo_rootx(), self._tk_object.winfo_rooty())

    @ETKBaseTkObject.size.setter
    def size(self, value: Optional[Vector2d]) -> None:
        if value is None:
            old_state = self._tk_object.state()
            self._tk_object.state("zoomed")
            self._tk_object.update()
            t_value = Vector2d(self._tk_object.winfo_width(),
                               self._tk_object.winfo_height())
            self._tk_object.state(old_state)
        else:
            t_value = value
        ETKBaseTkObject.size.fset(self, t_value)  # type:ignore
        self.canvas.size = t_value
        self.fullscreen = False
        self._main.scheduler.schedule_action(self.__place_object)

    @property
    def fullscreen(self) -> bool:
        return self.__fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        self.__fullscreen = value
        self._main.scheduler.schedule_action(self.__update_window_state)

    @property
    def caption(self) -> str:
        return self.__caption

    @caption.setter
    def caption(self, value: str) -> None:
        self.__caption = value
        self._main.scheduler.schedule_action(self.__update_caption)

    @ETKBaseTkObject.visibility.setter
    def visibility(self, value: bool) -> None:
        ETKBaseTkObject.visibility.fset(self, value)  # type: ignore
        self._main.scheduler.schedule_action(self.__update_visibility)

    @property
    def topmost(self) -> bool:
        return self.__topmost

    @topmost.setter
    def topmost(self, value: bool) -> None:
        self.__topmost = value
        self._main.scheduler.schedule_action(self.__update_topmost)

    # endregion
    # region Methods
        
    def __update_window_state(self):
        if self.__fullscreen:
            self._tk_object.state("zoomed")
        else:
            self._tk_object.state("normal")
    
    def __update_caption(self):
        self._tk_object.title(self.__caption)
    
    def __update_visibility(self):
        if not self.visibility:
            self._tk_object.withdraw()
        else:
            self._tk_object.deiconify()
            self.force_focus()
    
    def __update_topmost(self):
        self._tk_object.attributes('-topmost', self.__topmost)  # type:ignore
    
    def __update_focus(self):
        self._tk_object.attributes('-topmost', 1)  # type:ignore
        self._tk_object.focus_force()
        self._tk_object.attributes('-topmost', self.__topmost)  # type:ignore

    @abstractmethod
    def _add_elements(self) -> None:
        pass

    def run(self) -> None:
        self._tk_object.mainloop()

    def exit(self) -> None:
        self._handle_event(ETKEventData(self, ETKWindowEvents.EXIT), ignore_scheduler=True)
        if not self.exit_locked and not self.exit_ignore_next:
            self._main.scheduler.exit()
        if self.exit_ignore_next:
            self.exit_ignore_next = False

    def update_gui(self) -> None:
        self._main.scheduler.handle_actions()

    def force_focus(self) -> None:
        self._main.scheduler.schedule_action(self.__update_focus)

    def exec_gui_function(self, function: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self._tk_object.after(0, lambda: function(*args, **kwargs))

    def _update_background_color(self):
        super()._update_background_color()
        self.canvas.background_color = self.background_color

    def __configure_event_handler(self, event: Any = None):  # type:ignore
        if self.fullscreen:
            self.fullscreen = True

    def __place_object(self) -> None:
        self._tk_object.geometry(
            f"{int(self.size.x)}x{int(self.size.y)}+{int(self.pos.x)}+{int(self.pos.y)}")

    def _handle_tk_event(self, event: Event) -> None:  # type:ignore
        match event.type:
            case EventType.KeyPress:
                self._handle_event(ETKEventData(self, ETKWindowEvents.KEY_PRESSED, tk_event=event, state=event.state, keysym=event.keysym, keycode=event.keycode, keychar=event.char, rel_pos=get_rel_event_pos(event, self._main.scale_factor), abs_pos=get_abs_event_pos(event, self._main.root_tk_object, self._main.scale_factor)))
                return
            case EventType.KeyRelease:
                self._handle_event(ETKEventData(self, ETKWindowEvents.KEY_RELEASED, tk_event=event, state=event.state, keysym=event.keysym, keycode=event.keycode, keychar=event.char, rel_pos=get_rel_event_pos(event, self._main.scale_factor), abs_pos=get_abs_event_pos(event, self._main.root_tk_object, self._main.scale_factor)))
                return
            case EventType.FocusIn:
                self._handle_event(ETKEventData(self, ETKWindowEvents.FOCUS_IN, tk_event=event))
                return
            case EventType.FocusOut:
                self._handle_event(ETKEventData(self, ETKWindowEvents.FOCUS_OUT, tk_event=event))
                return
            case _:
                pass
        super()._handle_tk_event(event)  # type:ignore

    # endregion


ETKMain = ETKMainWindow.ETKMain
