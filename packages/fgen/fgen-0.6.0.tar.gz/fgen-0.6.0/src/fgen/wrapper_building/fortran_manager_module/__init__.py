"""
Generation of the Fortran manager module
"""

from pathlib import Path

from attrs import define

from fgen.data_models import Module, Package, PackageSharedElements
from fgen.jinja_environment import (
    JINJA_ENV,
    get_template_in_directory,
    post_process_jinja_rendering,
)


@define
class FortranManagerModuleBuilder:
    """
    Builder of Fortran manager modules
    """

    package: Package
    """
    Package for which the builder is building wrappers
    """

    module: Module
    """
    Module for which to build the wrapper
    """

    shared: PackageSharedElements
    """
    Elements which have to be shared across the package

    For example, the names of functions which are used in more than one wrapper module.
    """


def generate_fortran_manager_module(builder: FortranManagerModuleBuilder) -> str:
    """
    Generate the Fortran manager module

    Parameters
    ----------
    builder
        Builder to use to generate the Fortran manager module

    Returns
    -------
        Fortran manager module as code
    """
    template = get_template_in_directory(
        "fortran-manager-module.f90.jinja", Path(__file__).parent, JINJA_ENV
    )

    result = post_process_jinja_rendering(template.render(builder=builder))

    return result
