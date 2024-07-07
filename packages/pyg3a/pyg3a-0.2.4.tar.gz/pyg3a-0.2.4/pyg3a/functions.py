#!/usr/bin/env python3

import logging
from dataclasses import dataclass
from typing import Any, Optional, Sequence, override

import libcst as cst
from libcst._nodes.internal import (visit_optional, visit_required,
                                    visit_sentinel)
from libcst._visitors import CSTVisitorT

# Can't import from or we cause recursive imports
import pyg3a

from .block import Block
from .node import node_to_code, node_type
from .scope import Scope


class Parameter(cst.Param):
    """
    A positional or keyword argument in a :py:class:`libcst.Parameters` list. Always contains an :py:class:`libcst.Annotation`, and in some cases a ``default``.
    """

    annotation: cst.Annotation
    "A required :py:class:`libcst.Annotation`, used as a type hint."

    @override
    def __init__(self, parent: Optional[cst.Param] = None, **kwargs: Any):
        r"""
        Create a Parameter from either an annotated :py:class:`libcst.Param` or from keyworded attributes.

        :param parent: Optional 'parent' :py:class:`libcst.Param` with defined :py:attr:`annotation`.
        :param \**kwargs: Attributes of the created class to be used if ``parent`` isn't specified.

        :raises TypeError: If ``parent`` is not annotated.
        """

        if parent is None:
            super().__init__(**kwargs)
        else:
            if parent.annotation is None:
                raise TypeError

            super().__init__(
                star=parent.star,
                whitespace_after_star=parent.whitespace_after_star,
                name=parent.name,
                annotation=parent.annotation,
                equal=parent.equal,
                default=parent.default,
                comma=parent.comma,
                whitespace_after_param=parent.whitespace_after_param,
            )

    @override
    def _visit_and_replace_children(self, visitor: CSTVisitorT) -> "Parameter":
        return Parameter(
            star=self.star,
            whitespace_after_star=visit_required(
                self, "whitespace_after_star", self.whitespace_after_star, visitor
            ),
            name=visit_required(self, "name", self.name, visitor),
            annotation=visit_required(self, "annotation", self.annotation, visitor),
            equal=visit_sentinel(self, "equal", self.equal, visitor),
            default=visit_optional(self, "default", self.default, visitor),
            comma=visit_sentinel(self, "comma", self.comma, visitor),
            whitespace_after_param=visit_required(
                self, "whitespace_after_param", self.whitespace_after_param, visitor
            ),
        )


class Function:
    node: cst.FunctionDef
    "Original CST node, required to 'visit' it later when determining return type in :py:meth:`construct`."

    name: str
    "Name of function."

    exprs: Sequence[cst.BaseStatement] | Sequence[cst.BaseSmallStatement]
    "List of expressions (body) inside function."

    ret: str
    "String of return type as written in original Python file."

    args: list[Parameter]
    "List of arguments, all type-annotated."

    def __init__(self, func: cst.FunctionDef):
        """
        Create Function object from CST function definition.

        :param func: Function definition from the CST.
        """

        # Save CST node
        self.node = func

        # Save name of function
        self.name: str = func.name.value

        # Save 'body' of function (list of expressions)
        self.exprs: Sequence[cst.BaseStatement] | Sequence[cst.BaseSmallStatement] = func.body.body

        # Stringify (cst.Name("str") -> "str"; cst.Subscript("list", slice="str") -> "list[str]", etc.) return type annotation and store
        self.ret: str = (
            node_to_code(func.returns.annotation) if type(func.returns) is cst.Annotation else ""
        )

        # If we're asked to return a const char*, return a mutable char*
        if self.ret == "cstr":
            self.ret = "mutstr"

        # Raise SyntaxError if any parameters don't have an annotation, including all offenders in the error message
        if missing_annotations := [
            str(i) for i, arg in enumerate(func.params.params) if arg.annotation is None
        ]:
            raise SyntaxError(
                "Missing type annotation on argument(s) "
                + ", ".join(missing_annotations)
                + " of function "
                + self.name
            )

        # Save args as custom Parameter (forcing annotations to exist)
        self.args: list[Parameter] = [Parameter(p) for p in func.params.params]

        # Save this function's type (return_type, [annotation_types]) to the Main singleton
        pyg3a.Main.func_types[self.name] = (
            self.ret,
            [Block._obj_to_c_str(arg.annotation.annotation, True) for arg in self.args],
        )

    def __str__(self) -> str:
        """
        Create human-readable String containing all Function attributes.

        :returns: Function(name= :py:attr:`name`, args= :py:attr:`args`, exprs= :py:attr:`exprs`, ret= :py:attr:`ret`).
        """

        return f"Function(\n\tname='{self.name}',\n\targs={self.args},\n\texprs={self.exprs},\n\tret='{self.ret}'\n)"

    def __repr__(self) -> str:
        """
        Just use __str__ function for reprs.

        :returns: ``self.``:py:meth:`__str__`.
        """
        return str(self)

    def _str_args(self) -> str:
        """
        Helper function for :py:meth:`construct`, creating C-style list of arguments.

        :returns: comma-separated list of arguments in C format (``type name`` ).
        """

        return ", ".join(
            # <annotation -> C type str> <name>
            f"{Block._obj_to_c_str(arg.annotation.annotation, True)} {arg.name.value}"
            for arg in self.args
        )

    def construct(self) -> str:
        """
        High-level construction of C function definition from stored attributes:
            #. Generates the base inner scope from function arguments.
            #. Constructs the inside of the function with this base scope (see :py:meth:`pyg3a.block.Block.construct`).
            #. Determines the function return type if previously unknown, using found return statements.
            #. Re-registers function to Main singleton with new return type.
            #. Adds function signature to start of constructed function lines.
            #. Adds ``GetKey(&key)`` forever-loop to end of function if ``main()`` function.
            #. Ends function and returns constructed lines.

        :returns: Newline-delimited constructed C function.
        """

        # Output function lines
        lines: list[str] = []

        # Base scope inside function
        scope: Scope = Scope(
            {arg.name.value: node_to_code(arg.annotation.annotation) for arg in self.args}
        )

        # Add inside of function to ``lines``
        block: Block = Block(self.exprs, 1, scope)
        lines.append(block.construct())

        # Automatically find return type if unspecified
        if self.ret == "":
            # If there's no return statement, we're void/None
            self.ret = "None"

            # See :py:class:`FunctionVisitor`
            self.node.visit(FunctionVisitor(self, block.scope))

            # Re-register function type now we know what it is
            pyg3a.Main.func_types[self.name] = (self.ret, pyg3a.Main.func_types[self.name][1])

        # Now we know the exact function type, add signature to ``lines``
        lines.insert(0, f"{pyg3a.Main.registry[self.ret]} {self.name}({self._str_args()}) {{")

        # If we're the main function, ensure that the app doesn't automatically exit when Python's main() function completes
        if self.name == "main":
            # Create a temp var inside the function's scope
            tmp_var: str = pyg3a.PyG3A._gen_tmp_var(block.scope, "key")
            pyg3a.Main.project.includes.add("fxcg/keyboard.h")
            lines.append(f"\tint {tmp_var}; while (1) GetKey(&{tmp_var});")

        # End the function and return
        lines.append("}")
        return "\n".join(lines)


@dataclass(slots=True)
class FunctionVisitor(cst.CSTVisitor):
    """
    Traverses the CST of a Function's FunctionDef node to find a :py:class:`libcst.Return` node to determine the Function's return type.
    """

    func: Function
    "Function to set the return type of."

    scope: Scope
    "Scope inside function."

    @override
    def leave_Return_value(self, node: cst.Return) -> None:
        """
        If we find a ``return`` statement, get the type of the returned object and set our Function's return type to that.
        If the type cannot be determined, the user is warned and the type is automatically set to ``any``.

        :param node: The :py:class:`libcst.Return` node we've encountered.
        """

        if node.value is None:
            self.func.ret = "None"
        else:
            self.func.ret = node_type(node.value, self.scope, False, False)
            if self.func.ret == "any":
                logging.warning(
                    f"Return type of '{self.func.name}' could not be determined - automatically set to any"
                )
