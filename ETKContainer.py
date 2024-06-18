from __future__ import annotations
from typing import Any, Literal

from .Internal.ETKMain import ETKMain
from .Internal.ETKBaseWidget import ETKBaseWidget

from .Vector2d import Vector2d

from .Internal.ETKBaseContainer import ETKContainerSize, SizeError, PosError, ETKBaseContainer


class ETKContainer(ETKBaseContainer):
    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: ETKContainerSize = ETKContainerSize(0, 0, True, True), *, visibility: bool = True, enabled: bool = True, background_color: int = 0xAAAAAA, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        super().__init__(main=main, pos=pos, csize=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)
        self.__element_alignments: dict[ETKBaseWidget, ETKBaseContainer.Alignments] = {}

    # endregion
    # region Methods

    def _update_all_element_pos(self) -> None:
        elements = [e for e in self._element_rel_pos.keys() if e.abs_visibility]

        max_size = [0, 0]

        if len(elements) == 0:
            return

        for e in elements:
            alignment = self.__element_alignments[e].value
            for i, sal in enumerate(alignment):
                if sal == ETKBaseContainer.Alignments._SubAlignments.MAX:  # type:ignore
                    size = e.size[i] + e.pos[i] * -1
                elif sal == ETKBaseContainer.Alignments._SubAlignments.MIDDLE:  # type:ignore
                    size = e.size[i] + abs(e.pos[i]) * 2
                else:
                    size = e.size[i] + e.pos[i]
                if size > max_size[i]:
                    max_size[i] = int(size)

        if self.csize.dynamic_x:
            self._container_size.x = max_size[0] + self.csize.padding_x_r
        if self.csize.dynamic_y:
            self._container_size.y = max_size[1] + self.csize.padding_y_u

        vec_size = self.csize.vec
        self._size = vec_size
        if self.parent != None:
            self.parent._validate_size(self, vec_size)
        self._background.size = self.size

        for e in elements:
            self._element_rel_pos[e] = self._calculate_rel_element_pos(e)
            self.__validate_size_pos(self._element_rel_pos[e], e.size)
            self._main.scheduler.schedule_action(e._update_pos)

    def _calculate_rel_element_pos(self, element: ETKBaseWidget) -> Vector2d:
        x = self._calculate_rel_element_pos_part(
            element, 0, self.csize.padding_x_r)
        y = self._calculate_rel_element_pos_part(
            element, 1, self.csize.padding_y_u)
        return Vector2d(x, y)

    def _calculate_rel_element_pos_part(self, element: ETKBaseWidget, index: Literal[0, 1], padding_part: float) -> float:
        match self.__element_alignments[element].value[index]:
            case ETKBaseContainer.Alignments._SubAlignments.MIN:  # type:ignore
                return element.pos[index]
            case ETKBaseContainer.Alignments._SubAlignments.MIDDLE:  # type:ignore
                return 0.5 * self.csize[index] - 0.5 * element.size[index] + element.pos[index]
            case ETKBaseContainer.Alignments._SubAlignments.MAX:  # type:ignore
                return self.csize[index] - element.size[index] + element.pos[index] - padding_part

    def __validate_size_pos(self, rel_pos: Vector2d, size: Vector2d) -> None:
        s_size = self.csize

        if (size.x > s_size.x and not s_size.dynamic_x) or (size.y > s_size.y and not s_size.dynamic_y):
            raise SizeError(
                f"size is outside of container {self}\nparameter: size: {size}; container: abs_pos: size: {self.size}")

        if (rel_pos.x + size.x > s_size.x and not s_size.dynamic_x) or (rel_pos.y + size.y > s_size.y and not s_size.dynamic_y) or rel_pos.x < 0 or rel_pos.y < 0:
            raise PosError(
                f"pos is outside of container {self}\nparameter: rel_pos: {rel_pos}, size: {size}; container: size: {self.size}")

    def add_element(self, element: ETKBaseWidget, alignment: ETKBaseContainer.Alignments = ETKBaseContainer.Alignments.TOP_LEFT) -> None:
        self.__element_alignments.update({element: alignment})
        self.__validate_size_pos(element.pos, element.size)
        super().add_element(element)

    def remove_element(self, element: ETKBaseWidget) -> None:
        super().remove_element(element)
        self.__element_alignments.pop(element)

    def _validate_size(self, element: ETKBaseWidget, new_size: Vector2d) -> None:
        self.__validate_size_pos(element.pos, new_size)
        super()._validate_size(element, new_size)

    def _validate_pos(self, element: ETKBaseWidget, new_pos: Vector2d) -> None:
        self.__validate_size_pos(new_pos, element.size)
        super()._validate_pos(element, new_pos)

    # endregion
