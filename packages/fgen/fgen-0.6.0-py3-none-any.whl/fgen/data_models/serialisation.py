"""
Serialisation of our data models
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, TypedDict, TypeVar, Union, cast

from attrs import fields
from cattrs.preconf.pyyaml import make_converter
from typing_extensions import TypeAlias

from fgen.data_models.method import Method
from fgen.data_models.module import Module
from fgen.data_models.module_enum_defining import (
    EnumDefinition,
    ModuleEnumDefining,
)
from fgen.data_models.multi_return import MultiReturn
from fgen.data_models.value import Value

T = TypeVar("T")
converter = make_converter(
    detailed_validation=False, forbid_extra_keys=True, prefer_attrib_converters=True
)
UnstructuredElement: TypeAlias = dict[
    str, Union[str, int, float, list[Any], tuple[Any, ...]]
]
UnstructuredObject: TypeAlias = Union[
    UnstructuredElement, dict[str, "UnstructuredObject"]
]


def _add_name(
    inp: dict[str, UnstructuredObject], cls: type[dict[str, T]]
) -> dict[str, T]:
    """
    Add the name to attributes and methods automatically

    This avoids having to write schemas like

    .. ::code-block

    Attributes
    ----------
          k:
            name: k
            description: something

    Methods
    -------
          calculate:
            name: calculate
            description: something else

    Instead we can just write

    .. ::code-block

    Attributes
    ----------
          k:
            description: something

    Methods
    -------
          calculate:
            description: something else

    Where the name is inferred automatically

    Parameters
    ----------
    inp
        Unstructured object

    cls
        Type to which to structure the object

    Returns
    -------
        Structured object
    """
    value_type = cls.__args__[1]  # type: ignore

    res = {}

    if inp is None:
        raise ValueError(  # noqa: TRY003  # pragma: no cover
            f"Unexpected None when structuring {cls}"
        )

    for k, v in inp.items():
        for f in fields(value_type):
            if str(f.type).startswith("dict") and v.get(f.name) is None:
                raise ValueError(  # noqa: TRY003  # pragma: no cover
                    f"{f.name!r} in {k!r} is None but a dict was expected: {v}"
                )
        if "name" in v:
            if v["name"] != k:
                raise ValueError(  # noqa: TRY003
                    f"Inconsistent name for value: {k!r} and {v['name']!r}"
                )

        if value_type == Method:
            res[k] = converter.structure({"name": k} | v, value_type)
        else:
            to_structure = cast(dict[str, dict[str, str]], copy.deepcopy(v))
            to_structure["definition"]["name"] = k
            res[k] = converter.structure(to_structure, value_type)

    return res


converter.register_structure_hook_func(
    lambda t: any(
        t == add_name_type
        for add_name_type in (
            dict[str, Value],
            dict[str, MultiReturn],
            dict[str, Method],
        )
    ),
    _add_name,
)


def _infer_return_type(inp: UnstructuredObject, _: Any) -> Union[Value, MultiReturn]:
    if "unit" not in inp:
        return converter.structure(inp, Value)

    elif isinstance(inp["unit"], str):
        return converter.structure(inp, Value)

    elif isinstance(inp["unit"], (list, tuple)):
        return converter.structure(inp, MultiReturn)

    raise NotImplementedError(inp["unit"])


converter.register_structure_hook_func(
    lambda t: any(
        t == return_requires_inference_type
        for return_requires_inference_type in [
            Union[Value, MultiReturn],
        ]
    ),
    _infer_return_type,
)


class UnstructuredEnumValue(TypedDict):
    """Unstructured enum value type hint"""

    integer_value: int
    description: str


class UnstructuredEnumDefinition(TypedDict):
    """Unstructured enum definition type hint"""

    name: str
    description: str
    values: dict[str, UnstructuredEnumValue]


class UnstructuredEnumDefiningModule(TypedDict):
    """Unstructured enum defining module"""

    name: str
    description: str
    provides: UnstructuredEnumDefinition


def _structure_enum_defining_module(
    inp: UnstructuredEnumDefiningModule,
    target_type: type[ModuleEnumDefining],
) -> ModuleEnumDefining:
    injected_values = []
    for k, v in inp["provides"]["values"].items():
        injected_values.append({"str_value": k} | v)

    injected_provides = inp["provides"] | {"values": tuple(injected_values)}
    provides = converter.structure(injected_provides, EnumDefinition)

    return ModuleEnumDefining(
        name=inp["name"],
        description=inp["description"],
        provides=provides,
    )


converter.register_structure_hook_func(
    lambda t: t == ModuleEnumDefining,
    _structure_enum_defining_module,
)


def load_module_definition(filename: str) -> Module:
    """
    Read a YAML module definition file

    This module definition contains a description of the Fortran module
    that is being wrapped.

    Parameters
    ----------
    filename
        Filename to read

    Returns
    -------
        Loaded module definition
    """
    with open(filename, encoding="utf-8") as fh:
        txt = fh.read()

    return converter.loads(txt, Module)


def load_enum_defining_module(file: Path) -> ModuleEnumDefining:
    """
    Read a YAML enum defining module definition file

    This enum defining module file contains a description of a Fortran module
    that exposes an enum.

    Parameters
    ----------
    filename
        Filename to read

    Returns
    -------
        Loaded definition of the enum defining module
    """
    with open(file, encoding="utf-8") as fh:
        txt = fh.read()

    return converter.loads(txt, ModuleEnumDefining)
