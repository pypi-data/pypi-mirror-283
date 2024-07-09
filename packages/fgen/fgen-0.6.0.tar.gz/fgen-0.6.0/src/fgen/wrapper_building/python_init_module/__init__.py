"""
Generation of the Python init module
"""
from __future__ import annotations

from pathlib import Path

from fgen.data_models import (
    Package,
)
from fgen.jinja_environment import (
    JINJA_ENV,
    get_template_in_directory,
    post_process_jinja_rendering,
)
from fgen.wrapper_building.formatting import format_python_code


def generate_python_init_module(package: Package) -> str:
    """
    Generate the Python init module

    Parameters
    ----------
    package
        Package in which the module lives

    Returns
    -------
        Python init file as code
    """
    # Not using the builder pattern for this module due to how simple the output is

    template = get_template_in_directory(
        "python-init-module.py.jinja", Path(__file__).parent, JINJA_ENV
    )

    result = post_process_jinja_rendering(template.render())

    return format_python_code(result)
