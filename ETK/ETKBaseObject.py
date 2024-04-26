from asyncio import events
from enum import Enum, auto
from abc import abstractmethod
from tkinter import Event, EventType
from typing import Any, Callable
import logging

#this is for logging purposses, if you don't want it, set "log" to False
LOG = True
if LOG:
    my_logger = logging.getLogger("BaseObject_logger")
    my_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler('project.log',mode='w')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
#-------------------------------------------------------------------------

class BaseEvents(Enum):
    MOUSE_DOWN   = auto()
    MOUSE_UP     = auto()
    HOVERED      = auto()
    LEAVE        = auto()
    CONFIGURED   = auto()

class ETKBaseObject:
    def __init__(self) -> None:
        self.object_id
        self._parent = None
        self._event_lib:dict[str, list[dict[str, Any]]] = {
            "<ButtonPress>":[],
            "<ButtonRelease>":[],
            "<KeyPress>":[],
            "<KeyRelease>":[],
            "<Enter>":[],
            "<Leave>":[],
            "<Motion>":[],
            "<Configure>":[],
            "<Custom>":[]
        }
        self.__type_trans = {
            EventType.KeyPress:"<KeyPress>",
            EventType.KeyRelease:"<KeyRelease>",
            EventType.ButtonPress:"<ButtonPress>",
            EventType.ButtonRelease:"<ButtonRelease>",
            EventType.Motion:"<Motion>",
            EventType.Enter:"<Enter>",
            EventType.Leave:"<Leave>",
            EventType.Configure:"<Configure>"
        }
        self.__event_trans:dict[BaseEvents, list[str|Callable[...,None]]] = {
            BaseEvents.MOUSE_DOWN:"<ButtonPress>",
            BaseEvents.MOUSE_UP:"<ButtonRelease>",
            BaseEvents.HOVERED:"<Enter>",
            BaseEvents.LEAVE:"<Leave>",
            BaseEvents.CONFIGURED:"<Configure>"
        }
        self.__event_truth_funcs = {
            BaseEvents.MOUSE_DOWN:lambda event, object_id : True,
            BaseEvents.MOUSE_UP:lambda event, object_id : True,
            BaseEvents.HOVERED:lambda event, object_id : True,
            BaseEvents.LEAVE:lambda event, object_id : True,
            BaseEvents.CONFIGURED:lambda event, object_id : True
        }
    
    @property
    def parent(self)->Any:
        """
        READ-ONLY
        """
        return self._parent
    
    def add_event(self, event_type:BaseEvents, eventhandler:Callable[...,None], sequence:str=None, truth_func:Callable[..., None]|None=None):
        if type(event_type) == str:
            sequence = event_type
        if sequence == None:
            sequence = self.__event_trans[event_type]
        if truth_func == None:
            truth_func = self.__event_truth_funcs.get(event_type, lambda event, object_id : False)
        append_dict = {
            "eventhandler":eventhandler,
            "event_type": event_type,
            "truth_func": truth_func
        }
        if sequence not in self._event_lib.keys():
            self._event_lib[sequence] = []
        self._event_lib[sequence].append(append_dict)
        if len(self._event_lib[sequence]) == 1 and type(event_type) != str:
            self.object_id.bind(sequence, self._eventhandler)

    def remove_event(self, event_type:BaseEvents, eventhandler:Callable[..., None], sequence:str=None):
        if sequence == None:
            sequence = self.__event_trans[event_type]
        for event in self._event_lib[self.__event_trans[event_type]]:
            if event.get("event_type") == event_type and event.get("eventhandler") == eventhandler:
                self._event_lib[sequence].remove(event)
                if len(self._event_lib[sequence]) == 0 and sequence != "<Custom>":
                    self.object_id.unbind(sequence)
                break
        
    def _eventhandler(self, event:Event):
        event_type = 0
        if type(event) == Event:
            event_type = self.__type_trans[event.type]
        else:
            event_type = event
        if event_type not in self._event_lib.keys():
            return
        for dict in self._event_lib[event_type]:
            if dict.get("truth_func", lambda event, object_id: False)(event, self.object_id):
                try:
                    dict.get("eventhandler")(self, dict.get("event_type"), event)
                    continue
                except:
                    pass
                try:
                    params = {"object":self, "event_type":dict.get("event_typ"), "event":event}
                    dict.get("eventhandler")(params)
                    continue
                except:
                    pass
                try:
                    dict.get("eventhandler")()
                except:
                    ret_val = dict.get("eventhandler").__code__.co_varnames
                    name = dict.get("eventhandler").__name__
                    raise TypeError(f"Invalid parametercount for event function ({name}) (can only be 0,1 or 3 self is not included),parameters: {ret_val}")