from typing import Any

from ..ETKMainWindow import ETKMain
from ..Vector2d import Vector2d
from .ETKBaseTkWidget import ETKBaseTkWidget
from .ETKBaseWidgetDisableable import ETKBaseWidgetDisableable


class ETKBaseTkWidgetDisableable(ETKBaseWidgetDisableable, ETKBaseTkWidget):
    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, visibility: bool, enabled: bool, background_color: int, outline_color: int, outline_thickness: int, **kwargs: Any) -> None:
        super().__init__(main=main, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

    # region Methods
    # region update event methods

    def _update_enabled(self) -> bool:
        if not super()._update_enabled():
            return False
        if self.abs_enabled:
            self._tk_object["state"] = "normal"
        else:
            self._tk_object["state"] = "disabled"
        return True

    # endregion
    # endregion
