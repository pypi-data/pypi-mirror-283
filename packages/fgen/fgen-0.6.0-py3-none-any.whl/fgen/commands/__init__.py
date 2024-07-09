"""
Command-line interface definitions
"""
from fgen.commands.base import cli
from fgen.commands.generate import generate_command  # noqa: F401

__all__ = ["cli"]
