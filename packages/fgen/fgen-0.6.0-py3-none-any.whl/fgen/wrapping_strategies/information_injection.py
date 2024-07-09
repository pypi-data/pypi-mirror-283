"""
Information injection functions
"""
from __future__ import annotations

from typing import Union

from fgen.data_models import MultiReturn, Value
from fgen.wrapping_strategies.interface import WrappingStrategyLike


def inject_wrapping_strategy_information(
    rendered_code: str,
    value: Union[MultiReturn, Value],
    wrapping_strategy: WrappingStrategyLike,
    comment_character: str,
    indent: str = "",
) -> str:
    """
    Inject information about the strategy as a comment

    Parameters
    ----------
    rendered_code
        Rendered code, into which to inject the information

    value
        Value being wrapped

    wrapping_strategy
        Wrapping strategy used

    comment_character
        Comment character for this text

    indent
        Indent to use when starting a new line

    Returns
    -------
        Rendered code, with wrapping strategy information injected
    """
    ws_repr_raw = repr(wrapping_strategy)
    toks = ws_repr_raw.split("(")

    wrapping_strategy_name = toks[0]
    wrapping_strategy_attribute_values = toks[1][:-1].split(",")
    comment = f"\n{indent}".join(
        [
            f"{comment_character} Wrapping {value.definition.name}",
            f"{comment_character} Strategy: {wrapping_strategy_name}(",
            *[
                f"{comment_character}     {v.strip()},"
                for v in wrapping_strategy_attribute_values
                if v.strip()
            ],
            f"{comment_character} )",
        ]
    )

    return "\n".join([comment, rendered_code])
