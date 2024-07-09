"""
Data model of a value, excluding units
"""

from __future__ import annotations

from typing import Any

from attrs import define, field, validators

from fgen.fortran_parsing import FortranDataType

_NUMERIC_TYPE_STRINGS: list[str] = ["float", "int"]
"""
Strings that can appear in Python types that indicate that the Python type is numeric
"""


@define
class UnitlessValue:
    """
    Data model of a value excluding units

    This defines the value's Fortran data type and other metadata.
    It also allows us to get the equivalent Python type.
    """

    name: str
    """Name of the value"""

    description: str
    """Description of the value"""

    fortran_type: str = field(validator=[validators.instance_of(str)])
    """
    The value's fortran type

    The following built-in Fortran types are supported:

    * integer
    * real
    * real(8)
    * character

    Some additional attributes are supported including:

    * fixed length dimensions
    * automatic explicit length dimensions
      (e.g. using a variable "n" to specify the size of a dimension)
    """

    is_fortran_units_holder: bool = False
    """
    Is this value the attribute which specifies the units in the Fortran derived type?

    If ``True``, it is not not included in Python wrappers,
    instead being passed automatically to Fortran
    based on the units extracted from :mod:`pint` quantities in Python.
    """

    expose_getter_to_python: bool = True
    """
    Should a getter for this value be exposed to Python?

    If ``True``, we expose a getter for this value to Python, otherwise we don't.
    """

    expose_setter_to_python: bool = False
    """
    Should a setter for this value be exposed to Python?

    If ``True``, we expose a setter for this value to Python, otherwise we don't.
    """

    @fortran_type.validator
    def _check_fortran_type(self, attribute: Any, value: str) -> None:
        try:
            FortranDataType.from_str(value)
        except Exception as exc:
            raise ValueError(  # noqa: TRY003
                f"Unsupported fortran type: {value}"
            ) from exc

    @property
    def is_numeric_type(self) -> bool:
        """
        Whether this definition defines a numeric type or not

        Returns
        -------
            ``True`` if this definition defines a numeric type, ``False`` otherwise.
        """
        pt = self.python_type_as_str()
        return any(t in pt for t in _NUMERIC_TYPE_STRINGS)

    @property
    def is_python_str_type(self) -> bool:
        """
        Whether this definition corresponds to a string

        The concept of a string obviously only applies in Python.
        In Fortran, the equivalent is a character type.

        Returns
        -------
            ``True`` if this definition defines a type
            whose Python equivalent is string,
            ``False`` otherwise.
        """
        pt = self.python_type_as_str()

        return pt == "str"

    @property
    def is_python_bool_type(self) -> bool:
        """
        Whether this definition corresponds to a boolean

        The concept of a boolean obviously only applies in Python.
        In Fortran, the equivalent is a logical type.

        Returns
        -------
            ``True`` if this definition defines a type
            whose Python equivalent is boolean,
            ``False`` otherwise.
        """
        pt = self.python_type_as_str()
        return pt == "bool"

    def as_fortran_data_type(self) -> FortranDataType:
        """
        Convert ``self`` to its equivalent ``FortranDataType``
        """
        return FortranDataType.from_str(self.fortran_type)

    def python_type_as_str(self) -> str:
        """
        Determine the string representation of the Python type

        The python templator uses this function to translate a Python
        type to a string so that it can correctly be read by Python.
        If these type hints are converted to a string naively, the
        corresponding string will not be able to be read by Python as a valid type hint.

        Returns
        -------
            String representation of :attr:`python_type`
        """
        return self.as_fortran_data_type().equivalent_python_type
