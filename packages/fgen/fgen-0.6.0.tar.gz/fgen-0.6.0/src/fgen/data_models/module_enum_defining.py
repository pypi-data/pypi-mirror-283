"""
Data model of a module that defines an enum
"""
from __future__ import annotations

from attrs import define


@define
class EnumValue:
    """
    Data model of an enum value
    """

    description: str
    """Description of the value"""

    str_value: str
    """The string value of the enum."""

    integer_value: int
    """
    The integer value of the enum.

    Ensures consistency across Python and Fortran.
    """


@define
class EnumDefinition:
    """
    Data model of an enum definition
    """

    name: str
    """Name of the enum (in both Fortran and Python)"""

    description: str
    """Description of enum"""

    values: tuple[EnumValue, ...]
    """Values the enum can take"""


@define
class ModuleEnumDefining:
    """
    Data model of a module that defines an enum
    """

    name: str
    """Name of the module"""

    description: str
    """Description of the module"""

    provides: EnumDefinition
    """Enum that this module defines"""
