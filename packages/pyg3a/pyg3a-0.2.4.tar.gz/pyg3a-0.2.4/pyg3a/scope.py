#!/usr/bin/env python3

from collections.abc import Mapping
from typing import Any, Final, Never, Optional, Sequence, cast, override

import libcst as cst


class Scope:
    data: Final[dict[str, str]]

    __slots__ = "data"

    def __init__(
        self,
        dict: Optional[Mapping[str, str]] = None,
        /,
        **kwargs: str,
    ):
        self.data = {}

        if dict is not None:
            self.update(dict)
        if kwargs:
            self.update(kwargs)

    def update(
        self,
        other: Mapping[str, str] = {},
        /,
        **kwds: str,
    ) -> None:
        """D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
        If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
        In either case, this is followed by: for k, v in F.items(): D[k] = v
        """
        if other:
            for key in other:
                self.data[key] = other[key]

        for key, value in kwds.items():
            self.data[key] = value

    def copy(self) -> "Scope":
        return Scope(self.data)

    def __getitem__(self, var: str | cst.Name) -> str:
        return self.data[var] if isinstance(var, str) else self.data[var.value]

    def __contains__(self, var: str | cst.Name) -> bool:
        return (var in self.data) if isinstance(var, str) else (var.value in self.data)

    def __setitem__(self, *_: Any) -> Never:
        raise TypeError("Use set_var(var, py_type)")

    def set_var(self, var: cst.Name, py_type: str) -> None:
        if not py_type or not var.value:
            raise TypeError("Incorrect variable or type")

        self.data[var.value] = py_type

    def inner(
        self,
        var: Optional[str | cst.Param | Sequence[str] | Sequence[cst.Param]] = None,
        py_type: Optional[str | Sequence[str]] = None,
    ) -> "Scope":
        if not var or not py_type:
            return Scope(self.data)

        new_scope: Scope = Scope(self.data)
        variables: list[str]

        match var:
            case str():
                variables = [var]
            case cst.Param():
                variables = [var.name.value]
            case [*seq] if isinstance(seq[0], cst.Param):
                variables = [param.name.value for param in cast(Sequence[cst.Param], var)]
            case _:
                variables = list(cast(Sequence[str], var))

        if isinstance(py_type, str):
            for i in range(len(variables)):
                new_scope.data[variables[i]] = py_type
        else:
            for i in range(min(len(variables), len(py_type))):
                new_scope.data[variables[i]] = py_type[i]

        return new_scope
