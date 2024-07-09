"""
Data model of module requirements
"""

from __future__ import annotations

from attrs import define


@define
class ModuleRequirement:
    """
    Data model of a module requirement

    These specifications are used to define the requirements of a module,
    i.e. the other modules it depends on.

    We don't currently validate these at generation-time.
    If they are wrong, the module will fail to compile
    or, in the case of an incorrect :attr:`~python_module`,
    will raise an ImportError at run-time.
    """

    provides: str
    """
    Name of the derived type defined in the required module
    """

    fortran_module: str
    """
    Name of the required fortran module

    This should point to the fortran module
    that contains the definition of the required derived type.
    """

    python_module: str
    """
    Name of the python module that exposes the Python wrapper of the derived type

    This module should declare a class
    that has a name equal to the value of :attr:`~provides`.
    """
