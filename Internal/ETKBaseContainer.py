from __future__ import annotations
from abc import abstractmethod
from enum import Enum, auto
from typing import Any, Callable

from .ETKMain import ETKMain
from .ETKBaseObject import ETKBaseObject
from .ETKEventData import ETKEventData

from .ETKBaseWidget import ETKBaseWidget
from ..Vector2d import Vector2d
from .ETKBaseWidgetDisableable import ETKBaseWidgetDisableable
from ..ETKCanvas import ETKCanvas


class _ALIGNMENTS_PROTO():
    class _SUB_ALIGNMENTS(Enum):
        MIN = auto()
        MIDDLE = auto()
        MAX = auto()


class ETKBaseContainer(ETKBaseWidgetDisableable):
    # region ExceptionTypes

    class ElementAlreadyAddedError(ValueError):
        pass

    class AddContainerToItselfError(ValueError):
        pass

    class ElementNotPartOfContainerError(ValueError):
        pass

    class SizeError(ValueError):
        pass

    class PosError(ValueError):
        pass

    # endregion
    # region Enums

    class ALIGNMENTS(_ALIGNMENTS_PROTO, Enum):
        TOP_LEFT = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIN, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIN)
        TOP_CENTER = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIDDLE, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIN)
        TOP_RIGHT = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MAX, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIN)
        MIDDLE_LEFT = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIN, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIDDLE)
        MIDDLE_CENTER = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIDDLE, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIDDLE)
        MIDDLE_RIGHT = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MAX, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIDDLE)
        BOTTOM_LEFT = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIN, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MAX)
        BOTTOM_CENTER = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MIDDLE, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MAX)
        BOTTOM_RIGHT = (_ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MAX, _ALIGNMENTS_PROTO._SUB_ALIGNMENTS.MAX)

    # endregion

    class EVENTS(ETKBaseWidgetDisableable.EVENTS):
        pass

    # region Dataclass: ContainerSize

    class ContainerSize():
        def __init__(self, x: int | float = 0, y: int | float = 0, dynamic_x: bool = False, dynamic_y: bool = False, paddings_x_l: int = 0, paddings_x_r: int = 0, paddings_y_o: int = 0, paddings_y_u: int = 0) -> None:
            self.__x: int = 0
            self.__y: int = 0
            self.x = x
            self.y = y
            self.dynamic_x: bool = dynamic_x
            self.dynamic_y: bool = dynamic_y
            self.padding_x_l: int = paddings_x_l
            self.padding_x_r: int = paddings_x_r
            self.padding_y_o: int = paddings_y_o
            self.padding_y_u: int = paddings_y_u

        @property
        def x(self) -> int:
            return self.__x

        @x.setter
        def x(self, value: int | float) -> None:
            self.__x = int(value)

        @property
        def y(self) -> int:
            return self.__y

        @y.setter
        def y(self, value: int | float) -> None:
            self.__y = int(value)

        @classmethod
        def from_vector2d(cls, vec: Vector2d) -> ETKBaseContainer.ContainerSize:
            return cls(vec.x, vec.y)

        def copy(self) -> ETKBaseContainer.ContainerSize:
            return type(self)(self.x, self.y, self.dynamic_x, self.dynamic_y, self.padding_x_l, self.padding_x_r, self.padding_y_o, self.padding_y_u)

        @property
        def vec(self) -> Vector2d:
            """READ-ONLY"""
            return Vector2d(self.x, self.y)

        def __str__(self) -> str:
            return f"<{self.x}, {self.y}, {self.dynamic_x}, {self.dynamic_y}, {self.padding_x_l}, {self.padding_x_r}, {self.padding_y_o}, {self.padding_y_u}>"

        def __setitem__(self, address: int, other: int | bool | float) -> None:
            if address not in range(0, 8):
                raise KeyError("Invalid index")
            match address:
                case 0:
                    self.x = other
                case 1:
                    self.y = other
                case 2:
                    self.dynamic_x = bool(other)
                case 3:
                    self.dynamic_y = bool(other)
                case 4:
                    self.padding_x_l = int(other)
                case 5:
                    self.padding_x_r = int(other)
                case 6:
                    self.padding_y_o = int(other)
                case 7:
                    self.padding_y_u = int(other)
                case _:
                    pass

        def __getitem__(self, address: int) -> int | bool:
            if address not in range(0, 8):
                raise KeyError("Invalid index")
            match address:
                case 0:
                    return self.x
                case 1:
                    return self.y
                case 2:
                    return self.dynamic_x
                case 3:
                    return self.dynamic_y
                case 4:
                    return self.padding_x_l
                case 5:
                    return self.padding_x_r
                case 6:
                    return self.padding_y_o
                case 7:
                    return self.padding_y_u
                case _:
                    raise KeyError

    # endregion

    def __init__(self, *, main: ETKMain, pos: Vector2d, csize: ContainerSize, visibility: bool, enabled: bool, background_color: int, outline_color: int, outline_thickness: int, **kwargs: Any) -> None:
        self._background = ETKCanvas(main, pos, csize.vec, background_color=background_color)
        self._container_size: ETKBaseContainer.ContainerSize = self.ContainerSize(0, 0)
        self._element_rel_pos: dict[ETKBaseWidget, Vector2d] = {}

        super().__init__(main=main, pos=pos, size=csize.vec, visibility=visibility, enabled=enabled, background_color=background_color, **kwargs)

        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.csize = csize

    # region properties

    @ETKBaseWidgetDisableable.pos.setter
    def pos(self, value: Vector2d) -> None:
        ETKBaseWidgetDisableable.pos.fset(self, value)  # type:ignore
        self._background.pos = self.abs_pos

    @ETKBaseWidgetDisableable.size.setter
    def size(self, value: Vector2d):
        self.csize = value

    @property
    def csize(self) -> ContainerSize:  # type:ignore
        return self._container_size.copy()

    @csize.setter
    def csize(self, value: ContainerSize | Vector2d) -> None:
        if type(value) == self.ContainerSize:
            self._container_size = value
            vec = value.vec
        else:
            self._container_size = self.ContainerSize(int(value.x), int(value.y))
            vec = value
        ETKBaseWidgetDisableable.size.fset(self, vec)  # type:ignore

    @property
    def elements(self) -> tuple[ETKBaseWidget, ...]:
        return tuple(self._element_rel_pos.keys())

    @property
    def outline_color(self) -> int:
        return self._background.outline_color

    @outline_color.setter
    def outline_color(self, value: int) -> None:
        self._background.outline_color = value

    @property
    def outline_thickness(self) -> int:
        return self._background.outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value: int) -> None:
        self._background.outline_thickness = value

    @property
    def background_color(self) -> int:
        return self._background.background_color

    @background_color.setter
    def background_color(self, value: int) -> None:
        self._background.background_color = value

    # endregion

    # region Methods

    @abstractmethod
    def _update_all_element_pos(self) -> None:
        pass

    def add_element(self, element: ETKBaseWidget) -> None:
        self._prepare_element_add(element)

        self._element_rel_pos.update({element: Vector2d()})

        self._main.scheduler.schedule_action(element._update_visibility)
        self._main.scheduler.schedule_action(element._update_pos)

        self._main.scheduler.schedule_action(self._update_all_element_pos)

    def _prepare_element_add(self, element: ETKBaseWidget) -> None:
        if element in self._element_rel_pos.keys():
            raise self.ElementAlreadyAddedError(
                f"element {element} is already in container {self}")
        if element == self:
            raise self.AddContainerToItselfError(
                f"cannot add container {self} to itself")

        element._parent = self

        events = [ev for ev in self._event_lib.keys() if len(
            self._event_lib[ev]) != 0]
        for ev in events:
            element.add_event(ev, self.__event_handler)

    def remove_element(self, element: ETKBaseWidget) -> None:
        if element not in self._element_rel_pos.keys():
            raise self.ElementNotPartOfContainerError(
                f"element {element} is not in container {self}")
        self._element_rel_pos.pop(element)
        element._parent = None
        element.pos = Vector2d(0, 0)

        events = [ev for ev in self._event_lib.keys() if len(
            self._event_lib[ev]) != 0]
        for ev in events:
            element.remove_event(ev, self.__event_handler)

        self._main.scheduler.schedule_action(element._update_pos)
        self._main.scheduler.schedule_action(self._update_all_element_pos)

    def add_event(self, event_type: ETKBaseObject.EVENTS, eventhandler: Callable[[], None] | Callable[[ETKEventData], None]) -> None:
        super().add_event(event_type, eventhandler)
        self._background.add_event(event_type, self.__event_handler)
        for e in self._element_rel_pos.keys():
            e.add_event(event_type, self.__event_handler)

    def remove_event(self, event_type: ETKBaseObject.EVENTS, eventhandler: Callable[[], None] | Callable[[ETKEventData], None]) -> None:
        super().remove_event(event_type, eventhandler)
        self._background.remove_event(event_type, self.__event_handler)
        for e in self._element_rel_pos.keys():
            e.remove_event(event_type, self.__event_handler)

    def __event_handler(self, data: ETKEventData) -> None:
        if not isinstance(data.sender, ETKBaseWidget):
            raise TypeError
        if data.sender != self._background:
            data.child_sender = data.sender
        data.sender = self
        self._handle_event(data)

    # region update event methods

    def _update_pos(self) -> bool:
        if not super()._update_pos():
            return False
        self._main.scheduler.schedule_action(self._update_all_element_pos)
        self._background.pos = self.abs_pos
        return True

    def _update_size(self) -> bool:
        if not super()._update_size():
            return False
        self._background.size = self.size
        self._main.scheduler.schedule_action(self._update_all_element_pos)
        return True

    def _update_visibility(self) -> bool:
        if not super()._update_visibility():
            return False
        for e in self._element_rel_pos.keys():
            self._main.scheduler.schedule_action(e._update_visibility)
        self._main.scheduler.schedule_action(self._update_all_element_pos)
        self._background.visibility = self.abs_visibility
        return True

    def _update_enabled(self) -> bool:
        if not super()._update_enabled():
            return False
        for e in self._element_rel_pos.keys():
            self._main.scheduler.schedule_action(e._update_enabled)
        return True

    # endregion
    # region child validation methods

    def _get_childs_abs_pos(self, child: ETKBaseWidget) -> Vector2d:
        if child not in self._element_rel_pos.keys():
            raise self.ElementNotPartOfContainerError(
                f"element {child} is not in container {self}")
        pos = self._element_rel_pos[child]
        return Vector2d(pos.x + self.abs_pos.x, pos.y + self.abs_pos.y)

    def _detach_child(self, element: ETKBaseWidget) -> None:
        self.remove_element(element)

    def _validate_size(self, element: ETKBaseWidget, new_size: Vector2d) -> None:
        self._main.scheduler.schedule_action(self._update_all_element_pos)

    def _validate_pos(self, element: ETKBaseWidget, new_pos: Vector2d) -> None:
        self._main.scheduler.schedule_action(self._update_all_element_pos)

    def _validate_visibility(self, element: ETKBaseWidget, new_visibility: bool) -> None:
        self._main.scheduler.schedule_action(self._update_all_element_pos)

    # endregion
    # endregion
