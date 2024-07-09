"""
Data model of a value (e.g. parameter, single return value)
"""
from __future__ import annotations

from typing import Any, Optional, TypeVar, Union

from attrs import define, field

from fgen.data_models.unitless_value import UnitlessValue

T = TypeVar("T")


def no_conversion(inp: T) -> T:
    """
    Identity function, just returns what it is given i.e. performs no conversion

    The use case for this is disabling type conversion with :mod:`cattrs`
    and :mod:`attrs`. In order to get :mod:`cattrs` to not convert stuff,
    you have to tell the converter a) to prefer attrs converters (i.e. use
    ``prefer_attrib_converters=True`` when creating your :mod:`cattrs`
    converter) and b) actual supply a converter to your :mod:`attrs`
    attribute. If you don't actually want to do any conversion, then you
    need an identity function (otherwise, :mod:`cattrs` will assume you
    didn't think about conversion and inject its own conversion). This
    lets the validator handle type checking etc., rather than having that
    check happen in a separate spot (without any context about what is
    being checked etc.).

    Parameters
    ----------
    inp
        Input

    Returns
    -------
        ``inp``, unchanged.
    """
    return inp


@define
class Value:
    """
    Data model of a value

    This defines the value's unit, Fortran data type and other metadata.
    It is the combination of a :obj:`UnitlessValueDefinition` and unit information.
    """

    definition: UnitlessValue
    """Definition of the value's key information"""

    unit: Optional[str] = field(default=None, converter=no_conversion)
    """
    Unit of the value

    The unit must be able to parsed by `pint`
    and be present in the :obj:`pint.UnitRegistry`
    being used by the application (normal rules for pint).
    Some examples include: "kg", "1 / month".

    A unit is required for all numeric-types (i.e. integer, real, complex)
    that don't have :attr:`dynamic_unit` set.
    For non-numeric values, no unit is unused.
    """

    dynamic_unit: Union[bool, str] = False
    """
    Whether the unit should be inferred dynamically, rather than statically

    If this is ``True``, we will infer the unit
    using the units of passed :obj:`pint.Quantity`'s.
    When passing these values to Fortran,
    the unit will be extracted and passed to Fortran as a string
    to the attribute whose
    :py:attr:`~fgen.data_models.unitless_value.UnitlessValue.is_fortran_units_holder`
    is ``True``.
    If :attr:`dynamic_unit` is ``True``, when retrieving the values from Fortran,
    the unit will be requested from Fortran too
    (from the attribute whose
    :py:attr:`~fgen.data_models.unitless_value.UnitlessValue.is_fortran_units_holder`
    is ``True``)
    and added to the return value to make a :obj:`pint.Quantity` before returning.

    If this is a string, we assume this tells us where to retrieve the unit information
    from on the Python side (i.e. the string should be valid Python code).
    """

    @unit.validator
    def _check_unit(self, attribute: Any, value: str | None) -> None:
        if self.requires_units:
            if value is None:
                raise ValueError(  # noqa: TRY003
                    f"A unit is required for: {self.definition.name}"
                )

            if not isinstance(value, str):
                raise TypeError(  # noqa: TRY003
                    f"The unit for {self.definition.name} must be a string, "
                    f"received: {value}"
                )

    @property
    def requires_units(self) -> bool:
        """
        Whether this value requires units or not

        Returns
        -------
            ``True`` if this value requires units, ``False`` otherwise.
        """
        # TODO: loosen this. Not all numeric types require units
        # (e.g. integers that represent sizes of things).
        return (not self.dynamic_unit) and self.definition.is_numeric_type
