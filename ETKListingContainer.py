from __future__ import annotations
from enum import Enum, auto
from typing import Any

from .Internal.ETKMain import ETKMain

from .Internal.ETKBaseWidget import ETKBaseWidget
from .ETKContainer import ETKContainerSize
from .Vector2d import Vector2d
from .Internal.ETKBaseContainer import ETKBaseContainer, SizeError


class ElementPosLockedError(AttributeError):
    pass


class ETKListingTypes(Enum):
    TOP_TO_BOTTOM = auto()
    BOTTOM_TO_TOP = auto()
    LEFT_TO_RIGHT = auto()
    RIGHT_TO_LEFT = auto()


class ETKListingContainer(ETKBaseContainer):
    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: ETKContainerSize = ETKContainerSize(0, 0, True, True), alignment: ETKBaseContainer.Alignments = ETKBaseContainer.Alignments.TOP_LEFT, listing_type: ETKListingTypes = ETKListingTypes.TOP_TO_BOTTOM, offset: int = 10, *, visibility: bool = True, enabled: bool = True, background_color: int = 0xAAAAAA, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__alignment = alignment
        self.__listing_type = listing_type
        self.__offset = offset

        super().__init__(main=main, pos=pos, csize=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

        self.__calulate_excess_space(0)

    # region Methods

    def add_element(self, element: ETKBaseWidget) -> None:
        self.__validate_element_size(Vector2d(), element.size)
        super().add_element(element)

    def _update_all_element_pos(self) -> None:
        if self.__listing_type in [ETKListingTypes.TOP_TO_BOTTOM, ETKListingTypes.BOTTOM_TO_TOP]:
            listing_dir_index = 1
            non_listing_dir_index = 0
        else:
            listing_dir_index = 0
            non_listing_dir_index = 1

        elements = [e for e in self._element_rel_pos.keys() if e.abs_visibility]
        # print([(e.abs_visibility, e) for e in self._element_rel_pos.keys()]) #NOTE
        sizes = [e.size for e in elements]

        if len(elements) == 0:
            return

        listing_dir_size = sum([s[listing_dir_index]
                               for s in sizes]) + self.__offset * (len(sizes) - 1)
        non_listing_dir_size = max([s[non_listing_dir_index] for s in sizes])

        needed_size = Vector2d()
        needed_size[listing_dir_index] = listing_dir_size
        needed_size[non_listing_dir_index] = non_listing_dir_size

        if self.csize.dynamic_x:
            self._container_size.x = int(
                needed_size.x) + self.csize.padding_x_l + self.csize.padding_x_r
        if self.csize.dynamic_y:
            self._container_size.y = int(
                needed_size.y) + self.csize.padding_y_o + self.csize.padding_y_u

        vec_size = self.csize.vec
        self._size = vec_size
        if self.parent != None:
            self.parent._validate_size(self, vec_size)
        #self._background.size = self.size

        self.__calulate_excess_space(int(listing_dir_size))

        if listing_dir_size > self.csize[listing_dir_index] or non_listing_dir_size > self.csize[non_listing_dir_index]:
            raise SizeError(
                f"size of container {self} is too small\ncontainer: size: {self.csize}; needed: {needed_size}")

        listing_dir_pos = self.__calculate_pos_part(
            listing_dir_index, listing_dir_size, (self.csize[4+2*listing_dir_index], self.csize[5+2*listing_dir_index]))

        if self.__listing_type in [ETKListingTypes.BOTTOM_TO_TOP, ETKListingTypes.RIGHT_TO_LEFT]:
            elements = elements[::-1]

        for e in elements:
            non_listing_dir_pos = self.__calculate_pos_part(
                non_listing_dir_index, e.size[non_listing_dir_index], (self.csize[4+2*non_listing_dir_index], self.csize[5+2*non_listing_dir_index]))
            pos = Vector2d()
            pos[listing_dir_index] = listing_dir_pos
            pos[non_listing_dir_index] = non_listing_dir_pos
            self._element_rel_pos[e] = pos
            e._pos = pos
            self._main.scheduler.schedule_action(e._update_pos)
            listing_dir_pos += e.size[listing_dir_index] + self.__offset

    def __calculate_pos_part(self, index: int, size_part: float, padding_part: tuple[float, float]) -> float:
        match self.__alignment.value[index]:
            case ETKBaseContainer.Alignments._SubAlignments.MIN:  # type:ignore
                return padding_part[0]
            case ETKBaseContainer.Alignments._SubAlignments.MIDDLE:  # type:ignore
                return 0.5 * (self.csize[index] - padding_part[0] - padding_part[1]) - 0.5 * size_part + padding_part[0]
            case ETKBaseContainer.Alignments._SubAlignments.MAX:  # type:ignore
                return self.csize[index] - size_part - padding_part[1]

    def __validate_element_size(self, old_size: Vector2d, new_size: Vector2d):
        needed_space = new_size - old_size

        if self.__listing_type in [ETKListingTypes.TOP_TO_BOTTOM, ETKListingTypes.BOTTOM_TO_TOP]:
            listing_dir_index = 1
            non_listing_dir_index = 0
            listing_dir_dynamic = self.csize.dynamic_y
            non_listing_dir_dynamic = self.csize.dynamic_x
        else:
            listing_dir_index = 0
            non_listing_dir_index = 1
            listing_dir_dynamic = self.csize.dynamic_x
            non_listing_dir_dynamic = self.csize.dynamic_y

        if needed_space[listing_dir_index] > 0 and needed_space[listing_dir_index] > self.__excess_space and not listing_dir_dynamic:
            raise SizeError(
                f"size of container {self} is too small\ncontainer: size: {self.csize}")
        if new_size[non_listing_dir_index] > self.size[non_listing_dir_index] and not non_listing_dir_dynamic:
            raise SizeError(
                f"size of container {self} is too small\ncontainer: size: {self.csize}")

    def __calulate_excess_space(self, used_space: int):
        if self.__listing_type in [ETKListingTypes.TOP_TO_BOTTOM, ETKListingTypes.BOTTOM_TO_TOP]:
            listing_dir_index = 1
        else:
            listing_dir_index = 0

        if listing_dir_index == 0:
            padding = self.csize.padding_x_r + self.csize.padding_x_l
        else:
            padding = self.csize.padding_y_o + self.csize.padding_y_u

        self.__excess_space = self.csize[listing_dir_index] - used_space - padding

    def insert_element(self, element: ETKBaseWidget, index: int) -> None:
        self._prepare_element_add(element)

        element_list = list(self._element_rel_pos.items())
        element_list.insert(index, (element, Vector2d()))
        self._element_rel_pos = dict(element_list)

        self._main.scheduler.schedule_action(self._update_all_element_pos)
        self._main.scheduler.schedule_action(element._update_visibility)

    # region child validation methods

    def _validate_pos(self, element: ETKBaseWidget, new_pos: Vector2d) -> None:
        raise ElementPosLockedError(
            f"pos of element {element} is locked by ListingContainer {self}")

    def _validate_size(self, element: ETKBaseWidget, new_size: Vector2d) -> None:
        self.__validate_element_size(element.size, new_size)
        super()._validate_size(element, new_size)

    # endregion
    # endregion
