"""
:mod:`fgen`'s wrapper building module
"""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Callable, Protocol, TypeVar, Union

from attrs import define
from loguru import logger

from fgen.data_models import Module, Package, PackageSharedElements
from fgen.wrapper_building.fortran_manager_module import (
    FortranManagerModuleBuilder,
    generate_fortran_manager_module,
)
from fgen.wrapper_building.fortran_wrapper_module import (
    FortranWrapperModuleBuilder,
    generate_fortran_wrapper_module,
)
from fgen.wrapper_building.python_enums_module import generate_python_enums_module
from fgen.wrapper_building.python_init_module import generate_python_init_module
from fgen.wrapper_building.python_wrapper_module import (
    PythonWrapperModuleBuilder,
    generate_python_wrapper_module,
)

AvailableBuilders = Union[
    FortranManagerModuleBuilder, FortranWrapperModuleBuilder, PythonWrapperModuleBuilder
]
T_builder = TypeVar("T_builder", bound=AvailableBuilders)
T_contra = TypeVar("T_contra", contravariant=True)


def try_to_write_file(file: Path, contents: str) -> None:
    """
    Try to write a file to disk, logging an exception if this fails.

    Parameters
    ----------
    file
        File to write to.

    contents
        Contents to write in the file.
    """
    try:
        with open(file, mode="w", encoding="utf-8") as fh:
            fh.write(contents)
    except Exception:
        logger.exception(
            f"Error encountered while trying to write {file=} with {contents=}"
        )
        raise


def write_file_with_checks(
    file: Path,
    desc: str,
    generate_content: Callable[[], str],
    keep_existing: bool = False,
    force: bool = False,
) -> Path:
    """
    Write a file, first checking what to do if the file already exists.

    Parameters
    ----------
    file
        Path in which the file will be written if the checks pass.

    desc
        Description of the file which will be written if the checks pass.
        Only used for logging.

    generate_content
        Function which generates the contents of the file.
        This is only called if the file is to be written.

    keep_existing
        Whether to always keep existing files.
        If this is ``True``, if a file exists, it is not overwritten.

    force
        Whether to force overwrite an existing file.
        If this is ``True``, if a file exists, it is overwritten.

    Returns
    -------
        Path to the written file (or existing file if it already exists)

    Raises
    ------
    FileExistsError
        ``file`` exists and no flags are set to specify what to do.

    ValueError
        Both ``keep_existing`` and ``force`` are ``True``.
        ``force`` will never be used in this case, hence an error is raised.
    """
    if keep_existing and force:
        msg = (
            "Both ``keep_existing`` and ``force`` are ``True``. "
            "``force`` will never be used in this case. "
            "Please update your arguments."
        )
        raise ValueError(msg)

    if file.exists():
        if keep_existing:
            logger.info(f"Existing file will be kept: {file=}")
            return file

        if not force:
            logger.error("Existing file should not be overwritten")
            raise FileExistsError(file)

        logger.warning(
            f"{force=}, existing file will be forcefully overwritten: {file=}"
        )

    contents = generate_content()
    try_to_write_file(file, contents)
    logger.info(f"Wrote {desc} to {file}")

    return file


class ModuleWrapperGeneratorCallableLike(Protocol[T_contra]):
    """
    Callable that can generate a wrapper for a module
    """

    def __call__(self, builder: T_contra) -> str:
        """
        Generate the wrapper
        """


@define
class WrittenWrappers:
    """Written wrappers"""

    manager_file: Path
    """Path to the manager file"""

    wrapper_file: Path
    """Path to the wrapper file"""


def write_module_wrappers(  # noqa: PLR0913
    package: Package,
    shared: PackageSharedElements,
    module: Module,
    manager_directory: Path,
    wrapper_directory: Path,
    python_directory: Path,
    extension: str,
    force: bool,
) -> WrittenWrappers:
    """
    Write the wrappers for a module

    Parameters
    ----------
    package
        Package this module belongs to

    shared
        Shared elements across ``package``

    module
        Module to write wrappers for

    manager_directory
        Directory in which to write the manager wrappers

    wrapper_directory
        Directory in which to write the Fortran wrappers

    python_directory
        Directory in which to write the Python wrappers

    extension
        Name of the extension module that will be called from Python

    force
        Whether to force overwrite existing files or not

    Returns
    -------
        The written wrappers
    """
    wmw_partial = functools.partial(
        write_module_wrapper,
        force=force,
    )
    manager_file = wmw_partial(
        desc="Fortran manager module",
        generator_function=generate_fortran_manager_module,
        builder=FortranManagerModuleBuilder(
            package=package, shared=shared, module=module
        ),
        file_suffix="_manager.f90",
        outdir=manager_directory,
    )
    wrapper_file = wmw_partial(
        desc="Fortran wrapper module",
        generator_function=generate_fortran_wrapper_module,
        builder=FortranWrapperModuleBuilder(
            package=package, shared=shared, module=module
        ),
        file_suffix="_wrapped.f90",
        outdir=wrapper_directory,
    )
    wmw_partial(
        desc="Python wrapper module",
        generator_function=functools.partial(
            generate_python_wrapper_module, extension=extension
        ),
        builder=PythonWrapperModuleBuilder(
            package=package, shared=shared, module=module
        ),
        file_suffix=".py",
        outdir=python_directory,
    )

    return WrittenWrappers(
        manager_file=manager_file,
        wrapper_file=wrapper_file,
    )


def write_module_wrapper(  # noqa: PLR0913
    desc: str,
    generator_function: ModuleWrapperGeneratorCallableLike[T_builder],
    builder: T_builder,
    file_suffix: str,
    outdir: Path,
    force: bool,
) -> Path:
    """
    Write a wrapper for a module

    Parameters
    ----------
    desc
        Description of the wrapper being written (used for logging)

    generator_function
        Function that generates the wrapper's contents

    builder
        The builder to use in combination with ``generator_function``
        to generate the wrapper's contents

    file_suffix
        The suffix to apply to the builder's truncated name.
        This combination defines the filename.

    outdir
        Directory in which to write the wrapper.

    force
        Whether to force overwrite existing files or not.

    Returns
    -------
        Path to the file that was written
    """
    return write_file_with_checks(
        file=outdir / f"{builder.module.truncated_name}{file_suffix}",
        desc=desc,
        generate_content=functools.partial(generator_function, builder=builder),
        force=force,
    )


class PackageWrapperGeneratorCallableLike(Protocol):
    """
    Callable that can generate a wrapper for a package
    """

    def __call__(self, package: Package) -> str:
        """
        Generate the wrapper
        """


def write_package_wrapper(  # noqa: PLR0913
    package: Package,
    desc: str,
    generator_function: PackageWrapperGeneratorCallableLike,
    outdir: Path,
    filename: str,
    keep_existing: bool = False,
    force: bool = False,
) -> None:
    """
    Write a wrapper for the package

    Parameters
    ----------
    package
        Package for which to write the wrapper.

    desc
        Description of the wrapper being written (used for logging).

    generator_function
        Function to call to generate the wrapper's contents.

    outdir
        Directory in which to write the wrapper.

    filename
        Name of the file in which to write the wrapper.

    keep_existing
        Whether to keep existing files, irrespective of the value of ``force``.

    force
        Whether to force overwrite existing files.
    """
    write_file_with_checks(
        file=outdir / filename,
        desc=desc,
        generate_content=functools.partial(generator_function, package=package),
        force=force,
        keep_existing=keep_existing,
    )


def process_package(  # noqa: PLR0913
    package: Package,
    shared: PackageSharedElements,
    extension: str,
    manager_directory: Path,
    wrapper_directory: Path,
    python_directory: Path,
    force: bool = True,
) -> list[WrittenWrappers]:
    """
    Auto-generate python and fortran code for a package

    This function writes 3 files for each module that is being wrapped:

    - manager: Lifecycle handling for derived types (in Fortran)

    - wrapper: Provides a fortran wrapper to the generated functions that can be
                made available to Python

    - python module: Python interface for creating and manipulating derived types.

    This function may also write other files necessary
    for wrapping the package as a whole.
    This includes generating a `__init__.py` file
    if it doesn't already exist in the python directory.

    Parameters
    ----------
    package
        Package to generate wrappers for

    shared
        Shared elements which should be consistent
        across the package's generated wrappers

    extension
        Package name for the compiled extension module

        Typically, this is of the form ``my_module._lib``

    manager_directory
        Directory in which to write the derived type lifecycle manager(s)

    wrapper_directory
        Directory to write the Python-Fortran wrapper(s).

    python_directory
        Directory in which to write the python module(s).

    force
        If ``True``, overwrite any existing files

    Returns
    -------
        The wrappers that were written

    Raises
    ------
    FileExistsError
        If ``not force`` and a targeted file exists
    """
    write_package_wrapper(
        package=package,
        desc="Python package `__init__.py` file",
        generator_function=generate_python_init_module,
        outdir=python_directory,
        filename="__init__.py",
        keep_existing=True,
    )
    if package.modules_enum_defining:
        write_package_wrapper(
            package=package,
            desc="Python equivalent of enums",
            generator_function=generate_python_enums_module,
            outdir=python_directory,
            filename="enums.py",  # Can make this configurable too if we want
            force=force,
        )

    written_wrappers = []
    for module in package.modules:
        written_wrappers_module = write_module_wrappers(
            package=package,
            shared=shared,
            module=module,
            manager_directory=manager_directory,
            wrapper_directory=wrapper_directory,
            python_directory=python_directory,
            extension=extension,
            force=force,
        )
        written_wrappers.append(written_wrappers_module)

    return written_wrappers


__all__ = [
    "generate_fortran_manager_module",
    "generate_fortran_wrapper_module",
    "generate_python_init_module",
    "generate_python_wrapper_module",
    "process_package",
]
