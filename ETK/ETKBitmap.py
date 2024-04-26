from typing import Iterable
from .vector2d import vector2d
from tkinter  import Label, PhotoImage, Tk
from .ETKNoTKEventBase import ETKNoTKEventBase

class ETKBitmap(ETKNoTKEventBase):
    def __init__(self, my_tk:Tk, pos_x:int=0, pos_y:int=0, width:int=100, height:int=100) -> None:
        super().__init__()
        self.object_id = PhotoImage(width=width,height=height)
        self.__container = Label(my_tk, text="", image=self.object_id)
        self.__object_pos = vector2d(pos_x, pos_y)
        self.__dimensions = vector2d(width, height)
        self.__place_object()

    def __getitem__(self, index:vector2d|Iterable)->int:
        if type(index) in [vector2d, Iterable]:
            raise TypeError(f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        if type(index) == vector2d:
            index = [index.x,index.y]
        self.object_id.get(*index)
    
    def __setitem__(self, index:vector2d|Iterable, value:int)->int:
        if type(index) in [vector2d, Iterable]:
            raise TypeError(f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        if type(index) == vector2d:
            index = [index.x,index.y]
        if type(value) != int:
            raise TypeError(f"You can only assign an integer to a color")
        if value > 0xFFFFFF:
            raise ValueError(f"The maximum color is 0xFFFFFF, inputted value: {hex(value)}")
        color = "#%06x"%value
        self.object_id.put(color, index)

    
    @property
    def abs_pos(self)->vector2d:
        """
        READ-ONLY \r\n
        the absolute position in the Window
        """
        return self.__object_pos + vector2d() if self.parent == 0 else self._parent.abs_pos
    
    @property
    def pos(self)->vector2d:
        """
        The position relative to the parent (eg. if object, is added to Container, the Container becomes its parent)\r\n
        WARNING: Some Parents may lock the position and make it READ-ONLY
        """
        return self.__object_pos
    
    @pos.setter
    def pos(self, value:vector2d):
        if self.parent != None and not self._parent._validate("move", self):
            return
        self.__place_object(value)
        if self.parent != None and self._parent._validate("move", self):
            self._parent._element_changed(self)
    
    @property
    def width(self)->int:
        """
        The width of the element
        """
        return int(self.__dimensions.x)
    
    @width.setter
    def width(self, value:int):
        if self.parent != None and not self._parent._validate("width", self):
            return
        self.__dimensions.x = value
        self.__place_object()
        if self.parent != None and self._parent._validate("width", self):
            self._parent._element_changed(self)
    
    @property
    def height(self)->int:
        """
        the height of the element
        """
        return int(self.__dimensions.y)
    
    @height.setter
    def height(self, value:int):
        if self.parent != None and not self._parent._validate("height", self):
            return
        self.__dimensions.y = value
        self.__place_object()
        if self.parent != None and self._parent._validate("height", self):
            self._parent._element_changed(self)
    
    @property
    def visible(self)->bool:
        """
        If the element, is drawn on the window\r\n
        WARNING: When parents are set invisible the children are never drawn, but they remember their status and their status can still be changed, so upon making the parent visible again, only the children which,
        before or during the the parent being invisible were set to visible will be drawn
        """
        return self.__visibility
    
    @visible.setter
    def visible(self, value:bool):
        if value:
            self.__visibility = True
            if self.parent != None and not self._parent._validate("visible", self):
                return
            self.__place_object()
            self._eventhandler("<Visible>")
        else:
            self.__visibility = False
            if self.parent != None and not self._parent._validate("visible", self):
                return
            self.object_id.place_forget()
            self._eventhandler("<Visible>")

    def move(self, mov_vec:vector2d):
        """
        moves an element from its current position, by the mov_vec
        """
        self.pos = self.__object_pos+mov_vec

    def __place_object(self, pos:vector2d|None=None, dim:vector2d|None=None):
        if pos == None:
            pos = self.__object_pos
        else:
            self.__object_pos = pos
        if dim == None:
            dim = self.__dimensions
        else:
            self.__dimensions = dim
        anchor = vector2d()
        if self.parent != None:
            anchor = self._parent.abs_pos
        self.__container.place(x=pos.x + anchor.x, y=pos.y + anchor.y, width=dim.x, height=dim.y)
        #self.object_id.configure(width=dim.x,height=dim.y)
    
    def draw_rect(self, top_left:vector2d, bottom_right:vector2d, color:int):
        self.object_id.put("#%06x"%color,to=(int(top_left.x),int(top_left.y) , int(bottom_right.x),int(bottom_right.y)))
        self.__container.configure(image=self.object_id)
    
    def clear(self):
        self.object_id.blank()
    
    def detach(self):
        """
        detaches the object, from its parent
        """
        self._eventhandler("<Detach>")