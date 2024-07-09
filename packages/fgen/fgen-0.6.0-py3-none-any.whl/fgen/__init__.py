"""
An opinionated framework for wrapping Fortran-based code with Python.
"""
import importlib.metadata

from loguru import logger

logger.disable(__name__)

__version__ = importlib.metadata.version("fgen")


def _verify_dependency_importable(dependency: str) -> None:
    """
    Check if a package is importable

    Guards against use of :mod:`fgen`
    without first installing the template dependencies.
    This is a temporary workaround until fgen and fgen_runtime are split.
    """
    try:
        importlib.import_module(dependency)
    except ModuleNotFoundError as e:  # pragma: no cover
        raise ImportError(  # noqa: TRY003
            f"{dependency} is required. Run 'pip install fgen[templates]'"
        ) from e


_verify_dependency_importable("jinja2")
_verify_dependency_importable("black")
