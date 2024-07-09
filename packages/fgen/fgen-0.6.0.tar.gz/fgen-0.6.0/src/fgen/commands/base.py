"""
Base utilities for the CLI
"""
from __future__ import annotations

import sys
from typing import Any

import click
from loguru import logger

DEFAULT_LOGGING_CONFIG = dict(
    handlers=[
        dict(
            sink=sys.stderr,
            colorize=True,
            format=" - ".join(
                [
                    "<green>{time:!UTC}</>",
                    "<lvl>{level}</>",
                    "<cyan>{name}:{file}:{line}</>",
                    "<lvl>{message}</>",
                ]
            ),
        )
    ],
)
"""Default configuration used with :meth:`loguru.logger.configure`"""


def setup_logging(config: dict[str, Any] | None = None) -> None:
    """
    Early setup for logging.

    Parameters
    ----------
    config
        Passed to :meth:`loguru.logger.configure`. If not passed,
        :const:`DEFAULT_LOGGING_CONFIG` is used.
    """
    if config is None:
        config = DEFAULT_LOGGING_CONFIG

    logger.configure(**config)
    logger.enable("fgen")


@click.group
@click.option(
    "--no-logging-setup",
    is_flag=True,
    help="""Run without setting up any logging.

    You will almost never want this, it is mainly for testing purposes.
    """,
)
def cli(no_logging_setup: bool) -> None:
    """
    Entrypoint for the command-line interface
    """
    if not no_logging_setup:
        # For configurable logging from the CLI,
        # see https://gitlab.com/magicc/fgen/-/issues/81
        setup_logging()
