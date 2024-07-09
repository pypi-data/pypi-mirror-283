"""
Data model of a Fortran derived type
"""
from __future__ import annotations

from typing import Any, Optional, Union

from attrs import define, field

from fgen.data_models.method import Method
from fgen.data_models.multi_return import MultiReturn
from fgen.data_models.value import Value


@define
class FortranDerivedType:
    """
    Data model of a Fortran derived type
    """

    name: str
    """Name of the derived type"""

    description: str
    """Description of the derived type"""

    attributes: dict[str, Value] = field()
    """The derived type's attributes"""

    methods: dict[str, Method]
    """The derived type's methods"""

    # We may need the equivalent of this for methods.
    # I haven't thought through whether it makes sense to have a method
    # that requires a Fortran unit holder without any attribute
    # that has that requirement.
    @attributes.validator
    def _check_units_handling(self, attribute: Any, value: dict[str, Value]) -> None:
        attributes_requiring_fortran_units_holder = (
            self.fortran_units_holder_reliant_attributes
        )
        if attributes_requiring_fortran_units_holder:
            if self.fortran_units_holder is None:
                msg = (
                    "There are attributes with dynamic units, "
                    "but no attribute is specified as a ``fortran_units_holder``. "
                    "Attributes with dynamic units "
                    "that require a Fortran units holder: "
                    f"{attributes_requiring_fortran_units_holder}. "
                    f"{self=} {attribute=} {value=}"
                )
                raise ValueError(msg)

    @attributes.validator
    def _check_fortran_units_holder(
        self, attribute: Any, value: dict[str, Value]
    ) -> None:
        fortran_units_holders = [
            name
            for name, att in self.attributes.items()
            if att.definition.is_fortran_units_holder
        ]
        if not fortran_units_holders:
            # No Fortran units holders, fine here
            # (checked in _check_units_handling instead).
            return

        if len(fortran_units_holders) > 1:
            # Validation should prevent getting here, just in case
            msg = (
                "Cannot have more than one Fortran units holder. "
                "These attributes have `is_fortran_units_holder=True`: "
                f"{fortran_units_holders}"
            )
            raise ValueError(msg)

        fortran_units_holder = fortran_units_holders[0]
        if not self.attributes[fortran_units_holder].definition.expose_getter_to_python:
            msg = (
                "The Fortran units holder's getter must be exposed to Python. "
                f"This is not the case for `{fortran_units_holder}`"
            )
            raise ValueError(msg)

    @property
    def fortran_units_holder_reliant_attributes(self) -> tuple[str, ...]:
        """
        The attributes whose units are reliant on ``self.fortran_units_holder``

        Fortran doesn't have an equivalent of :mod:`pint`,
        hence units are just held as plain attributes instead.
        The units of these attributes is defined by the unit holding attribute.

        Returns
        -------
            Attributes that rely on the Fortran units holder to define their units.
        """
        return tuple(
            name
            for name, att in self.attributes.items()
            if att.dynamic_unit and not isinstance(att.dynamic_unit, str)
        )

    @property
    def fortran_units_holder(self) -> Union[str, None]:
        """
        The attribute on the Fortran derived type which holds the units

        This is often, but does not necessarily need to be, an attribute named `units`.

        Fortran doesn't have an equivalent of :mod:`pint`,
        hence units are just held as plain attributes instead.
        If a provided derived type has such an attribute,
        it can be accessed via this property

        Returns
        -------
            Attribute on the Fortran derived type which holds the units.
            If no attribute on the Fortran derived type holds units,
            ``None`` is returned.
        """
        fortran_units_holders = [
            name
            for name, att in self.attributes.items()
            if att.definition.is_fortran_units_holder
        ]
        if not fortran_units_holders:
            return None

        if len(fortran_units_holders) > 1:  # pragma: no cover
            # Validation should prevent getting here, just in case
            msg = (
                "Validation should have prevented this. "
                "Cannot have more than one Fortran units holder. "
                "These attributes have `is_fortran_units_holder=True`: "
                f"{fortran_units_holders}"
            )
            raise AssertionError(msg)

        return fortran_units_holders[0]

    @property
    def exposed_attributes(self) -> dict[str, Value]:
        """
        Get the attributes that are marked to be exposed to python

        Returns
        -------
            Collection of exposed attributes
        """
        return dict(
            filter(
                lambda item: item[1].definition.expose_getter_to_python,
                self.attributes.items(),
            )
        )

    @property
    def units(self) -> dict[str, Union[str, tuple[str, ...]]]:
        """
        Get the unit for each declared value in the derived type

        The unit for a given named value must be consistent across the derived type
        and the module which defines it.
        This includes the unit for ``attributes``, and in the ``parameter`` and
        ``return`` values for each ``method``.

        Raises
        ------
        ValueError
            Inconsistent units were found

        Returns
        -------
            Dictionary containing value names' as keys and the associated units
            as values.
        """
        # We are tracking the units for each possible source of units.
        # For each name we keep track of a tuple containing the method name
        # where the unit was declared and the unit.
        # For derived type attributes the "method name" is None.

        # Collect units from the attributes.
        unit_sources: dict[str, tuple[Optional[str], Union[str, tuple[str, ...]]]] = {
            key: (None, attr.unit)
            for key, attr in self.attributes.items()
            # Drop any attributes that don't have a unit
            if attr.unit is not None
        }

        # Collect units from the methods
        for method_name, method in self.methods.items():
            method_units = method.units

            # Check that the method units are consistent
            # with any previously declared units
            for name, method_unit in method_units.items():
                if name in unit_sources and unit_sources[name][1] != method_unit:
                    # Inconsistent unit declarations found

                    previous_source, previous_value = unit_sources[name]
                    if previous_source is not None:
                        previous_source_type = "method"
                    else:
                        previous_source_type = "derived type"
                        previous_source = self.name

                    raise ValueError(  # noqa: TRY003
                        f"Inconsistent units for attribute '{name}'. "
                        f"In the method '{method_name}' it has units '{method_unit}' "
                        f"whereas in the {previous_source_type} '{previous_source}' "
                        f"it has units '{previous_value}'"
                    )
                unit_sources[name] = (method_name, method_unit)

        return {key: value[1] for key, value in unit_sources.items()}

    @property
    def units_multi_return(self) -> dict[str, tuple[str, ...]]:
        """
        Get units declared in this object, if the units are tuples

        This occurs if the units apply to a return statement that returns
        multiple values

        Returns
        -------
            Dictionary containing value names' as keys and the associated units
            as values (all these values are plain strings).
        """
        return {k: v for k, v in self.units.items() if not isinstance(v, str)}

    def get_dynamic_unit_source(
        self, value: Union[MultiReturn, Value]
    ) -> Optional[str]:
        """
        Get the source of the dynamic unit for a given value

        Parameters
        ----------
        value
            Value for which to get the source of the dynamic unit

        Returns
        -------
            Source of the dynamic unit for ``value``
        """
        if not value.dynamic_unit:
            return None

        if isinstance(value.dynamic_unit, str):
            return value.dynamic_unit

        # If we have a dynamic unit, but it isn't defined as a string,
        # then it comes from the Fortran units holder attribute of self.
        return f"self.{self.fortran_units_holder}"
