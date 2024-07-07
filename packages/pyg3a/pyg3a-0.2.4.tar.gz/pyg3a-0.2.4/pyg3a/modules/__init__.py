#!/usr/bin/env python3

from typing import (Final, Iterable, override, Any)

from .functions import Function, FuncTypes
from .modules import Module
from ..scope import Scope


class ModuleSet:
    _funcs: Final[dict[type[FuncTypes], set[Function[FuncTypes]]]]
    _names: Final[set[str]]

    __slots__ = "functions", "_funcs", "_names"

    @override
    def __init__(self, iterable: Iterable[Module] = tuple()) -> None:
        self._funcs = {typ: set() for typ in FuncTypes.__args__}
        self._names = {module.name for module in iterable}

        for module in iterable:
            for function in module.functions:
                self._funcs[function.typ].add(function)

    @override
    def __repr__(self) -> str:
        return f"ModuleSet({', '.join([str(module) for module in self._names])})"

    def __contains__(self, module: str) -> bool:
        return module in self._names

    def add(self, module: Module) -> None:
        self._names.add(module.name)
        for function in module.functions:
            self._funcs[function.typ].add(function)

    def contains(self, node: FuncTypes, scope: Scope) -> bool:
        for fun in self._funcs[type(node)]:
            if fun.accepts(node, scope):
                return True
        return False

    def convert(self, node: FuncTypes, scope: Scope, **kwargs: Any) -> str:
        for fun in self._funcs[type(node)]:
            if inst := fun.accepts(node, scope):
                return inst.convert(**kwargs)
        raise KeyError(node)
