from .ETKBaseWidget import ETKBaseWidget
from .ETKNoTKEventBase import ETKNoTKEventBase
from .ETKBaseObject import BaseEvents
from .vector2d     import vector2d
from enum         import Enum
import logging

class Alignments(Enum):
    TOP_LEFT      = "00"
    TOP_CENTER    = "01"
    TOP_RIGHT     = "02"
    MIDDLE_LEFT   = "10"
    MIDDLE_CENTER = "11"
    MIDDLE_RIGHT  = "12"
    BOTTOM_LEFT   = "20"
    BOTTOM_CENTER = "21"
    BOTTOM_RIGHT  = "22"

class ETKContainer(ETKNoTKEventBase):
    def __init__(self, gui_object=None):
        super().__init__()
        self.__elements = []
        self.__anchor = vector2d()
        if gui_object == None:
            self.__my_pos = vector2d()
            self.__dimensions = vector2d()
            self.width = None
            self.height = None
        else:
            self.__my_pos = gui_object.pos
            self.__dimensions = vector2d(gui_object.width, gui_object.height)
    
    @property
    def anchor(self)->vector2d:
        return self.__anchor
    
    @anchor.setter
    def anchor(self, value:vector2d):
        my_anchor = self.__anchor
        self.__anchor = value
        if my_anchor != value:
            self._eventhandler(BaseEvents.CONFIGURED)
        self.__place_elements()
        

    @property
    def pos(self)->vector2d:
        return self.__my_pos
    
    @pos.setter
    def pos(self, value:vector2d):
        my_pos = self.__my_pos
        self.__my_pos = value
        if my_pos != value:
            self._eventhandler(BaseEvents.CONFIGURED)
        self.__place_elements()
    
    @property
    def width(self)->int:
        if self.__dimensions.x == -1:
            return max([e[0].pos.x + e[0].width for e in self.__elements])
        return self.__dimensions.x
    
    @width.setter
    def width(self, value:int):
        if type(value) == int and value < 0:
            raise ValueError("objects must have a positive width")
        if value == None:
            value = -1
        my_width = self.__dimensions.x
        self.__dimensions.x = value
        if my_width != value:
            self._eventhandler(BaseEvents.CONFIGURED)
        self.__place_elements()
    
    @property
    def height(self)->int:
        if self.__dimensions.y == -1:
            return max([e[0].pos.y + e[0].height for e in self.__elements])
        return self.__dimensions.y
    
    @height.setter
    def height(self, value:int):
        if type(value) == int and value < 0:
            raise ValueError("objects must have a positive height")
        if value == None:
            value = -1
        my_height = self.__dimensions.y
        self.__dimensions.y = value
        if my_height != value:
            self._eventhandler(BaseEvents.CONFIGURED)
        self.__place_elements()
    
    @property
    def visible(self)->bool:
        if True in [e[0].visible for e in self.__elements]:
            return True
        else:
            return False
    
    @visible.setter
    def visible(self, value):
        for element in self.__elements:
            element[0].visible = True
    
    def add_element(self, element, allignment:Alignments=Alignments.TOP_LEFT):
        self.__elements.append([element, vector2d(int(allignment.value[1]), int(allignment.value[0]))])
        self.__place_elements()
        element.add_event("<Detach>", self.__ev_element_detached, lambda event, object_id : True)
        element.add_event(BaseEvents.CONFIGURED, self.__ev_element_configured)
    
    def remove_element(self, element):
        element.remove_event("<Detach>", self.__ev_element_detached, lambda event, object_id : True)
        element.remove_event(BaseEvents.CONFIGURED)
        element.anchor = vector2d(0,0)
        for my_element in self.__elements:
            if my_element[0] == element:
                self.__elements.remove(my_element)
                break

    def __place_elements(self):
        if len(self.__elements) == 0:
            return
        max_x = max([e[0].pos.x + e[0].width for e in self.__elements])
        max_y = max([e[0].pos.y + e[0].height for e in self.__elements])
        my_dim = self.__dimensions
        self.__dimensions = vector2d(max_x if self.__dimensions.x == -1 else self.__dimensions.x,
                                     max_y if self.__dimensions.y == -1 else self.__dimensions.y)
        for element in self.__elements:
            if element[0].pos.x + element[0].width > self.__dimensions.x or element[0].pos.y + element[0].height > self.__dimensions.y:
                continue 
            element_pos = (self.__dimensions - vector2d(element[0].width, element[0].height)) * element[1] / 2
            element[0].anchor = self.__my_pos + self.anchor + element_pos + element[0].pos
        self.__dimensions = my_dim
    
    def __ev_element_configured(self):
        self.__place_elements()
    
    def __ev_element_detached(self, params):
        my_object = params.get("object_id")
        if type(my_object) == ETKBaseWidget:
            for element in self.__elements:
                if element.object_id == my_object:
                    my_object = element
                    break
        for my_element in self.__elements:
            if my_element[0] == element:
                self.__elements.remove(my_element)
                break
        my_object.anchor = vector2d()
        my_object.pos = vector2d()
        my_object.visible = False
    
    def detach(self):
        self._eventhandler("<Detach>")