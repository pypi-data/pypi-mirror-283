"""
Data model for how we pass data from Python to Fortran
"""
from __future__ import annotations

from typing import Optional

from attrs import define


@define
class PassingToFortranSteps:
    """
    Container for holding the steps required to pass data to Fortran
    """

    preparatory_python_calls: Optional[str]
    """Calls required in Python to prepare to pass the data to Fortran"""

    fortran_module_callable_args: tuple[tuple[str, str], ...]
    """
    Tuple of argument-value pairs to pass to the Fortran module callable

    The first element of each element in ``fortran_module_callable_args``
    is the name expected by Fortran,
    the second element is the name of the Python variable.

    There might be differences from the user-facing Python arguments,
    because we don't always pass values straight through.
    """

    @property
    def fortran_callable_arg_list(self) -> list[str]:
        """
        Argument list to use when calling a Fortran callable

        Note that this may not be the entire argument list,
        it is only the calls for the arguments managed by ``self``.
        """
        return [
            f"{arg_fortran}={arg_python}"
            for arg_fortran, arg_python in self.fortran_module_callable_args
        ]
