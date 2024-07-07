#!/usr/bin/env python3

import builtins
import functools
import inspect
import logging
from dataclasses import dataclass
from types import FunctionType, GenericAlias
from typing import Any, Final, NamedTuple, Never, Optional, Protocol, TypeVar, cast, Callable

import libcst as cst

import pyg3a
from ..block import Block
from ..functions import Function as CFunction
from ..node import CSTConstant, node_to_code, node_to_py_const, node_type
from ..scope import Scope
from ..type_registry import TypeCategory

FuncTypes = cst.Call | cst.For

# For some reason our type checkers can't figure this out
# Node = TypeVar("Node", *FuncTypes.__args__)
Node = TypeVar("Node", cst.Call, cst.For)


class Converter[Node](Protocol):
    def __call__(self, node: Node, /) -> str: ...


class Parameter(NamedTuple):
    name: str
    py_type: str
    default: object | Never
    to_arg: Callable[[cst.Arg, Scope], any]


def _annotation_to_c(annotation: cst.Annotation) -> str:
    if isinstance(annotation.annotation, cst.SimpleString | cst.ConcatenatedString):
        return annotation.annotation.evaluated_value
    return node_to_code(annotation.annotation)


def _gen_param(p: cst.Param) -> Parameter:
    if p.annotation is None:
        raise TypeError

    if p.default is not None and not isinstance(p.default, CSTConstant.__value__):
        raise TypeError

    if isinstance(p.annotation.annotation, cst.List):
        return Parameter(
            p.name.value,
            f"tuple{_annotation_to_c(p.annotation)}",
            Never if p.default is None else node_to_py_const(cast(CSTConstant, p.default)),
            lambda arg, scope: [Block._obj_to_c_str(elem.value, False, False, scope) for elem in arg.value.elements],
        )

    return Parameter(
        p.name.value,
        _annotation_to_c(p.annotation),
        Never if p.default is None else node_to_py_const(cast(CSTConstant, p.default)),
        lambda arg, scope: Block._obj_to_c_str(arg.value, False, False, scope),
    )


def _importer(
    name: str,
    _globs: Optional[dict[str, Any]] = None,
    locals: Optional[dict[str, Any]] = None,
    *_args,
) -> None:
    if locals and name.split(".", maxsplit=1)[0] in locals:
        raise ImportError("Cannot import module with same name as local variable", name=name)

    pyg3a.Main.project.include_from_python_name(name)


def _annotation_to_str(annotation: type | GenericAlias | str) -> str:
    return annotation.__name__ if type(annotation) is type else str(annotation)


def _c_func_decorator(parent_mod_name: str, func: FunctionType) -> None:
    if "return" not in func.__annotations__:
        raise SyntaxError(f"No return annotation on function {func.__name__}() from module '{parent_mod_name}'")

    pyg3a.Main.func_types[func.__name__] = (
        _annotation_to_str(func.__annotations__["return"]),
        [_annotation_to_str(p_ann) for p_ann in func.__annotations__ if p_ann != "return"],
    )

    func_c_body: str = func(*((None,) * func.__code__.co_argcount)).strip()

    globs: dict[str, Any] = {}

    pyg3a.PyG3A._add_c_func(
        func.__name__,
        CFunction(
            cst.parse_statement(
                f'def {func.__name__}{str(inspect.signature(func, eval_str=True)).replace(f"{__name__}.", "")}:\n\traw_c("""{func_c_body}""")'
            ),
        ).construct(),
    )


def _struct_c_func_decorator(parent_mod_name: str, func: FunctionType) -> None:
    if "return" not in func.__annotations__:
        raise SyntaxError(f"No return annotation on function {func.__name__}() from module '{parent_mod_name}'")
    if not (
        isinstance(func.__annotations__["return"], GenericAlias) and func.__annotations__["return"].__origin__ is tuple
    ):
        raise SyntaxError("@struct_c_func can only be used on functions that return a tuple")

    pyg3a.Main.func_types[func.__name__] = (
        _annotation_to_str(func.__annotations__["return"]),
        [_annotation_to_str(p_ann) for p_ann in func.__annotations__ if p_ann != "return"],
    )

    func_c_body: str = func(*((None,) * func.__code__.co_argcount)).strip()
    struct_name: str = f"__pyg3a_struct_{func.__name__}"

    pyg3a.Main.registry.register(struct_name, struct_name, TypeCategory.NONE)

    # Add struct to C project
    pyg3a.PyG3A._add_c_func(
        struct_name,
        f"struct {struct_name} {{\n"
        + "\n".join(
            [
                f"\t{pyg3a.Main.registry[_annotation_to_str(t)]} _{i};"
                for i, t in enumerate(func.__annotations__["return"].__args__)
            ]
        )
        + "\n};",
    )

    # Adjust the
    func.__annotations__["return"] = struct_name

    def init(self) -> None:
        self.__repr__ = lambda: struct_name

    struct_annotation: type = type(struct_name, (), {"__slots__": "__repr__", "__init__": init})

    pyg3a.PyG3A._add_c_func(
        func.__name__,
        CFunction(
            cst.parse_statement(
                # Map struct_name: str(struct_name) so we evaluate it to itself
                f'def {func.__name__}{inspect.signature(func, globals={struct_name: struct_annotation()}, eval_str=True)}:\n\traw_c("""{func_c_body}""")'
            ),
        ).construct(),
    )


def _syscall_decorator(parent_mod_name: str, number: int) -> Callable[[FunctionType], None]:
    def wrapper(func: FunctionType) -> None:
        if "return" not in func.__annotations__:
            raise SyntaxError(f"No return annotation on function {func.__name__}() from module '{parent_mod_name}'")

        ret_annotation: str = _annotation_to_str(func.__annotations__["return"])
        param_annotations: dict[str, str] = {
            p_name: _annotation_to_str(p_ann) for p_name, p_ann in func.__annotations__.items() if p_name != "return"
        }

        pyg3a.Main.func_types[func.__name__] = (ret_annotation, list(param_annotations.values()))

        pyg3a.PyG3A._add_c_func(
            f"__pyg3a_asm_{func.__name__}",
            f'extern "C" {pyg3a.Main.registry[ret_annotation]} {func.__name__}({
            ', '.join(
                [
                    f"{pyg3a.Main.registry[ann]} {name}" for name, ann in param_annotations.items()
                ]
            )
            }); \
            __asm__(".text; .align 2; .global _{func.__name__}; _{func.__name__}: \
                    mov.l sc_addr, r2; mov.l 1f, r0; jmp @r2; nop; 1: .long {number}; sc_addr: .long 0x80020070");',
        )

    return wrapper


@dataclass(slots=True, init=False, unsafe_hash=True)
class Function[Node]:
    name: Final[str]
    parent_mod_name: Final[str]
    func_def: Final[cst.FunctionDef]
    typ: Final[type[Node]]

    params: Final[tuple[Parameter, ...]]
    posonly_params: Final[tuple[Parameter, ...]]
    kwonly_params: Final[tuple[Parameter, ...]]

    kwargs: Final[Optional[Parameter]]
    starargs: Final[Optional[Parameter]]

    def __init__(self, func_def: cst.FunctionDef, parent_mod_name: str, typ: type[Node]) -> None:
        self.typ = typ

        self.name = func_def.name.value if self.typ is cst.Call else func_def.name.value.split("__iter__")[0]
        self.parent_mod_name = parent_mod_name
        self.func_def = func_def

        if self.typ is cst.For:
            # If the __iter__ function has pos-only params, then the first one is the var name
            # (i.e. it's not passed in by calls)
            if func_def.params.posonly_params:
                self.posonly_params = tuple([_gen_param(param) for param in func_def.params.posonly_params[1:]])
                self.params = tuple([_gen_param(param) for param in func_def.params.params])

            # Else if the __iter__ function has standard params, then the first one is the var name
            elif func_def.params.params:
                self.posonly_params = tuple([_gen_param(param) for param in func_def.params.posonly_params])
                self.params = tuple([_gen_param(param) for param in func_def.params.params[1:]])

            # We don't support passing the var name as a keyword param, so error
            else:
                raise SyntaxError("__iter__ functions must have a positional parameter to pass the var name into")
        else:
            self.posonly_params = tuple([_gen_param(param) for param in func_def.params.posonly_params])
            self.params = tuple([_gen_param(param) for param in func_def.params.params])

        self.kwonly_params = tuple([_gen_param(param) for param in func_def.params.kwonly_params])

        self.kwargs = _gen_param(func_def.params.star_kwarg) if func_def.params.star_kwarg else None
        self.starargs = _gen_param(func_def.params.star_arg) if type(func_def.params.star_arg) is cst.Param else None

        pyg3a.Main.func_types[self.name] = (
            node_to_code(func_def.returns.annotation),
            [param.py_type for param in self.posonly_params + self.params + self.kwonly_params],
        )

    def accepts(self, node: Node, scope: Scope) -> Optional["FunctionInstance[Node]"]:
        inst: FunctionInstance[Node] = FunctionInstance[Node](self, node, scope)
        if inst.acceptable():
            return inst

        return None


@dataclass(slots=True)
class FunctionInstance[Node]:
    function: Final[Function]
    node: Final[Node]
    scope: Final[Scope]
    complete_args: list[cst.Arg | Parameter] = lambda: []

    def acceptable(self) -> bool:
        if self.function.typ is cst.For:
            assert type(self.node.iter) is cst.Call

        call: cst.Call = self.node.iter if self.function.typ is cst.For else self.node

        # If we're not calling a function with the same name as ours, don't accept
        if self.function.name != Block._obj_to_c_str(call.func, scope=self.scope):
            return False

        logging.debug(self.function.name)

        # If too many args, we don't accept
        if (
            not self.function.kwargs
            and not self.function.starargs
            and len(call.args)
            > (len(self.function.params) + len(self.function.kwonly_params) + len(self.function.posonly_params))
        ):
            logging.debug("2")
            return False

        # If not enough args for just standard params, short-circuit and don't accept
        if len(call.args) < len([p for p in self.function.params if p.default is Never]):
            logging.debug("3")
            return False

        # Get the passed positional args
        pos_args: list[cst.Arg] | None = []
        kw_args: list[cst.Arg] | None = []

        for arg in call.args:
            if arg.keyword:
                # We're not worrying about evaluating **kwargs arguments
                if arg.star:
                    kw_args = None
                elif kw_args is not None:
                    kw_args.append(arg)
            else:
                # We're not worrying about evaluating *args arguments
                if arg.star:
                    pos_args = None
                elif pos_args is not None:
                    pos_args.append(arg)

        # If we can't process the pos and kw arg counts, short-circuit to accept
        if kw_args is None and pos_args is None:
            logging.debug("4")
            return True

        # Expanded list of arguments or their parameters if defaulted
        self.complete_args = []

        # The number of positional args
        checked_posargs: int = 0

        # If pos_args is None, we won't process the posargs
        if pos_args is not None:
            # Now we'll check the positional arguments
            self.complete_args.extend(pos_args)

            # Fill in with posonly defaults
            if len(pos_args) < len(self.function.posonly_params):
                for param in self.function.posonly_params[checked_posargs:]:

                    # If we haven't specified an argument and it doesn't have a default param, don't accept
                    if param.default is Never:
                        logging.debug("5")
                        return False

                    # Otherwise add the default's type to the list of specified args
                    self.complete_args.append(param)
                    checked_posargs += 1

            checked_posargs = len(pos_args) - len(self.function.posonly_params)

            # If we have too many positional params to fill, don't accept
            if checked_posargs > len(self.function.params):
                logging.debug("6")
                return False

        # If kw_args is None, we won't process the kwargs
        if kw_args is not None:
            # Map argument names
            arg_map: dict[str, cst.Arg] = {arg.keyword.value: arg for arg in kw_args}

            # Now generate the complete_args from our map
            for param in self.function.params[checked_posargs:] + self.function.kwonly_params:
                # Use default if necessary
                if param.name not in arg_map:
                    # If it's not specified and there's no default, don't accept
                    if param.default is Never:
                        logging.debug("7")
                        return False

                    # Otherwise add the default's type to the list of specified args
                    self.complete_args.append(param)
                else:
                    self.complete_args.append(arg_map[param.name])

        # This should hopefully work, but really I should write a test for it
        try:
            for arg, param in zip(
                self.complete_args,
                (self.function.posonly_params if pos_args is not None else tuple())
                + (self.function.params + self.function.kwonly_params if kw_args is not None else tuple()),
                strict=True,
            ):
                if isinstance(arg, Parameter):
                    # We must have defaulted so let's assume for now that it's fine
                    continue

                if node_type(arg.value, self.scope) != param.py_type:
                    return False
        except ValueError:
            return False

        return True

    def _call_get_args(self) -> tuple[list[str], dict[str, str]]:
        return (
            [
                param.to_arg(arg, self.scope)
                for arg, param in zip(
                    self.complete_args,
                    self.function.posonly_params + self.function.params + self.function.kwonly_params,
                )
                if isinstance(arg, cst.Arg) and not arg.keyword
            ],
            {
                arg.keyword.value: param.to_arg(arg, self.scope)
                for arg, param in zip(
                    self.complete_args,
                    self.function.posonly_params + self.function.params + self.function.kwonly_params,
                )
                if isinstance(arg, cst.Arg) and arg.keyword
            },
        )

    def _call_converter(self) -> str:
        args, kwargs = self._call_get_args()
        return self.eval_module_func(*args, **kwargs)

    def eval_module_func(self, *args: str, **kwargs: str):
        func_def: cst.FunctionDef = self.function.func_def

        untyped_funcdef: cst.FunctionDef = cst.FunctionDef(
            name=cst.Name(f"__pyg3a_{self.function.name}"),
            body=(
                cst.IndentedBlock(
                    body=[cst.SimpleStatementLine(body=[cst.Expr(cst.Call(func=cst.Name("locals")))])]
                    + list(func_def.body.body),
                    indent=func_def.body.indent,
                )
                if type(func_def.body) is cst.IndentedBlock
                else cst.SimpleStatementSuite(
                    body=[cst.Expr(cst.Call(func=cst.Name("locals")))]
                    + list(cast(cst.SimpleStatementSuite, func_def.body).body)
                )
            ),
            params=cst.Parameters(
                params=[cst.Param(param.name, default=param.default) for param in func_def.params.params],
                star_arg=(
                    cst.Param(func_def.params.star_arg.name, default=func_def.params.star_arg.default)
                    if type(func_def.params.star_arg) is cst.Param
                    else func_def.params.star_arg
                ),
                kwonly_params=[cst.Param(param.name, default=param.default) for param in func_def.params.kwonly_params],
                star_kwarg=(
                    cst.Param(func_def.params.star_kwarg.name, default=func_def.params.star_kwarg.default)
                    if func_def.params.star_kwarg
                    else None
                ),
                posonly_params=[
                    cst.Param(param.name, default=param.default) for param in func_def.params.posonly_params
                ],
                posonly_ind=func_def.params.posonly_ind,
            ),
        )

        custom_builtins: dict[str, Any] = builtins.__dict__.copy()
        custom_builtins["__import__"] = _importer
        custom_builtins["eval"] = lambda code: eval(code, {"__builtins__": {}}, {})

        globs: dict[str, Any] = {
            "__builtins__": custom_builtins,
            "c_func": functools.partial(_c_func_decorator, self.function.parent_mod_name),
            "struct_c_func": functools.partial(_struct_c_func_decorator, self.function.parent_mod_name),
            "syscall": functools.partial(_syscall_decorator, self.function.parent_mod_name),
        }

        def init(self, name) -> None:
            self.__repr__ = lambda: name

        for custom_type in pyg3a.Main.registry.all_cats:
            if custom_type not in builtins.__dict__:
                globs[custom_type] = type(
                    custom_type, (), {"__slots__": "__repr__", "__init__": functools.partial(init, name=custom_type)}
                )

        exec(node_to_code(untyped_funcdef), globs)
        return globs[f"__pyg3a_{self.function.name}"](*args, **kwargs)

    def _iter_converter(self, tabnum: int) -> str:
        args, kwargs = self._call_get_args()
        args.insert(0, self.node.target.value)
        lines: list[str] = [f"{tabnum * "\t"}for ({self.eval_module_func(*args, **kwargs)}) {{"]

        if self.function.func_def.returns is None:
            raise TypeError

        expressions = Block(
            self.node.body.body,
            tabnum + 1,
            self.scope.inner(self.node.target.value, _annotation_to_c(self.function.func_def.returns)),
        )
        lines.append(expressions.construct())

        lines.append(tabnum * "\t" + "}")

        return "\n".join(lines)

    def convert(self, **kwargs: Any) -> str:
        return self._call_converter() if self.function.typ is cst.Call else self._iter_converter(**kwargs)
