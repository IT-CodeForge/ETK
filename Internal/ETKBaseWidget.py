from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional

from ..Vector2d import Vector2d
from .ETKBaseObject import ETKBaseObject

if TYPE_CHECKING:
    from .ETKMain import ETKMain


class ETKBaseWidget(ETKBaseObject):
    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, visibility: bool, background_color: int, **kwargs: Any) -> None:
        self._parent: Optional[ETKBaseWidget] = None
        self._enabled: bool = True
        self.__akt_visibility: bool
        self.__akt_pos: Vector2d
        self.__akt_size: Vector2d
        self.__akt_enabled: bool

        super().__init__(main=main, pos=pos, size=size, visibility=visibility, background_color=background_color, **kwargs)

    # region Properties

    @property
    def parent(self) -> Optional[ETKBaseWidget]:
        return self._parent

    @property
    def abs_pos(self) -> Vector2d:
        """READ-ONLY"""
        if self._parent != None:
            return self._parent._get_childs_abs_pos(self)
        return self.pos

    @property
    def abs_visibility(self) -> bool:
        """READ-ONLY"""
        if self._parent != None:
            return self.visibility and self._parent.abs_visibility
        return self.visibility

    @ETKBaseObject.pos.setter
    def pos(self, value: Vector2d):
        if self._pos == value:
            return
        if self.parent != None:
            self.parent._validate_pos(self, value)
        ETKBaseObject.pos.fset(self, value)  # type:ignore

    @ETKBaseObject.size.setter
    def size(self, value: Vector2d):
        if self.size == value:
            return
        if self.parent != None:
            self.parent._validate_size(self, value)
        ETKBaseObject.size.fset(self, value)  # type:ignore

    @ETKBaseObject.visibility.setter
    def visibility(self, value: bool):
        if self.visibility == value:
            return
        if self.parent != None:
            self.parent._validate_visibility(self, value)
        ETKBaseObject.visibility.fset(self, value)  # type:ignore

    @property
    def enabled(self) -> bool:
        """READ-ONLY"""
        return self._enabled

    @property
    def abs_enabled(self) -> bool:
        """READ-ONLY"""
        if self._parent != None:
            return self._enabled and self._parent._enabled
        return self._enabled

    # endregion
    # region Methods

    def detach_from_parent(self) -> None:
        if self._parent is None:
            raise ValueError(f"{self} has no parent!")
        self._parent._detach_child(self)

    # region update event methods

    def _update_pos(self) -> bool:
        abspos = self.abs_pos
        try:
            if abspos == self.__akt_pos:
                return False
        except:
            pass
        self.__akt_pos = abspos

        if abspos.x < 0 or abspos.y < 0:
            raise RuntimeError(
                f"element {self} is outside of window\nelement: pos: {self.pos}")
        return True

    def _update_size(self) -> bool:
        size = self.size
        try:
            if size == self.__akt_size:
                return False
        except:
            pass
        self.__akt_size = size
        return True

    def _update_visibility(self) -> bool:
        a_vis = self.abs_visibility
        try:
            if a_vis == self.__akt_visibility:
                return False
        except:
            pass
        self.__akt_visibility = a_vis
        return True

    def _update_enabled(self) -> bool:
        a_en = self.abs_enabled
        try:
            if a_en == self.__akt_enabled:
                return False
        except:
            pass
        self.__akt_enabled = a_en
        return True

    # endregion
    # region child validation methods

    def _get_childs_abs_pos(self, child: ETKBaseWidget) -> Vector2d:
        return self.abs_pos + child.pos

    def _detach_child(self, element: ETKBaseWidget) -> None:
        if element._parent != self:
            raise ValueError(f"{self} is not the parent of {element}!")
        element._parent = None

    def _validate_pos(self, element: ETKBaseWidget, new_pos: Vector2d) -> None:
        pass

    def _validate_size(self, element: ETKBaseWidget, new_size: Vector2d) -> None:
        pass

    def _validate_visibility(self, element: ETKBaseWidget, new_visibility: bool) -> None:
        pass

    # endregion
    # endregion
