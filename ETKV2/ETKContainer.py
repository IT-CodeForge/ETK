from __future__ import annotations
from typing import Literal
from ETKV2.ETKBaseWidget import ETKBaseWidget

from ETKV2.vector2d import vector2d

from .ETKBaseContainer import Alignments, _SubAlignments, ContainerSize, SizeError, PosError, ETKBaseContainer #type:ignore


class ETKContainer(ETKBaseContainer):
    def __init__(self, pos: vector2d = vector2d(0, 0), size: ContainerSize = ContainerSize(0, 0, True, True), background_color: int = 11184810) -> None:
        ETKBaseContainer.__init__(self, pos, size, background_color)
        self._element_alignments: dict[ETKBaseWidget, Alignments] = {}
    
    @ETKBaseContainer.size.setter
    def size(self, value: ContainerSize | vector2d) -> None:
        ETKBaseContainer.size.fset(self, value) #type:ignore
        try:
            self.__update_all_element_pos()
        except ValueError:
            raise SizeError(
                f"size of container {self} is too small\ncontainer: size: {self.size}")

    def add_element(self, element: ETKBaseWidget, alignment: Alignments = Alignments.TOP_LEFT):
        self._element_alignments.update({element: alignment})
        ETKBaseContainer.add_element(self, element)
        self.__update_all_element_pos()
    
    def _calculate_rel_element_pos_part(self, element: ETKBaseWidget, index: Literal[0, 1]) -> float:
        match self._element_alignments[element].value[index]:
            case _SubAlignments.MIN:
                return element.pos[index]
            case _SubAlignments.MIDDLE:
                return  0.5 * self.size[index] - 0.5 * element.size[index] + element.pos[index]
            case _SubAlignments.MAX:
                return self.size[index] - element.size[index] + element.pos[index]
        
    def __update_all_element_pos(self) -> None:
        elements = [e for e in self._element_rel_pos.keys() if e.abs_enabled]

        max_size = [0, 0]

        if len(elements) == 0:
            return

        for e in elements:
            alignment = self._element_alignments[e].value
            for i, sal in enumerate(alignment):
                if sal == _SubAlignments.MAX:
                    size = e.size[i] + e.pos[i] * -1
                elif sal == _SubAlignments.MIDDLE:
                    size = e.size[i] + abs(e.pos[i]) * 2
                else:
                    size = e.size[i] + e.pos[i]
                if size > max_size[i]:
                    max_size[i] = int(size)
        
        if self.size.dynamic_x:
            self._container_size.x = max_size[0]
        if self.size.dynamic_y:
            self._container_size.y = max_size[1]
        
        for e in elements:
            self._element_rel_pos[e] = self._calculate_rel_element_pos(e)
            self.__validate_size_pos(self._element_rel_pos[e], e.size)
            e._update_pos()
        
        
        
            
    
    def __validate_size_pos(self, rel_pos: vector2d, size: vector2d):
        s_size = self.size

        if s_size.x > self.size.x or s_size.y > self.size.y:
            raise SizeError(
                f"size is outside of container {self}\nparameter: size: {size}; container: abs_pos: size: {self.size}")

        if rel_pos.x + size.x > s_size.x or rel_pos.y + size.y > s_size.y or rel_pos.x < 0 or rel_pos.y < 0:
            raise PosError(
                f"pos is outside of container {self}\nparameter: rel_pos: {rel_pos}, size: {size}; container: size: {self.size}")
    
    def _validate_pos(self, element: ETKBaseWidget):
        self.__update_all_element_pos()
        ETKBaseContainer._validate_size(self, element)

    def _validate_size(self, element: ETKBaseWidget):
        self.__update_all_element_pos()
        ETKBaseContainer._validate_size(self, element)