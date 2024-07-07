#!/usr/bin/env python3

from types import EllipsisType
from typing import Optional, cast

import libcst as cst

import pyg3a

from .scope import Scope

type CSTConstant = cst.BaseNumber | cst.BaseString | cst.Ellipsis | cst.Name
"Union type representing all Python constants in the CST."

type Constant = int | float | complex | str | bool | EllipsisType | None


def node_to_py_const(
    const: CSTConstant,
) -> Constant:
    """
    Convert a CST node representing a constant into its equivalent Python object.

    :param const: The constant to convert.
    :returns: The Python constant equivalent of the provided node.
    :raises SyntaxError: If the constant is an f-string.
    :raises TypeError: If the provided node cannot be interpreted.
    """

    # ...
    if type(const) is cst.Ellipsis:
        return ...

    # Numbers
    if type(const) is cst.Imaginary or type(const) is cst.Integer or type(const) is cst.Float:
        return const.evaluated_value

    # Strings
    if type(const) is cst.SimpleString:
        return const.raw_value
    if type(const) is cst.FormattedString:
        raise SyntaxError("There is currently no support for formatted strings")
    if type(const) is cst.ConcatenatedString:
        if type(const.left) is cst.FormattedString or type(const.right) is cst.FormattedString:
            raise SyntaxError("There is currently no support for formatted strings")

        assert isinstance(const.left, cst.SimpleString)

        # Recurse over right argument
        return const.left.raw_value + cast(str, node_to_py_const(const.right))

    # True, False, None
    if type(const) is cst.Name:
        if const.value == "True":
            return True
        if const.value == "False":
            return False
        if const.value == "None":
            return None

    raise TypeError(f"Wrong argument passed to node_to_py_const: {const}")


def node_type(
    node: cst.CSTNode,
    scope: Optional[Scope] = None,
    func_explicit: bool = True,
    scope_error: bool = True,
) -> str:
    """
    Determine type of CST node under specified scope, optionally explicitly specifying function types, and optionally raising an error when variables are not specified in the specified scope.

    :param node: The CST node to determine the type of.
    :param scope: The scope to find variables' types inside.
    :param func_explicit: Explicitly specify the stringified type of a function ("<function(arg1,arg2,...) returns type>"), enabled by default.
    :param scope_error: Raise a RuntimeError if ``node`` is a variable whose type is not defined inside ``scope``. True by default.
    :returns: A string representing the 'Python' type (see the type definitions in :py:class:`~pyg3a.pyg3a.Main`) of the specified ``node``.
    :raises RuntimeError: If ``scope_error`` is True and a variable is referenced with no type specified in ``scope``.
    """

    if scope is None:
        scope = Scope()

    # Named constants, variables, and functions
    if type(node) is cst.Name:
        if node.value == "None":
            return "None"
        if node.value in ("True", "False"):
            return "bool"

        if node.value in scope:
            return scope[node.value]

        if node.value in pyg3a.Main.func_types:
            return_type, param_types = pyg3a.Main.func_types[node.value]
            if func_explicit:
                return f"Callable[[{', '.join(param_types)}], {return_type}]"

            return return_type

        if scope_error:
            raise RuntimeError("Variable not in scope!")
        return "any"

    # Other constants
    if isinstance(node, CSTConstant.__value__):
        return type(node_to_py_const(node)).__name__

    # Called functions
    if type(node) is cst.Call:
        match node:
            case cst.Call(func=cst.Name(value=func_name)) if func_name in pyg3a.Main.func_types:
                return pyg3a.Main.func_types[node.func.value][0]
            case cst.Call(func=cst.Name(value="cast"), args=[cst.Arg(value=cst.Name(value=typ)), _]):
                return typ

    # List access with variable index
    if type(node) is cst.Subscript and type(node.value) is cst.Name:
        # If accessing sub[script], just return "sub[script]"
        if (
            type(node.slice[0].slice) is cst.Index
            and type(node.slice[0].slice.value) is cst.Name
            and node.slice[0].slice.value.value not in scope
        ):
            return f"{node.value.value}[{node.slice[0].slice.value.value}]"

        # Determine and return the reference list[T]'s T
        if "[" in (var := node_type(node.value, scope, False, scope_error)):
            return var[var.find("[") + 1 : -1]

    # Lambdas
    if type(node) is cst.Lambda:
        if func_explicit:
            return f"Callable[[{', '.join(['auto' for _ in node.params.params])}], any]"
        return "any"

    # Sequences
    if type(node) is cst.Tuple:
        return f"tuple[{', '.join([node_type(elem.value, scope) for elem in node.elements])}]"
    if type(node) is cst.List:
        return f"list[{node_type(node.elements[0].value, scope)}]"

    # Operators
    if type(node) is cst.BinaryOperation:
        # All string operations return strings
        if node_type(node.left, scope, False) == "str" or node_type(node.right, scope, False) == "str":
            return "str"

        # Numerical operations
        elif (
            node_type(node.left, scope, False) in pyg3a.Main.registry.NUMBERS
            and node_type(node.right, scope, False) in pyg3a.Main.registry.NUMBERS
        ):
            # For + - * % ** // use the more specific type (float if either is a float else int)
            if type(node.operator) in (
                cst.Add,
                cst.Subtract,
                cst.Multiply,
                cst.Modulo,
                cst.Power,
                cst.FloorDivide,
            ):
                return (
                    node_type(node.left, scope)
                    if (
                        node_type(node.left, scope) in pyg3a.Main.registry.FLOATS
                        or node_type(node.right, scope) in pyg3a.Main.registry.FLOATS
                    )
                    else node_type(node.left, scope)
                )

            # Standard division always returns a float
            if type(node.operator) is cst.Divide:
                return "float"

            # Otherwise we stick with the left operand's type
            return node_type(node.left, scope)

    # No type if unsure
    return "None"


def node_to_code(node: cst.CSTNode) -> str:
    """
    Convert CST Node object to Python code.

    :param node: CST Node
    :returns: String containing Python code equivalent
    """
    return pyg3a.Main.codegen_module.code_for_node(node)
