"""
Package data model
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Optional, Union

import attr
from attrs import define, field

from fgen.data_models.module import Module
from fgen.data_models.module_enum_defining import ModuleEnumDefining
from fgen.data_models.multi_return import MultiReturn
from fgen.data_models.value import Value


class NoProvidingModuleError(ValueError):
    """
    Exception raised when no module provides a given type
    """

    def __init__(
        self, sought_type: str, value: Union[MultiReturn, Value], package: Package
    ):
        error_msg = (
            f"No module provides {sought_type}, which is the type of {value}. "
            f"We searched in {package=}."
        )

        super().__init__(error_msg)


@define
class Package:
    """
    Data model of a package

    It isn't clear that our package is exactly like a typical Python/Fortran package,
    so it is best to think of it exactly as it is for now:
    a Package is a collection of :obj:~`fgen.data_models.Module`'s.
    While the naming is similar to the Package > Module hierarchy used by Python,
    they should be treated as different concepts.
    """

    modules: tuple[Module, ...] = field()
    """
    Collection of modules that define derived types used within the package
    """

    modules_enum_defining: tuple[ModuleEnumDefining, ...] = field(factory=tuple)
    """
    Collection of modules that define enums used within the package
    """

    @modules.validator
    def _modules_provide_unique(
        self, attribute: attr.Attribute[Any], value: tuple[Module, ...]
    ) -> None:
        provided_derived_types_modules = defaultdict(list)

        # Multiple loops as mypy being silly
        for module in value:
            provided_derived_types_modules[module.provides.name].append(module.name)

        for module_enum_defining in self.modules_enum_defining:
            provided_derived_types_modules[module_enum_defining.provides.name].append(
                module_enum_defining.name
            )

        not_unique = tuple(
            (k, sorted(v))
            for k, v in provided_derived_types_modules.items()
            if len(v) > 1
        )
        if not_unique:
            duplicate_type_info = "\n".join(
                (
                    f"Provided type `{provided_type}` is provided by: {provided_by}"
                    for provided_type, provided_by in not_unique
                )
            )
            msg = (
                "The following derived types are provided by more than one module: "
                f"{duplicate_type_info}"
            )

            raise ValueError(msg)

    # Can cache this if we need speed
    def get_module_that_provides_values_type(
        self, value: Union[MultiReturn, Value]
    ) -> Module:
        """
        Get the module that provides a value's data type

        Parameters
        ----------
        value
            Value of which to find the data type provider

        Returns
        -------
            Module that provides ``value``

        Raises
        ------
        NoProvidingModuleError
            No module that provides ``value``'s data type is part of ``self.modules``.
        """
        fdt = value.definition.as_fortran_data_type()
        sought_type = fdt.equivalent_python_type
        if "tuple" in sought_type:
            sought_type = fdt.base_python_type

        for module in self.modules:
            if module.provides.name == sought_type:
                return module

        raise NoProvidingModuleError(sought_type=sought_type, value=value, package=self)

    def find_providing_module(
        self, value: Union[MultiReturn, Value]
    ) -> Optional[Module]:
        """
        Find the module that provides a value's data type

        If no module provides the value's data type, ``None`` is returned.

        Parameters
        ----------
        value
            Value of which to find the data type provider

        Returns
        -------
            Module that provides ``value``.
            If no module provides the value, ``None`` is returned.
        """
        try:
            return self.get_module_that_provides_values_type(value)
        except NoProvidingModuleError:
            return None
