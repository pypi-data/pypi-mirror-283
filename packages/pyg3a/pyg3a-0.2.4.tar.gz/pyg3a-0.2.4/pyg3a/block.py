#!/usr/bin/env python3

import logging
from typing import Final, Optional, Sequence, cast

import libcst as cst

import pyg3a
from .node import (Constant, CSTConstant, node_to_code, node_to_py_const,
                   node_type)
from .scope import Scope

CST_TO_C_EQV: Final[dict[type[cst.CSTNode], str]] = {
    # Statements
    cst.Break: "break",
    cst.Continue: "continue",
    cst.Pass: "// PASS",
    #
    # Comparison operators
    cst.Equal: "==",
    cst.Is: "==",
    cst.NotEqual: "!=",
    cst.IsNot: "!=",
    cst.GreaterThan: ">",
    cst.GreaterThanEqual: ">=",
    cst.LessThan: "<",
    cst.LessThanEqual: "<=",
    #
    # Logical operators
    cst.Or: "||",
    cst.And: "&&",
    cst.Not: "!",
    #
    # Numerical operators
    cst.Add: "+",
    cst.Subtract: "-",
    cst.Multiply: "*",
    cst.Divide: "/",
    cst.Modulo: "%",
    cst.Plus: "+",
    cst.Minus: "-",
    # cst.Power - covered in cst.BinaryOperation as it requires math.h.
    # cst.FloorDivide - covered in cst.BinaryOperation as it requires math.h.
    #
    # Binary operators
    cst.BitAnd: "&",
    cst.BitOr: "|",
    cst.BitXor: "^",
    cst.BitInvert: "~",
    cst.LeftShift: "<<",
    cst.RightShift: ">>",
    #
    # Operative assignment
    cst.AddAssign: "+=",
    cst.SubtractAssign: "-=",
    cst.MultiplyAssign: "*=",
    cst.DivideAssign: "/=",
    cst.ModuloAssign: "%=",
    cst.BitAndAssign: "&=",
    cst.BitOrAssign: "|=",
    cst.BitXorAssign: "^=",
    cst.LeftShiftAssign: "<<=",
    cst.RightShiftAssign: ">>=",
    # cst.FloorDivideAssign - covered in cst.AugAssign as it does not have a 1-1 in C
}
"Dictionary mapping CST node types to their C string equivalent."

type QualifiedConstOrTuple[T] = Constant | tuple[T]
type ConstOrTuple = QualifiedConstOrTuple[Constant | cst.CSTNode] | QualifiedConstOrTuple[
    ConstOrTuple
]


class Block:
    exprs: Final[list[cst.CSTNode]]
    "The statements contained within this block of code."

    scope: Final[Scope]
    "The inner scope of this block of code."

    tabnum: int
    "The number of tabs this block is indented by."

    nested_if: bool
    "True if this block is inside an if statement."

    __slots__ = "exprs", "scope", "tabnum", "nested_if"

    def __init__(
            self,
            statements: Sequence[cst.BaseStatement] | Sequence[cst.BaseSmallStatement],
            tabs: int,
            scope: Optional[Scope] = None,
            nested_if: bool = False,
    ) -> None:
        """
        Create a :py:class:`Block` containing a list of statements, indented by a certain number of tabs and with an optional initial scope.

        :param exprs: Sequence of statements inside the block of code.
        :param tabs: The number of tabs this code is indented by.
        :param scope: The scope outside the block of code.
        """

        # Set attributes from params
        self.exprs = list(statements)
        self.tabnum = tabs
        self.scope = Scope() if scope is None else scope.inner()
        self.nested_if = nested_if

        # Expand statements separated by semicolons into their own statements inside :py:attr:`exprs`
        for i, node in enumerate(self.exprs):
            if type(node) is cst.SimpleStatementLine:
                del self.exprs[i]
                for j, statement in enumerate(node.body):
                    self.exprs.insert(i + j, statement)

    @property
    def tabs(self) -> str:
        """
        Generate a string representing the tabs at the start of each line of this block's code.

        :returns: :py:attr:`tabnum` tabs.
        """

        return self.tabnum * "\t"

    @staticmethod
    def _obj_to_c_str(
            obj: ConstOrTuple | cst.CSTNode,
            isType: bool = False,
            generateVoidLambda: bool = False,
            scope: Optional[Scope] = None,
    ) -> str:
        """
        Convert an ``obj`` to a string containing a C equivalent.

        :param obj: The object (CST node or Python constant) to convert.
        :param isType: Optionally assume that the CST node passed references a Python type to be converted to the equivalent C type.
        :param generateVoidLambda: Optionally make lambdas return void instead of returning their output value.
        :param scope: Optionally provide a scope to look up variables inside of.

        :returns: C equivalent of ``obj``.

        :raises SyntaxError: If unsupported syntax is used.
        :raises Error: Passes through errors from called custom package functions.
        """

        if scope is None:
            scope = Scope()

        # Constants
        def const_to_c_str(
                const: ConstOrTuple,
        ) -> str:
            # Numbers are the same in Python and C
            if type(const) is int or type(obj) is float:
                return str(const)

            # Complex numbers are unsupported
            if type(const) is complex:
                raise SyntaxError("No support for complex numbers.")

            # Use String class for strings
            if type(const) is str:
                escaped_str: str = repr(const).replace("'", '"')
                return f"String({escaped_str})"

            # Bools are just ints in C
            if type(const) is bool:
                return "1" if const is True else "0"

            # Tuples are structs
            if type(const) is tuple:
                return f"{{{', '.join([Block._obj_to_c_str(o, scope=scope) for o in const])}}}"

            # Ellipses are comments
            if const is Ellipsis:
                return "/* ... */"

            # Otherwise const is just None
            pyg3a.Main.project.includes.add("stddef.h")
            return "NULL"

        def node_to_c_str(node: cst.CSTNode) -> str:
            # Expand semicolon-separated statements
            if type(node) is cst.SimpleStatementLine:
                return "; ".join([node_to_c_str(o) for o in node.body])

            # If we're calling a function
            if type(node) is cst.Call:
                # If we have a custom function defined for this function
                try:
                    return pyg3a.Main.project.modules.convert(node, scope)
                except KeyError:
                    pass

                match node:
                    # If we're casting a value
                    case cst.Call(func=cst.Name(value="cast"),
                                  args=[cst.Arg(value=cst.Name(value=typ)), cst.Arg(value=val)]):
                        return f"({pyg3a.Main.registry[typ]}) ({node_to_c_str(val)})"
                    case _:
                        # If no custom __pyg3a_, just run the function
                        return f"{node_to_c_str(node.func)}({', '.join([node_to_c_str(arg.value) for arg in node.args])})"
            if type(node) is cst.Name:
                # Constants
                if node.value in ("True", "False", "None"):
                    return Block._obj_to_c_str(node_to_py_const(node), isType)

                # Type name
                if isType is True and node.value in pyg3a.Main.registry:
                    return pyg3a.Main.registry[node.value]

                # Variable
                return node.value

            # Other constants
            if isinstance(node, CSTConstant.__value__):
                return Block._obj_to_c_str(node_to_py_const(node), isType)

            # Array/list/class item access and gene[ric] types
            if type(node) is cst.Subscript:
                if type(node.slice[0].slice) is not cst.Index:
                    raise SyntaxError("There is no support for slices")

                # If we're referencing a gene[ric] type
                if type(node.value) is cst.Name and type(node.slice[0].slice.value) is cst.Name:
                    if isType and node.value.value == "list":
                        pyg3a.Main.project.includes.add("list.hpp")

                        # List<char> for all strings
                        if node.slice[0].slice.value.value in pyg3a.Main.registry.C_STRINGS:
                            return "List<char>"

                        # Otherwise List<ric>
                        return f"List<{pyg3a.Main.registry[node.slice[0].slice.value.value]}>"

                    if isType and node.value.value == "tuple":
                        # tuple[string_type] is an array of chars
                        if node.slice[0].slice.value.value in pyg3a.Main.registry.C_STRINGS:
                            return f"char"

                        # A variable-length tuple[T] is a T*
                        if len(node.slice) == 2 and isinstance(node.slice[1].slice.value, cst.Ellipsis):
                            return f"{pyg3a.Main.registry[node.slice[0].slice.value.value]}*"

                        # Otherwise tuple[T] is an array of T
                        return pyg3a.Main.registry[node.slice[0].slice.value.value]

                # Otherwise translate our item access directly to C
                return f"{node_to_c_str(node.value)}[{node_to_c_str(node.slice[0].slice.value)}]"

            # struct.prop translates directly to C
            if type(node) is cst.Attribute and type(node.attr) is cst.Name:
                return f"{node_to_c_str(node.value)}.{node.attr.value}"

            # Use CST_TO_C_EQV to translate comparisons, boolean, and unary operators
            if type(node) is cst.Comparison:
                # && separated comparisons
                return CST_TO_C_EQV[cst.And].join(
                    [
                        f"{node_to_c_str(node.left)} {CST_TO_C_EQV[type(node.comparisons[i].operator)]} ({node_to_c_str(node.comparisons[i].comparator)})"
                        for i in range(len(node.comparisons))
                    ]
                )
            if type(node) is cst.BooleanOperation:
                return f"({node_to_c_str(node.left)}) {CST_TO_C_EQV[type(node.operator)]} ({node_to_c_str(node.right)})"
            if type(node) is cst.UnaryOperation:
                return f"{CST_TO_C_EQV[type(node.operator)]} ({node_to_c_str(node.expression)})"

            if type(node) is cst.BinaryOperation:
                # Use <math.h>'s pow function for power operators.
                if type(node.operator) is cst.Power:
                    pyg3a.Main.project.includes.add("math.h")
                    return f"pow({node_to_c_str(node.left)}, {node_to_c_str(node.right)})"

                # Use casts for C equivalent of floor division.
                if type(node.operator) is cst.FloorDivide:
                    # Not sure if this is necessary
                    # if "math.h" not in pyg3a.Main.project.imports:
                    #     pyg3a.Main.project.imports.append("math.h")

                    # If left and right are integers => left / right == left // right
                    if (
                            node_type(node.left, scope=scope) in pyg3a.Main.registry.INTEGERS
                            and node_type(node.right, scope=scope) in pyg3a.Main.registry.INTEGERS
                    ):
                        return f"(({node_to_c_str(node.left)}) / ({node_to_c_str(node.right)}))"

                    # Otherwise, round left / right and then convert it to a float
                    return f"(float) ((int) (({node_to_c_str(node.left)}) / ({node_to_c_str(node.right)})))"

                # Otherwise use CST_C_EQV for Python-supported operations
                if (
                        node_type(node.left, scope, False) in pyg3a.Main.registry.PY
                        and node_type(node.right, scope, False) in pyg3a.Main.registry.PY
                ):
                    return f"({node_to_c_str(node.left)} {CST_TO_C_EQV[type(node.operator)]} {node_to_c_str(node.right)})"

                raise SyntaxError(
                    f"'{node_to_code(node)}': Unsupported types {node_type(node.left, scope, False)} and {node_type(node.right, scope, False)} for operation {type(node.operator).__name__}"
                )

            # Walrus operator
            if type(node) is cst.NamedExpr:
                # You can't declare a variable in the C equivalent ((int a = b) doesn't syntax correctly), so it must be something already in scope
                if type(node.target) is cst.Name and node.target.value not in scope:
                    raise SyntaxError(
                        f"type of variable '{node.target.value}' must be defined in scope"
                    )
                elif (
                        type(node.target) is cst.Subscript
                        and type(node.target.value) is cst.Name
                        and node.target.value.value not in scope
                ):
                    raise SyntaxError(
                        f"type of variable '{node.target.value.value}' must be defined in scope"
                    )

                # a := b => a = b in C
                return f"{node_to_c_str(node.target)} = {node_to_c_str(node.value)}"

            # Lambdas
            if type(node) is cst.Lambda:
                # You can't annotate lambda args, so we'll have to automatically determine their type
                args: list[str] = [f"auto {param.name.value}" for param in node.params.params]

                stmt: str = Block._obj_to_c_str(
                    # Create inner scope from the lambda args with 'any' types
                    node.body,
                    scope=scope.inner(node.params.params, "any"),
                )

                if generateVoidLambda:
                    return f"[]({', '.join(args)}){{{stmt};}}"

                # Return outcome of lambda if not generateVoidLambda
                return f"[]({', '.join(args)}){{return {stmt};}}"

            # Ternary if
            if type(node) is cst.IfExp:
                return f"({node_to_c_str(node.test)}) ? {node_to_c_str(node.body)} : {node_to_c_str(node.orelse)}"

            # Sets, tuples, lists are all struct initialisers
            if isinstance(node, cst.Set | cst.Tuple | cst.List):
                return f"{{{', '.join([node_to_c_str(elt.value) for elt in node.elements])}}}"

            raise SyntaxError(f"No support for {type(node)}: '{node_to_code(node)}'")

        # Constants
        if isinstance(obj, Constant.__value__ | tuple):
            return const_to_c_str(obj)

        # CST Nodes
        if isinstance(obj, cst.CSTNode):
            return node_to_c_str(obj)

        # Otherwise give up
        return str(obj)

    def construct(self) -> str:
        """
        Construct this block of code into C.

        :returns: A string containing the converted C block delimited with '\n's.
        :raises SyntaxError: If unsupported syntax is used.
        """

        lines: list[str] = []
        for expr in self.exprs:
            match expr:
                case cst.Expr(
                    value=cst.Call(
                        func=cst.Name(func_name), args=[cst.Arg(value=(cst.BaseString() as c_code))]
                    )
                ) if func_name == "raw_c":
                    lines.append(f"{self.tabs}{node_to_py_const(c_code)};")

                case cst.Expr():
                    lines.append(f"{self.tabs}{Block._obj_to_c_str(expr.value, scope=self.scope)};")

                case cst.Assign() | cst.AnnAssign(target=cst.Name()):
                    annotation: str = ""
                    c_annotation: str = ""
                    targets: list[cst.BaseAssignTargetExpression] = (
                        [expr.target]
                        if type(expr) is cst.AnnAssign
                        else [target.target for target in expr.targets]
                    )

                    for target in targets:
                        if type(expr) is cst.AnnAssign:
                            match expr.annotation.annotation:
                                case cst.Subscript(value=cst.Name(value=gene), slice=indices):
                                    annotation = f"{gene}[{', '.join([node_to_code(index.slice.value) for index in indices])}]"
                                case cst.Name(value=ann):
                                    annotation = ann

                            c_annotation = Block._obj_to_c_str(
                                expr.annotation.annotation, True, scope=self.scope
                            )
                        elif type(target) is cst.Name and target not in self.scope:
                            annotation = node_type(cast(cst.Assign, expr).value, self.scope, False)

                            if annotation == "any":
                                logging.warning(
                                    f"Type of '{node_to_code(target)}' not be determined - automatically set to any"
                                )

                            if annotation in pyg3a.Main.registry:
                                c_annotation = pyg3a.Main.registry[annotation]
                            else:
                                c_annotation = Block._obj_to_c_str(
                                    cst.parse_expression(annotation), True, scope=self.scope
                                )
                        elif (
                                type(target) is cst.Subscript
                                and type(target.value) is cst.Name
                                and target.value not in self.scope
                        ):
                            raise SyntaxError(
                                f"Type of '{node_to_code(target.value)}' not defined in scope"
                            )

                        match target:
                            case cst.Tuple():
                                tmp_var: str = pyg3a.PyG3A._gen_tmp_var(self.scope, "tuple_unpack")
                                lines.append(
                                    f"{self.tabs}auto {tmp_var} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                )
                                for i, elt in enumerate(target.elements):
                                    if type(elt.value) is cst.Name:
                                        if elt.value.value == "_":
                                            continue

                                        if elt.value.value not in self.scope:
                                            raise SyntaxError(
                                                f"type of variable '{elt.value.value}' must be defined in scope"
                                            )

                                        if (
                                                Block._obj_to_c_str(
                                                    self.scope[elt.value.value], True, scope=self.scope
                                                )[-1]
                                                == "*"
                                        ):
                                            pyg3a.Main.project.includes.add("stddef.h")
                                            lines.append(
                                                f"{self.tabs}if ({elt.value.value} != NULL) free({elt.value.value});"
                                            )

                                        if (
                                                self.scope[elt.value.value]
                                                in pyg3a.Main.registry.C_STRINGS
                                        ):
                                            pyg3a.Main.project.includes.add("string.h")
                                            lines.append(
                                                f"{self.tabs}strcpy({elt.value.value}, {tmp_var}._{i});"
                                            )
                                        else:
                                            lines.append(
                                                f"{self.tabs}{Block._obj_to_c_str(elt.value, scope=self.scope)} = {tmp_var}._{i};"
                                            )
                                    else:
                                        lines.append(
                                            f"{self.tabs}{Block._obj_to_c_str(elt.value, scope=self.scope)} = {tmp_var}._{i};"
                                        )

                            case cst.Name(value=var_name) | cst.Subscript(
                                value=cst.Name(value=var_name)
                            ) if var_name in self.scope:
                                if (
                                        type(target) is cst.Name
                                        and self.scope[target.value] in pyg3a.Main.registry
                                        and pyg3a.Main.registry[self.scope[target.value]][-1] == "*"
                                ):
                                    pyg3a.Main.project.includes.add("stddef.h")
                                    lines.append(
                                        f"{self.tabs}if ({target.value} != NULL) free({target.value});"
                                    )

                                if (
                                        type(target) is cst.Name
                                        and self.scope[target.value] in pyg3a.Main.registry.C_STRINGS
                                ):
                                    pyg3a.Main.project.includes.add("string.h")
                                    lines.append(
                                        f"{self.tabs}strcpy({target.value}, {Block._obj_to_c_str(expr.value, scope=self.scope)});"
                                    )
                                else:
                                    lines.append(
                                        f"{self.tabs}{Block._obj_to_c_str(target, scope=self.scope)} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                    )

                            case cst.Name():
                                if (
                                        type(expr.value) is cst.Name
                                        and expr.value.value == "None"
                                        and annotation not in pyg3a.Main.registry
                                ):
                                    lines.append(f"{self.tabs}{c_annotation} {target.value};")
                                else:
                                    if annotation == "cstr":
                                        if (
                                                type(expr.value) is cst.Name
                                                and expr.value.value != "None"
                                        ) or type(expr.value) is not cst.Name:
                                            self.scope.set_var(target, "conststr")
                                            lines.append(
                                                f"{self.tabs}const char* {target.value} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                            )
                                        else:
                                            self.scope.set_var(target, "arrstr")
                                            if (
                                                    type(expr.value) is cst.Name
                                                    and expr.value.value == "None"
                                            ):
                                                lines.append(
                                                    f"{self.tabs}char {target.value}[257];"
                                                )
                                            else:
                                                lines.append(
                                                    f"{self.tabs}char* {target.value} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                                )
                                    # Fixed-length tuples
                                    elif annotation[:6] == "tuple[" and annotation[-4:] != "...]":
                                        tuple_val: str = Block._obj_to_c_str(
                                            expr.value, scope=self.scope
                                        )
                                        tuple_size: int = 0

                                        if tuple_val[0] == "{" and tuple_val[-1] == "}":
                                            tuple_size = len(
                                                [
                                                    int(i)
                                                    for i in tuple_val[1:-1]
                                                .replace(" ", "")
                                                .split(",")
                                                ]
                                            )

                                        lines.append(
                                            f"{self.tabs}{c_annotation} {target.value}[{tuple_size}] = {tuple_val};"
                                        )
                                    # elif type(expr.value) is cst.List:
                                    #     lines.append(
                                    #         f"{self.tabs}{c_annotation} {target.value}({len(expr.value.elements)}, {Block._obj_to_c_str(cst.Tuple(elements=expr.value.elements), scope=self.scope)});"
                                    #     )
                                    else:
                                        lines.append(
                                            f"{self.tabs}{c_annotation} {target.value} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                        )

                        if len(annotation) > 0 and type(target) is cst.Name:
                            self.scope.set_var(target, annotation)

                case cst.AugAssign(target=cst.Name(var_name)) if var_name not in self.scope:
                    raise SyntaxError(f"variable '{var_name}' must be defined in scope")

                case cst.AugAssign(
                    target=cst.Subscript(value=cst.Name(var_name))
                ) if var_name not in self.scope:
                    raise SyntaxError(f"variable '{var_name}' must be defined in scope")

                case cst.AugAssign(operator=cst.FloorDivideAssign()):
                    lines.append(
                        f"{self.tabs}{Block._obj_to_c_str(expr.target, scope=self.scope)} = {Block._obj_to_c_str(cst.BinaryOperation(left=expr.target, operator=cst.FloorDivide(), right=expr.value), scope=self.scope)};"
                    )

                case cst.AugAssign():
                    lines.append(
                        f"{self.tabs}{Block._obj_to_c_str(expr.target, scope=self.scope)} {CST_TO_C_EQV[type(expr.operator)]} {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                    )

                case cst.If():
                    if not self.nested_if:
                        lines.append(
                            f"{self.tabs}if ({Block._obj_to_c_str(expr.test, scope=self.scope)}) {{"
                        )

                    expressions: Block = Block(expr.body.body, self.tabnum + 1, self.scope)
                    lines.append(expressions.construct())

                    if expr.orelse is not None:
                        if type(expr.orelse) is cst.If:
                            lines.append(
                                f"{self.tabs}}} else if ({Block._obj_to_c_str(expr.orelse.test, scope=self.scope)}) {{"
                            )
                            expressions = Block(
                                expr.orelse.body.body, self.tabnum, self.scope, nested_if=True
                            )
                            lines.append(expressions.construct())
                        else:
                            lines.append(f"{self.tabs}}} else {{")
                            expressions = Block(expr.orelse.body.body, self.tabnum + 1, self.scope)
                            lines.append(expressions.construct())

                    if not self.nested_if:
                        lines.append(f"{self.tabs}}}")

                case cst.While():
                    lines.append(
                        f"{self.tabs}while ({Block._obj_to_c_str(expr.test, scope=self.scope)}) {{"
                    )

                    expressions = Block(expr.body.body, self.tabnum + 1, self.scope)
                    lines.append(expressions.construct())

                    lines.append(f"{self.tabs}}}")

                case cst.Return(value=None):
                    lines.append(f"{self.tabs}return;")

                case cst.Return(value=cst.Name(value="None")):
                    pyg3a.Main.project.includes.add("stddef.h")
                    lines.append(f"{self.tabs}return NULL;")

                case cst.Return(value=cst.Name(var_name)) if (
                        var_name not in ("None", "True", "False")
                        and self.scope[var_name]
                        in (
                            "mutstr",
                            "arrstr",
                        )
                ):
                    pyg3a.Main.project.includes.add("stdlib.h")

                    tmp_name: str = pyg3a.PyG3A._gen_tmp_var(self.scope, "ret_str")
                    lines.append(
                        f"{self.tabs}char* {tmp_name} = (char*) malloc(sizeof {var_name});"
                    )
                    lines.append(f"{self.tabs}strcpy({tmp_name}, {var_name});")
                    lines.append(f"{self.tabs}return {tmp_name};")

                case cst.Return():
                    lines.append(
                        f"{self.tabs}return {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                    )

                case cst.For(
                    iter=cst.Call(func=cst.Name()),
                    target=(cst.Name())
                ) if pyg3a.Main.project.modules.contains(expr, self.scope):
                    lines.append(pyg3a.Main.project.modules.convert(expr, self.scope, tabnum=self.tabnum))

                case cst.For(target=(cst.Name() as target)):
                    arr_name: str = pyg3a.PyG3A._gen_tmp_var(self.scope, "for_arr")
                    iter_name: str = pyg3a.PyG3A._gen_tmp_var(self.scope, "for_iter")

                    iter_str: str = Block._obj_to_c_str(expr.iter, scope=self.scope)
                    if iter_str[0] == "{" and iter_str[-1] == "}":
                        iter_items: list[str] = iter_str[1:-1].replace(" ", "").split(",")
                        lines.append(
                            f"{self.tabs}decltype({iter_items[0]}) {arr_name}[{len(iter_items)}] = {iter_str};"
                        )
                    else:
                        lines.append(f"{self.tabs}auto {arr_name} = {iter_str};")

                    lines.append(
                        f"{self.tabs}for (unsigned int {iter_name} = 0; {iter_name} < sizeof({arr_name})/sizeof(*{arr_name}); {iter_name}++) {{"
                    )

                    target_type: str = "auto"
                    iter_type: list[str] = node_type(expr.iter, self.scope, func_explicit=False).split("[", maxsplit=1)
                    if (
                            len(iter_type) == 2 and
                            (iter_type[0] == "tuple"
                             or iter_type[0] == "list")
                            and iter_type[1][-1] == "]"
                    ):
                        target_type = pyg3a.Main.registry[iter_type[1][:-1]]

                    lines.append(
                        f"{self.tabs}\t{target_type} {target.value} = {arr_name}[{iter_name}];"
                    )

                    expressions = Block(
                        expr.body.body,
                        self.tabnum + 1,
                        self.scope.inner(
                            target.value, target_type if target_type != "auto" else "any"
                        ),
                    )
                    lines.append(expressions.construct())

                    lines.append(f"{self.tabs}}}")

                case cst.Del():
                    del_targets: list[cst.CSTNode] = []
                    if type(expr.target) is cst.Tuple:
                        del_targets.extend([el.value for el in expr.target.elements])
                    else:
                        del_targets.append(expr.target)

                    for del_target in del_targets:
                        if type(del_target) is cst.Subscript:
                            raise SyntaxError(
                                f"'{node_to_code(expr)}': You cannot delete an item of an array."
                            )
                        if (
                                type(del_target) is cst.Name
                                and node_type(del_target, self.scope) in pyg3a.Main.registry.C_STRINGS
                        ):
                            pyg3a.Main.project.includes.add("stddef.h")
                            lines.append(
                                f"{self.tabs}if ({Block._obj_to_c_str(del_target, scope=self.scope)} != NULL) free({Block._obj_to_c_str(del_target, scope=self.scope)});"
                            )
                        else:
                            raise SyntaxError(
                                f"You cannot delete {Block._obj_to_c_str(del_target, scope=self.scope)}"
                            )
                #   case cst.Match():
                #     def _match_case_to_c_str(pattern: cst.pattern) -> str:
                #         case_lines: list[str] = []
                #         if type(pattern) is cst.MatchValue:
                #             case_lines.append(
                #                 f"{self.tabs}\tcase {Block._obj_to_c_str(pattern.value, scope = self.scope)}:"
                #             )
                #         elif type(pattern) is cst.MatchAs:
                #             if pattern.pattern is None:
                #                 case_lines.append(f"{self.tabs}\tdefault:")
                #             else:
                #                 case_lines.append(_match_case_to_c_str(pattern.pattern))
                #         elif type(pattern) is cst.MatchOr:
                #             for option in pattern.patterns:
                #                 case_lines.append(_match_case_to_c_str(option))
                #         else:
                #             raise SyntaxError(
                #                 "Match statements only support: matching values, _ (default), as, | (or)"
                #             )
                #         return "\n".join(case_lines)

                #     lines.append(
                #         f"{self.tabs}switch ({Block._obj_to_c_str(expr.subject, scope = self.scope)}) {{"
                #     )
                #     for case in expr.cases:
                #         lines.append(_match_case_to_c_str(case.pattern))
                #         lines.append(f"{self.tabs}\t\t{{")

                #         if type(case.pattern) is cst.MatchAs and case.pattern.name is not None:
                #             lines.append(
                #                 f"{self.tabs}\t\t\tauto {case.pattern.name} = {Block._obj_to_c_str(expr.subject, scope = self.scope)};"
                #             )

                #         body: Block = Block(case.body, self.tabnum + 3, self.scope)
                #         lines.append(body.construct())
                #         lines.append(f"{self.tabs}\t\t\tbreak;")

                #         lines.append(f"{self.tabs}\t\t}}")

                #     if lines[-2] == f"{self.tabs}\t\tbreak;":
                #         lines.pop(-2)

                #     lines.append(f"{self.tabs}}}")

                case cst.ImportFrom(module=module):
                    pyg3a.PyG3A._import_module(Block._obj_to_c_str(module).replace(".", "/"))

                case cst.Import(names=modules):
                    for mod in modules:
                        pyg3a.PyG3A._import_module(Block._obj_to_c_str(mod.name).replace(".", "/"))

                case cst.FunctionDef(name=cst.Name(value=func_name)):
                    for func in [
                        fun for fun in pyg3a.Main.project.functions if fun.name == func_name
                    ]:
                        if func.name == "main" and not pyg3a.Main.main_function_overridden:
                            pyg3a.Main.main_function_overridden = True
                        else:
                            raise SyntaxError(f"Cannot override function '{func.name}'")

                    pyg3a.Main.project.add_func(expr)

                case stmt if type(stmt) in CST_TO_C_EQV:
                    lines.append(f"{self.tabs}{CST_TO_C_EQV[type(expr)]};")

                case _ as node:
                    raise SyntaxError(f"No support for {type(node)}: '{node_to_code(node)}'")
                # else:
                #     lines.append(f"{self.tabs}{Block._obj_to_c_str(expr, scope=self.scope)};")
        return "\n".join(lines)
