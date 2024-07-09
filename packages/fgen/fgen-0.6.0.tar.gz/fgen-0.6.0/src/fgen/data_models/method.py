"""
Data model of a method
"""
from __future__ import annotations

from typing import Union

from attrs import define

from fgen.data_models.multi_return import MultiReturn
from fgen.data_models.value import Value


@define
class Method:
    """
    Data model of a Fortran method

    This method is assumed to be part of a
    :class:`~fgen.data_models.fortran_derived_type.FortranDerivedType`.

    This function can have multiple :attr:`parameters`
    and a single, optional :attr:`returns` value.
    """

    name: str
    """Name of the function in Fortran"""

    description: str
    """Description of what the function does"""

    parameters: dict[str, Value]
    """
    Collection of named parameters of the function

    Currently, only :obj:`ValueDefinition` is supported because
    we assume that each parameter only refers to
    one value. If you think this assumption should be
    relaxed, please raise an issue illustrating your use
    case.
    """

    returns: Union[Value, MultiReturn]
    """Return value of the function"""

    @property
    def units(self) -> dict[str, Union[str, tuple[str, ...]]]:
        """
        Units used in the method

        Includes units from of the parameters and the return value.

        Raises
        ------
        ValueError
            If different units are supplied for a given parameter name

        Returns
        -------
            Collection of parameter names and associated units
        """
        res: dict[str, Union[str, tuple[str, ...], None]] = {
            key: parameter.unit for key, parameter in self.parameters.items()
        }

        if self.returns:
            rn = self.returns.definition.name  # rn = return's name
            if rn in res and res[rn] != self.returns.unit:
                raise ValueError(  # noqa: TRY003
                    f"Inconsistent units for attribute '{rn}'. "
                    f"In the input parameters it has units '{res[rn]}' "
                    f"whereas in the returns it has units '{self.returns.unit}'"
                )

            res[rn] = self.returns.unit

        # Drop any None units
        return {k: v for k, v in res.items() if v is not None}
