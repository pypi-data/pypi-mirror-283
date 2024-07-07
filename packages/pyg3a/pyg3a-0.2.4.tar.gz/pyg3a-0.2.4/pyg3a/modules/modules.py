#!/usr/bin/env python3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import libcst as cst

import pyg3a
from .functions import Function
from ..node import node_to_code
from ..type_registry import TypeCategory


@dataclass(slots=True, init=False)
class Module:
    name: Final[str]
    file_name: Final[Path]
    functions: Final[set[Function]]

    def __init__(self, name: str, file_name: Path) -> None:
        self.name = name
        self.file_name = file_name
        self.functions = set()

        # Open the module file
        with file_name.open() as f:
            contents = f.read()

            # For statement in module
            for stmt in cst.parse_module(contents).body:
                # Parse functions in module
                if type(stmt) is cst.FunctionDef:
                    # Run __registry_types_pyg3a() to determine custom types
                    if stmt.name.value == "__registry_types_pyg3a":
                        extra_types_globs: dict[str, Any] = {"TypeCategory": TypeCategory}
                        exec(node_to_code(stmt), extra_types_globs)
                        for item in extra_types_globs["__registry_types_pyg3a"]().items():
                            if len(item[1]) > 1:
                                pyg3a.Main.registry.register(item[0], item[1][0], item[1][1])
                            else:
                                pyg3a.Main.registry.register(item[0], item[1][0], TypeCategory.NONE)

                    # Add custom functions and __for_pyg3a_* functions from module to custom_functions dictionary
                    elif stmt.name.value[-8:] == "__iter__":
                        self.functions.add(Function[cst.For](stmt, self.name, cst.For))
                    else:
                        self.functions.add(Function[cst.Call](stmt, self.name, cst.Call))

                # Parse imports in module
                elif type(stmt) is cst.SimpleStatementLine:
                    for line in stmt.body:
                        if type(line) is cst.Import:
                            # For header in imports
                            for alias in line.names:
                                pyg3a.Main.project.include_from_python_name(node_to_code(alias.name))

                        # Include headers from ``from header import _``
                        elif type(line) is cst.ImportFrom and type(line.module) is not None:
                            pyg3a.Main.project.include_from_python_name(node_to_code(line.module))
