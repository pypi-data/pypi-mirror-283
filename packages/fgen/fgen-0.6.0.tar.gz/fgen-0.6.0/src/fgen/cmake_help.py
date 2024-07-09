"""
Help with `CMakeLists.txt` files
"""
from __future__ import annotations

from collections.abc import Iterable
from functools import partial
from pathlib import Path

from loguru import logger

from fgen.wrapper_building import WrittenWrappers


def get_cmake_lists_help_string(written_paths: list[Path], cmake_prefix: str) -> str:
    """
    Get help string for files to include in a `CMakeLists.txt` file

    Parameters
    ----------
    written_paths
        Input paths to include in the help message

    cmake_prefix
        Prefix to apply to the paths in the help string.

        This can make it easier if you want to copy and paste
        these messages later.

    Returns
    -------
        Help string that includes the sorted paths with the prefix
        and some instructions.
    """
    filenames = sorted([v.name for v in written_paths])
    info_str = "\n".join([f'"{Path(cmake_prefix) / v}"' for v in filenames])

    return f"In your `CMakeLists.txt` you will probably need paths like:\n{info_str}"


def log_cmake_lists_help(
    written_wrappers: Iterable[WrittenWrappers], cmake_prefix: str
) -> None:
    """
    Log help for the lines that will probably be needed in a `CMakeLists.txt` file

    Parameters
    ----------
    written_wrappers
        The wrappers that were written by {py:mod}`fgen`

    cmake_prefix
        Prefix to apply to the paths in the help string.

        This can make it easier if you want to copy and paste
        these messages later.
    """
    gcmls = partial(get_cmake_lists_help_string, cmake_prefix=cmake_prefix)

    logger.info(gcmls([v.manager_file for v in written_wrappers]))
    logger.info(gcmls([v.wrapper_file for v in written_wrappers]))
