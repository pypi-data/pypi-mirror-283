"""
Generate command

Produce the required output files for a given YAML file
"""

import os
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

import click

from fgen.cmake_help import log_cmake_lists_help
from fgen.commands.base import cli
from fgen.data_models import (
    Package,
    PackageSharedElements,
    load_enum_defining_module,
    load_module_definition,
)
from fgen.wrapper_building import process_package


@cli.command(name="generate")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Overwrite any existing files",
)
@click.option(
    "--extension",
    "-e",
    help="""Name of the Python extension package.

    Normally, this will be something `<python_package_name>.<extension_module_name>`,
    e.g. `my_model._lib`.
    """,
    required=True,
)
@click.option(
    "--wrapper-directory",
    help="Directory in which to write the Python-Fortran wrapper(s).",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
)
@click.option(
    "--python-directory",
    help="Directory in which to write the python module(s).",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
)
@click.option(
    "--manager-directory",
    help="""Directory in which to write the derived type lifecycle manager(s)
    (Fortran-based).

    This defaults to the same directory as the yaml file(s)
    which define the derived type,
    which is generally where the Fortran code for the derived type is also located.
    If the YAML files come from more than one directory and this is not defined,
    an error is raised.""",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
)
@click.option(
    "--enum-definition",
    "-ed",
    help="""Yaml-file that holds the definition of an enum.

    As many of these as you like can be provided.
    Each needs to be behind its own option flag.
    For example,

    `fgen generate ... --enum-definition enum-file-1.yaml -ed enum-file-2.yaml`""",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    multiple=True,
)
@click.option(
    "--cmake-prefix",
    help="""Prefix for `CMakeLists.txt` help text.

    This prefix is applied to filenames when displaying the paths
    that will likely need to be added to your `CMakeLists.txt` file
    This can make it easier if you want to copy and paste
    the log messages later.""",
    default="<path-to-generated>",
)
@click.argument(
    "yaml_files",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    nargs=-1,
)
def generate_command(  # noqa: PLR0913
    force: bool,
    extension: str,
    wrapper_directory: str,
    python_directory: str,
    manager_directory: Optional[str],
    enum_definition: Optional[tuple[str, ...]],
    cmake_prefix: str,
    yaml_files: Iterable[str],
) -> None:
    """
    Autogenerate python and fortran code according to a collection of module definitions

    We assume that each file in YAML_FILES describes a module
    which exposes a Fortran derived type that we wish to expose to Python.
    The collection of modules is considered to be a package.

    This function writes 3 files for each module that is being wrapped:

    * manager - Lifecycle handling for derived types (in Fortran)

    * wrapper - Provides a fortran wrapper to the generated functions that can be
      made available to Python

    * python module - Python interface for creating, manipulating and interacting with
      the derived types.

    This function may also write other files necessary
    for wrapping the package as a whole.
    """
    if manager_directory is not None:
        manager_directory_to_use = manager_directory
    else:
        yaml_file_directories = tuple(os.path.dirname(fn) for fn in yaml_files)
        if len(set(yaml_file_directories)) > 1:
            msg = (
                "yaml files are in different directories. "
                "Please specify the manager directory "
                "(via the manager-directory option). "
                f"yaml file directories: {yaml_file_directories}"
            )
            raise ValueError(msg)

        manager_directory_to_use = yaml_file_directories[0]

    modules = tuple(load_module_definition(fn) for fn in yaml_files)

    if enum_definition:
        modules_enum_defining = tuple(
            load_enum_defining_module(Path(fn)) for fn in enum_definition
        )
    else:
        modules_enum_defining = ()

    package = Package(
        modules=modules,
        modules_enum_defining=modules_enum_defining,
    )
    # If we need, can make it so the initialisation of shared is configurable too.
    shared = PackageSharedElements()

    written_wrappers = process_package(
        package,
        shared=shared,
        extension=extension,
        manager_directory=Path(manager_directory_to_use),
        wrapper_directory=Path(wrapper_directory),
        python_directory=Path(python_directory),
        force=force,
    )

    log_cmake_lists_help(written_wrappers, cmake_prefix=cmake_prefix)
