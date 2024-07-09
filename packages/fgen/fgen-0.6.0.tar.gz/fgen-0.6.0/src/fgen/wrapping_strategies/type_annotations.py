"""
Helpers for type annotations
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from fgen.data_models import MultiReturn, Value


PINT_QUANTITY_TYPE_ANNOTATION: str = "pint.registry.UnitRegistry.Quantity"
"""
Type annotation for pint quantities.

Currently these don't support information about the type held by the quantity.
This can be updated in future.
"""


NUMPY_ARRAY_TYPE_ANNOTATION_BASE: str = "npt.NDArray[{kind}]"
"""
Base type annotation for numpy arrays
"""


def get_numpy_array_type_annotation(value: Union[MultiReturn, Value]) -> str:
    """
    Get type annotation for a numpy array
    """
    fdt = value.definition.as_fortran_data_type()
    if fdt.is_array_of_float_double:
        return NUMPY_ARRAY_TYPE_ANNOTATION_BASE.format(kind="np.float64")

    raise NotImplementedError(value)
