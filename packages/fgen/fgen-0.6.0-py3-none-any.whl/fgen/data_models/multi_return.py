"""
Data model of a return value that contains multiple values
"""
from __future__ import annotations

from typing import Any, Optional, Union

from attrs import define, field

from fgen.data_models.unitless_value import UnitlessValue


@define
class MultiReturn:  # type: ignore # mypy confused by converter
    """
    Data model for a return type that returns more than one value

    This defines the returned values' units, Fortran data type and other metadata.
    It is the combination of a :obj:`UnitlessValueDefinition`
    and information about the units of each returned value.
    """

    definition: UnitlessValue
    """Definition of the value's key information"""

    unit: Optional[tuple[str, ...]] = field(  # type: ignore # mypy confused by converter
        default=None,
        converter=lambda x: tuple(x) if x is not None and not isinstance(x, str) else x,
    )
    """
    Units of the returned values

    The units must be able to parsed by `pint`
    and be present in the :obj:`pint.UnitRegistry`
    being used by the application (normal rules for pint).
    Some examples include: "kg", "1 / month".

    A unit is required for all numeric-types (i.e. integer, real, complex).
    For non-numeric values, the unit is unused.
    """

    dynamic_unit: Union[bool, str] = False
    """
    Whether the units should be inferred dynamically, rather than statically

    Support for this is currently not implemented.
    If you require this feature, please raise an issue.
    """

    @unit.validator
    def _check_unit(self, attribute: Any, value: tuple[str, ...] | None) -> None:
        if self.dynamic_unit:
            raise NotImplementedError()

        if self.definition.is_numeric_type:
            if value is None:
                raise ValueError(  # noqa: TRY003
                    f"A unit is required for: {self.definition.name}"
                )

            if not isinstance(value, tuple) or not all(
                isinstance(v, str) for v in value
            ):
                raise TypeError(  # noqa: TRY003
                    f"The unit for {self.definition.name} must be a tuple of strings, "
                    f"received: {value!r}"
                )

            dimension_attribute_spec = (
                self.definition.as_fortran_data_type().dimension_attribute_specification
            )
            if dimension_attribute_spec is None:
                raise ValueError(  # noqa: TRY003
                    "The Fortran method must return "
                    "more than one value for this to work. "
                    f"{self.definition.fortran_type=}"
                )

            dimensions = dimension_attribute_spec.dimensions
            if len(dimensions) > 1:
                raise NotImplementedError(
                    "Not sure which way to put the dimensions/units to make this work"
                )

            if len(value) != dimensions[0]:
                raise ValueError(  # noqa: TRY003
                    "The number of return units "
                    "should match the number of returned values. "
                    f"{value=} {dimensions=} {self.definition.fortran_type=}"
                )

    @property
    def requires_units(self) -> bool:
        """
        Whether this value requires units or not

        Returns
        -------
            ``True`` if this value requires units, ``False`` otherwise.
        """
        return (not self.dynamic_unit) and self.definition.is_numeric_type
