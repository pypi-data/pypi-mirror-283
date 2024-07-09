"""
Functions to use to format generated code
"""
from __future__ import annotations

import black


def format_python_code(code: str) -> str:
    """
    Format Python code

    Parameters
    ----------
    code
        Code to format

    Returns
    -------
        Formatted Python code
    """
    # Format result with black
    # This doesn't automatically read `pyproject.toml` so settings must be prescribed
    # TODO: update to formatting with ruff to avoid formatters fighting each other
    return black.format_str(code, mode=black.Mode(line_length=88))
