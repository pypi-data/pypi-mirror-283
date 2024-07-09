"""
Unit-handling
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Callable, TypeVar, Union, overload

import numpy as np
import numpy.typing as npt
import pint
from typing_extensions import ParamSpec, TypeAlias

UnitDefinition: TypeAlias = Union[str, pint.registry.Unit]
"""Types which can be used to specify the exepcted (input) unit"""

ReturnUnitDefinition: TypeAlias = Union[
    str, tuple[str, ...], pint.registry.Unit, tuple[pint.registry.Unit, ...]
]
"""Types which can be used to specify the exepcted return unit"""

VerifyUnitsSupported: TypeAlias = Union[UnitDefinition, None]
"""Types which are supported as inputs to :func:`verify_units`"""

Q: TypeAlias = pint.registry.UnitRegistry.Quantity
"""Short-hand to save space and typing"""

PintSupported: TypeAlias = Union[
    float, int, np.number[Any], npt.NDArray[np.number[Any]], npt.ArrayLike
]
"""
Types that are able to be cast to :obj:`pint.registry.UnitRegistry.Quantity` by pint
"""

P = ParamSpec("P")
FuncT = TypeVar("FuncT", bound=Callable[..., Any])


# Overload variants created with scripts/make-verify-units-overloads.py
# Best not to do this by hand unless you want cramp

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")
UT = TypeVar("UT")
VT = TypeVar("VT")
XT = TypeVar("XT")
YT = TypeVar("YT")
PintT = TypeVar("PintT", bound=PintSupported)
PintU = TypeVar("PintU", bound=PintSupported)
PintV = TypeVar("PintV", bound=PintSupported)
PintX = TypeVar("PintX", bound=PintSupported)
PintY = TypeVar("PintY", bound=PintSupported)
PintZ = TypeVar("PintZ", bound=PintSupported)
PintUT = TypeVar("PintUT", bound=PintSupported)
PintVT = TypeVar("PintVT", bound=PintSupported)
PintXT = TypeVar("PintXT", bound=PintSupported)
PintYT = TypeVar("PintYT", bound=PintSupported)


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[()],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[P, PintT]], Callable[P, Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU], PintT]], Callable[[Q], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[P, PintT]], Callable[P, Q]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU], T]], Callable[[Q], T]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, PintV], PintT]], Callable[[Q, Q], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, U], PintT]], Callable[[Q, U], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU], PintT]], Callable[[U, Q], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[P, PintT]], Callable[P, Q]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, PintV], T]], Callable[[Q, Q], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, U], T]], Callable[[Q, U], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[None, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU], T]], Callable[[U, Q], T]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, PintV, PintX], PintT]], Callable[[Q, Q, Q], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition, UnitDefinition, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, PintV, U], PintT]], Callable[[Q, Q, U], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition, None, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, U, PintV], PintT]], Callable[[Q, U, Q], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition, None, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, U, V], PintT]], Callable[[Q, U, V], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, PintV], PintT]], Callable[[U, Q, Q], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, UnitDefinition, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, V], PintT]], Callable[[U, Q, V], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, None, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, V, PintU], PintT]], Callable[[U, V, Q], Q]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, None, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[P, PintT]], Callable[P, Q]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, PintV, PintX], T]], Callable[[Q, Q, Q], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition, UnitDefinition, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, PintV, U], T]], Callable[[Q, Q, U], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition, None, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, U, PintV], T]], Callable[[Q, U, Q], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition, None, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, U, V], T]], Callable[[Q, U, V], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[None, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, PintV], T]], Callable[[U, Q, Q], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[None, UnitDefinition, None],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, V], T]], Callable[[U, Q, V], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[None, None, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, V, PintU], T]], Callable[[U, V, Q], T]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[PintU, PintV, PintX, PintY], PintT]], Callable[[Q, Q, Q, Q], Q]
]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, PintV, PintX], PintT]], Callable[[U, Q, Q, Q], Q]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[PintU, PintV, PintX, PintY], T]], Callable[[Q, Q, Q, Q], T]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[None, UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, PintV, PintX], T]], Callable[[U, Q, Q, Q], T]]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[
        UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[PintU, PintV, PintX, PintY, PintZ], PintT]], Callable[[Q, Q, Q, Q, Q], Q]
]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[None, UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, PintY], PintT]], Callable[[U, Q, Q, Q, Q], Q]
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[PintU, PintV, PintX, PintY, PintZ], T]], Callable[[Q, Q, Q, Q, Q], T]
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[None, UnitDefinition, UnitDefinition, UnitDefinition, UnitDefinition],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, PintY], T]], Callable[[U, Q, Q, Q, Q], T]
]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[PintU, PintV, PintX, PintY, PintZ, PintUT], PintT]],
    Callable[[Q, Q, Q, Q, Q, Q], Q],
]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, PintY, PintZ], PintT]],
    Callable[[U, Q, Q, Q, Q, Q], Q],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[PintU, PintV, PintX, PintY, PintZ, PintUT], T]],
    Callable[[Q, Q, Q, Q, Q, Q], T],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, PintY, PintZ], T]],
    Callable[[U, Q, Q, Q, Q, Q], T],
]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[PintU, PintV, PintX, PintY, PintZ, PintUT, PintVT], PintT]],
    Callable[[Q, Q, Q, Q, Q, Q, Q], Q],
]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, PintY, PintZ, PintUT], PintT]],
    Callable[[U, Q, Q, Q, Q, Q, Q], Q],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[PintU, PintV, PintX, PintY, PintZ, PintUT, PintVT], T]],
    Callable[[Q, Q, Q, Q, Q, Q, Q], T],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, PintY, PintZ, PintUT], T]],
    Callable[[U, Q, Q, Q, Q, Q, Q], T],
]:
    ...


# Below here are overloads written by hand
# Our lack of all combos means we have to write some by hand.
# This could become extremely painful, or this file may become ludicrously long.
@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        None,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, PintV, V], X]], Callable[[U, Q, Q, V], X]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        None,
        None,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, PintU, PintV, V, X], Y]], Callable[[U, Q, Q, V, X], Y]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        None,
        UnitDefinition,
        UnitDefinition,
        None,
        None,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, V, PintY, PintZ, X, Y], Z]],
    Callable[[U, Q, Q, Q, V, Q, Q, X, Y], Z],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        None,
        UnitDefinition,
        UnitDefinition,
        None,
        None,
        None,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, PintU, PintV, PintX, V, PintY, PintZ, X, Y, Z], UT]],
    Callable[[U, Q, Q, Q, V, Q, Q, X, Y, Z], UT],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        None,
        None,
        None,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, V, X, Y, PintU], Z]],
    Callable[[U, V, X, Y, Q], Z],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, V, PintU, PintV, PintX, PintZ], Z]],
    Callable[[U, V, Q, Q, Q, Q], Z],
]:
    ...


@overload
def verify_units(
    ret: ReturnUnitDefinition,
    args: tuple[
        None,
        None,
        None,
        None,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, V, X, Y], PintT]],
    Callable[[U, V, X, Y], Q],
]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        None,
        UnitDefinition,
        UnitDefinition,
        UnitDefinition,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[[U, V, PintU, PintV, PintX], Y]], Callable[[U, V, Q, Q, Q], Y]]:
    ...


@overload
def verify_units(
    ret: None,
    args: tuple[
        None,
        None,
        None,
        None,
        None,
        None,
        UnitDefinition,
        None,
        None,
    ],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[
    [Callable[[U, V, X, Y, Z, UT, PintU, VT, XT], YT]],
    Callable[[U, V, X, Y, Z, UT, Q, VT, XT], YT],
]:
    ...


# The do nothing case. Here the decorator does not alter the signature of the
# input function.
@overload
def verify_units(
    ret: None,
    args: tuple[None, ...],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[FuncT], FuncT]:
    ...


def verify_units(
    ret: VerifyUnitsSupported | Iterable[VerifyUnitsSupported],
    args: Iterable[VerifyUnitsSupported],
    strict: bool = True,
    ureg: pint.registry.UnitRegistry | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Wrap a function to make it pint-aware

    This wraps :func:`unit_registry.wraps`, but provides better handling for types

    Parameters
    ----------
    ret
        Units of each of the return values. Use `None` to skip argument conversion.

    args
        Units of each of the arguments. Use `None` to skip argument conversion.

    strict
        Indicates that only quantities are accepted. (Default value = True)

    ureg
        Unit registry to use

        Defaults to :attr:`unit_registry` in the `fgen.units` module.

    Returns
    -------
        Decorator for wrapping callables
    """
    # Work around quirk where wraps doesn't accept dimensionless
    clean_args = [arg if arg != "dimensionless" else "" for arg in args]

    if ureg is None:
        ureg: pint.registry.UnitRegistry = pint.get_application_registry()  # type: ignore

    return ureg.wraps(ret, clean_args, strict)  # type: ignore
