from __future__ import annotations
from typing import Any, Type
from warnings import warn


class _SubclassableEnumType(type):
    _members: dict[str, Any]
    _in_construction: bool

    def __new__(metacls, name: str, bases: tuple[Type[Any]], classdict: dict[str, Any], **kwds: Any) -> _SubclassableEnumType:
        t_member_keys = classdict.get("_values", {})
        cls = type.__new__(metacls, name, bases, classdict)
        cls._in_construction = True

        _members = {e: cls(e, classdict["_values"][e]) for e in t_member_keys}
        for k, v in _members.items():
            setattr(cls, k, v)
            if k not in classdict.get("__annotations__", {}).keys():
                warn(f"missing annotation for {v} in {type(v)}")

        for a in classdict.get("__annotations__", {}).keys():
            if a not in _members.keys() and a not in ["_values"]:
                warn(f"missing value for {name}.{a}")

        cls._members = {}
        for b in bases:
            cls._members.update(getattr(b, "_members", {}))
        cls._members.update(_members)

        cls._in_construction = False
        return cls

    def __setattr__(cls, name: str, value: Any):
        if name != "_in_construction" and not cls._in_construction:
            raise AttributeError(f"cannot alter class {cls.__name__} after creation")
        super().__setattr__(name, value)

    def __iter__(cls):
        return iter(cls._members.values())

    def __len__(cls):
        return len(cls._members.keys())

    def __contains__(cls, value: object) -> bool:
        return value in cls._members.values()

    def __repr__(cls) -> str:
        return f"{type(cls).__name__}({', '.join(repr(m) for m in cls._members.values())})"

    def __str__(cls) -> str:
        return f"{type(cls).__name__}({', '.join(str(m) for m in cls._members.values())})"


class SubclassableEnum(metaclass=_SubclassableEnumType):
    _values: dict[str, Any] = {}

    def __init__(self, name: str = "", value: Any = None) -> None:
        if not self._in_construction:  # type:ignore
            raise RuntimeError(f"class {type(self).__name__} is static")
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value

    def __str__(self) -> str:
        return f"{type(self).__name__}.{self._name}: {self._value}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}.{self._name}"
