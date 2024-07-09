"""
Shared elements of a package data model
"""
from __future__ import annotations

from attrs import define


@define
class PackageSharedElements:
    """
    Data model of the shared elements in a package

    This helps us define the shared elements across the package.
    For example, the names of callables
    that are defined in Fortran but used in Python.
    """

    @property
    def from_build_args_name(self) -> str:
        """
        Name of the Python function which creates an object from its build arguments
        """
        return "from_build_args"

    @property
    def finalise_method_name(self) -> str:
        """
        Name of the callables which finalise instances
        """
        return "finalize"

    @property
    def fortran_build_callable_name(self) -> str:
        """
        Name of Fortran callables which build instances
        """
        return "instance_build"

    @property
    def fortran_get_free_instance_number_callable_name(self) -> str:
        """
        Name of Fortran callables which get the number of a free/available instance
        """
        return "get_free_instance_number"

    @property
    def fortran_get_instance_callable_name(self) -> str:
        """
        Name of Fortran callables which get an instance
        """
        return "get_instance"

    @property
    def fortran_instance_finalise_callable_name(self) -> str:
        """
        Name of Fortran callables finalise an instance
        """
        return "instance_finalize"

    @property
    def fortran_wrapper_method_prefix(self) -> str:
        """
        Prefix to use when creating the Fortran wrapper equivalent of methods
        """
        return "i_"  # i for 'instance'

    @property
    def n_fortran_instances_to_expose(self) -> int:
        """
        Number of Fortran instances to expose

        Once the user requests more instances than this, an error is raised.
        """
        return 4096

    @property
    def no_setters_suffix(self) -> str:
        """
        Suffix to use when creating the no setters version of our wrapper classes
        """
        return "NoSetters"
