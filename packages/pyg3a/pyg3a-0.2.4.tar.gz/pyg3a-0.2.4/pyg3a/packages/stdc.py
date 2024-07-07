# TO BE IMPLEMENTED: @cst_types
@cst_types
def ref(var: cst.Name) -> any:
    return f"&{var}"


@cst_types
def ref(var: cst.Attribute) -> any:
    return f"&{var}"


def deref(reference: any) -> any:
    return f"*({reference})"


def __registry_types_pyg3a() -> dict[str, tuple[str, TypeCategory]]:
    PY_C_TYPES: dict[str, tuple[str, TypeCategory]] = {}
    PY_C_TYPES["unslong"] = ("unsigned long", TypeCategory.INTEGERS)
    PY_C_TYPES["unsshort"] = ("unsigned short", TypeCategory.INTEGERS)

    return PY_C_TYPES
