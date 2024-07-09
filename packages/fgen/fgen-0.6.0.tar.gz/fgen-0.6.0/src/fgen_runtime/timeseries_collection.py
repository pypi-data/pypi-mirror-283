"""
Timeseries collection handling class
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from attrs import define

if TYPE_CHECKING:
    import pint


class ValuesBoundedLike(Protocol):
    """
    Class that behaves like a bounded values holder
    """

    @property
    def values(self) -> pint.UnitRegistry.Quantity:
        """
        Values
        """
        ...

    @property
    def value_last_bound(self) -> pint.UnitRegistry.Quantity:
        """
        Value at the end of the last bound
        """
        ...


class TimeseriesLike(Protocol):
    """
    Class that behaves like a timeseries
    """

    @property
    def name(self) -> str:
        """
        Name of the timeseries
        """
        ...

    @property
    def values(self) -> ValuesBoundedLike:
        """
        Values of the timeseries
        """
        ...

    @property
    def time(self) -> ValuesBoundedLike:
        """
        Time axis of the timeseries
        """
        ...

    @property
    def spline(self) -> int:
        """
        Spline of the timeseries
        """
        ...


@define
class TimeseriesCollection:
    """
    Container for a number of :obj:`Timeseries`
    """

    ts: list[TimeseriesLike]

    def __getitem__(self, key: int | str) -> TimeseriesLike:
        if isinstance(key, str):
            raise NotImplementedError()

        return self.ts[key]

    def __len__(self) -> int:
        return len(self.ts)
