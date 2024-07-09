"""
Generation of the Python enums module

This holds the Python equivalent of any enums defined in Fortran.
"""
from __future__ import annotations

from pathlib import Path

from fgen.data_models import Package
from fgen.jinja_environment import (
    JINJA_ENV,
    get_template_in_directory,
    post_process_jinja_rendering,
)
from fgen.wrapper_building.formatting import format_python_code


def generate_python_enums_module(
    package: Package,
) -> str:
    """
    Generate the Python enums module

    Parameters
    ----------
    package
        Package for which to generate the Python enums module

    Returns
    -------
        Python enums module
    """
    # Not using the builder pattern for this module due to how simple the output is

    template = get_template_in_directory(
        "python-enums-module.py.jinja", Path(__file__).parent, JINJA_ENV
    )
    template_enum = get_template_in_directory(
        "python-enum-definition.py.jinja", Path(__file__).parent, JINJA_ENV
    )

    enums = []
    for module_enum_defining in package.modules_enum_defining:
        enums.append(
            template_enum.render(enum_definition=module_enum_defining.provides)
        )

    result = post_process_jinja_rendering(template.render(enums=enums))

    return format_python_code(result)
