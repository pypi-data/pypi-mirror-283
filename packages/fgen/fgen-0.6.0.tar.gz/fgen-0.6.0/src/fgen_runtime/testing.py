"""
Testing tools
"""
from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Callable, Protocol

import pint.testing

from fgen_runtime.timeseries_collection import TimeseriesCollection

if TYPE_CHECKING:
    import pint


def assert_timeseries_collection_equal(
    left: TimeseriesCollection, right: TimeseriesCollection
) -> None:
    """
    Assert that two :obj:`TimeseriesCollection` are equal

    Parameters
    ----------
    left
        First object to compare

    right
        Second object to compare

    Raises
    ------
    AssertionError
        The two objects are not equal
    """

    def get_msg(i: int) -> str:
        return f"left_v.data != right_v.data for index={i}"

    assert_timeseries_collection_compare(
        left=left,
        right=right,
        compare_data=pint.testing.assert_equal,  # type: ignore # mypy and pint fighting
        get_data_error_message=get_msg,
    )


def assert_timeseries_collection_allclose(
    left: TimeseriesCollection,
    right: TimeseriesCollection,
    rtol: float = 1e-6,
    atol: float = 1e-8,
) -> None:
    """
    Assert that two :obj:`TimeseriesCollection`'s values are all close

    Parameters
    ----------
    left
        First object to compare

    right
        Second object to compare

    rtol
        Relative tolerance to pass through to :func:`pint.testing.assert_allclose`

    atol
        Absolute tolerance to pass through to :func:`pint.testing.assert_allclose`

    Raises
    ------
    AssertionError
        The two objects are not equal
    """

    def get_msg(i: int) -> str:
        return f"left_v.data not close to right_v.data for index={i}"

    assert_timeseries_collection_compare(
        left=left,
        right=right,
        compare_data=partial(pint.testing.assert_allclose, rtol=rtol, atol=atol),
        get_data_error_message=get_msg,
    )


class CompareDataCallable(Protocol):
    def __call__(
        self,
        left: pint.UnitRegistry.Quantity,
        right: pint.UnitRegistry.Quantity,
        msg: str | None = None,
    ) -> None:
        """
        Compare the data
        """
        ...


def assert_timeseries_collection_compare(
    left: TimeseriesCollection,
    right: TimeseriesCollection,
    compare_data: CompareDataCallable,
    get_data_error_message: Callable[[int], str],
) -> None:
    """
    Assert that two :obj:`TimeseriesCollection`'s values are all close

    Parameters
    ----------
    left
        First object to compare

    right
        Second object to compare

    compare_data
        Function to use to compare the data attributes of left and right

    get_data_error_message
        Function that creates the error message if the data attributes are
        not identical based on the index that is being compared.

    Raises
    ------
    AssertionError
        The two objects are not equal
    """
    # First check that there are the same number of Timeseries in each
    if len(left) != len(right):
        msg = f"{len(left)} != {len(right)}"
        raise AssertionError(msg)

    # Order matters for timeseries collections, so we can check with basic iteration
    for i in range(len(left)):  # I would want to use zip here but mypy was complaining
        left_v = left[i]
        right_v = right[i]
        if left_v.name != right_v.name:
            msg = f"{left_v.name} != {right_v.name} for index={i}"
            raise AssertionError(msg)

        msg = get_data_error_message(i)
        compare_data(
            left_v.values.values,
            right_v.values.values,
            msg=msg,
        )
        compare_data(
            left_v.values.value_last_bound,
            right_v.values.value_last_bound,
            msg=msg,
        )

        try:
            compare_data(left_v.time.values, right_v.time.values)
            compare_data(left_v.time.value_last_bound, right_v.time.value_last_bound)
        except AssertionError as exc:
            msg = f"left_v.time_axis != right_v.time_axis for index={i}"
            raise AssertionError(msg) from exc

        if left_v.spline != right_v.spline:
            msg = f"{left_v.spline} != {right_v.spline} for index={i}"
            raise AssertionError(msg)
