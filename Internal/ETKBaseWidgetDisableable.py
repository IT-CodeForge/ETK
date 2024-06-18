from typing import Any

from .ETKMain import ETKMain
from ..Vector2d import Vector2d
from .ETKBaseWidget import ETKBaseWidget


class ETKBaseWidgetDisableable(ETKBaseWidget):
    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, visibility: bool, enabled: bool, background_color: int, **kwargs: Any) -> None:
        super().__init__(main=main, pos=pos, size=size, visibility=visibility, background_color=background_color, **kwargs)

        self._enabled = not enabled
        self.enabled = enabled

    # region Properties

    @ETKBaseWidget.enabled.setter
    def enabled(self, value: bool) -> None:
        """ """
        if self._enabled == value:
            return
        self._enabled = value
        self._main.scheduler.schedule_action(self._update_enabled)

    # endregion
