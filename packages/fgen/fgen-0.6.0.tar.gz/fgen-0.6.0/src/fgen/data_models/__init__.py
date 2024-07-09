"""
Data models

These data models describe the configuration that is used by this package
and the schema used to serialize and validate any configuration that is loaded.
For a more detailed description, see :ref:`overview-reference`.

Each module that is being wrapped is represented
using a :class:`~fgen.data_models.module.Module`
and can be loaded from disk using
:func:`~fgen.data_models.serialisation.load_module_definition`.
"""

from __future__ import annotations

from fgen.data_models.fortran_derived_type import FortranDerivedType
from fgen.data_models.method import Method
from fgen.data_models.module import Module
from fgen.data_models.module_enum_defining import ModuleEnumDefining
from fgen.data_models.module_requirement import ModuleRequirement
from fgen.data_models.multi_return import MultiReturn
from fgen.data_models.package import Package
from fgen.data_models.package_shared_elements import PackageSharedElements
from fgen.data_models.serialisation import (
    converter,
    load_enum_defining_module,
    load_module_definition,
)
from fgen.data_models.unitless_value import UnitlessValue
from fgen.data_models.value import Value

__all__ = [
    "FortranDerivedType",
    "Method",
    "Module",
    "ModuleEnumDefining",
    "ModuleRequirement",
    "MultiReturn",
    "Package",
    "PackageSharedElements",
    "Value",
    "UnitlessValue",
    "converter",
    "load_enum_defining_module",
    "load_module_definition",
]
