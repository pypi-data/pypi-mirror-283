"""
Wrapping strategies

Different Fortran types need different strategies for wrapping.
We capture these here.
"""
from __future__ import annotations

from fgen.fortran_parsing import FortranDataType
from fgen.wrapping_strategies.array_deferred_size import (
    WrappingStrategyArrayDeferredSize,
)
from fgen.wrapping_strategies.array_derived_type import (
    WrappingStrategyArrayDerivedType,
)
from fgen.wrapping_strategies.array_derived_type_deferred_size import (
    WrappingStrategyArrayDerivedTypeDeferredSize,
)
from fgen.wrapping_strategies.character import (
    WrappingStrategyCharacter,
)
from fgen.wrapping_strategies.character_deferred_size import (
    WrappingStrategyCharacterDeferredSize,
)
from fgen.wrapping_strategies.default import WrappingStrategyDefault
from fgen.wrapping_strategies.derived_type import (
    WrappingStrategyDerivedType,
)
from fgen.wrapping_strategies.enum import WrappingStrategyEnum
from fgen.wrapping_strategies.interface import WrappingStrategyLike
from fgen.wrapping_strategies.logical import (
    WrappingStrategyLogical,
)
from fgen.wrapping_strategies.passing_to_fortran_steps import (
    PassingToFortranSteps,
)


def get_wrapping_strategy(
    fortran_data_type: FortranDataType,
) -> WrappingStrategyLike:
    """
    Get wrapping strategy for a given :obj:`FortranDataType`

    Parameters
    ----------
    fortran_data_type
        :obj:`FortranDataType` for which to get the wrapping strategy

    Returns
    -------
        Wrapping strategy object
    """
    if fortran_data_type.is_array:
        return get_array_wrapping_strategy(fortran_data_type)

    if fortran_data_type.is_character:
        return get_character_wrapping_strategy(fortran_data_type)

    if fortran_data_type.is_derived_type:
        return WrappingStrategyDerivedType()

    if fortran_data_type.is_enum:
        return WrappingStrategyEnum()

    if fortran_data_type.is_logical:
        return WrappingStrategyLogical()

    return WrappingStrategyDefault()


def get_character_wrapping_strategy(fdt: FortranDataType) -> WrappingStrategyLike:
    """
    Get wrapping strategy, given we know the Fortran data type is a character

    Parameters
    ----------
    fdt
        Fortran data type

    Returns
    -------
        Wrapping strategy
    """
    if fdt.has_deferred_size:
        return WrappingStrategyCharacterDeferredSize()

    return WrappingStrategyCharacter()


def get_array_wrapping_strategy(fdt: FortranDataType) -> WrappingStrategyLike:
    """
    Get wrapping strategy, given we know the data type is an array

    Parameters
    ----------
    fdt
        Fortran data type

    Returns
    -------
        Wrapping strategy
    """
    if fdt.is_array_of_derived_type:
        if fdt.has_deferred_size:
            res: WrappingStrategyLike = WrappingStrategyArrayDerivedTypeDeferredSize()
        else:
            res = WrappingStrategyArrayDerivedType()

    elif fdt.has_deferred_size:
        res = WrappingStrategyArrayDeferredSize()

    else:
        res = WrappingStrategyDefault()

    return res


__all__ = [
    "PassingToFortranSteps",
    "WrappingStrategyArrayDeferredSize",
    "WrappingStrategyCharacter",
    "WrappingStrategyCharacterDeferredSize",
    "WrappingStrategyDefault",
    "WrappingStrategyDerivedType",
    "WrappingStrategyLike",
    "WrappingStrategyLogical",
    "get_wrapping_strategy",
]
