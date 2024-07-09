"""
Base class for wrapped derived types
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from functools import wraps
from types import TracebackType
from typing import Any, Callable, Optional, TypeVar

import attrs
from attrs import define, field
from typing_extensions import Concatenate, ParamSpec

from fgen_runtime.exceptions import InitialisationError
from fgen_runtime.formatting import to_html, to_pretty, to_str
from fgen_runtime.units import FuncT

INVALID_INSTANCE_INDEX: int = -1
"""
Value used to denote an invalid ``instance_index``.

This can occur value when a wrapper class
has not yet been initialised (connected to a Fortran instance).
"""


@define
class FinalizableWrapperBase(ABC):
    """
    Base class for model wrappers
    """

    instance_index: int = field(
        validator=attrs.validators.instance_of(int),
        default=INVALID_INSTANCE_INDEX,
    )
    """
    Model index of wrapper Fortran instance
    """

    def __str__(self) -> str:
        """
        Get string representation of self
        """
        return to_str(
            self,
            self.exposed_attributes,
        )

    def _repr_pretty_(self, p: Any, cycle: bool) -> None:
        """
        Get pretty representation of self

        Used by IPython notebooks and other tools
        """
        to_pretty(
            self,
            self.exposed_attributes,
            p=p,
            cycle=cycle,
        )

    def _repr_html_(self) -> str:
        """
        Get html representation of self

        Used by IPython notebooks and other tools
        """
        return to_html(
            self,
            self.exposed_attributes,
        )

    @property
    def initialized(self) -> bool:
        """
        Is the instance initialised, i.e. connected to a Fortran instance?
        """
        return self.instance_index != INVALID_INSTANCE_INDEX

    @property
    @abstractmethod
    def exposed_attributes(self) -> tuple[str, ...]:
        """
        Attributes exposed by this wrapper
        """
        ...

    @classmethod
    @abstractmethod
    def from_new_connection(cls) -> FinalizableWrapperBase:
        """
        Initialise by establishing a new connection with the Fortran module

        This requests a new model index from the Fortran module and then
        initialises a class instance

        Returns
        -------
        New class instance
        """
        ...

    @abstractmethod
    def finalize(self) -> None:
        """
        Finalise the Fortran instance and set self back to being uninitialised

        This method resets ``self.instance_index`` back to
        ``_UNINITIALISED_instance_index``

        Should be decorated with :func:`check_initialised`
        """
        # call to Fortran module goes here when implementing
        self._uninitialise_instance_index()

    def _uninitialise_instance_index(self) -> None:
        self.instance_index = INVALID_INSTANCE_INDEX


@define
class FinalizableWrapperBaseContext(AbstractContextManager):  # type: ignore
    """
    Context manager for a wrapper
    """

    model: FinalizableWrapperBase
    """
    model instance to be managed
    """

    def __enter__(self) -> FinalizableWrapperBase:
        if not self.model.initialized:
            raise InitialisationError(self.model)

        return self.model

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.model.finalize()


P = ParamSpec("P")
T = TypeVar("T")
Wrapper = TypeVar("Wrapper", bound=FinalizableWrapperBase)


def check_initialised(method: FuncT) -> FuncT:
    """
    Check that initialisation is called before execution

    Parameters
    ----------
    method
        Method to wrap

    Returns
    -------
    Wrapped method. Before the method is called, initialisation will first be
    checked. If the model wrapper hasn't been initialised before the method is
    called, an ``InitialisationError`` will be raised.
    """

    @wraps(method)
    def checked(
        ref: Wrapper,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if not ref.initialized:
            raise InitialisationError(ref, method)

        return method(ref, *args, **kwargs)

    return checked  # type: ignore


# Thank you for type hints info
# https://adamj.eu/tech/2021/05/11/python-type-hints-args-and-kwargs/
def execute_finalize_on_fail(
    inst: FinalizableWrapperBase,
    func_to_try: Callable[Concatenate[int, P], T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    """
    Execute a function, finalising the instance before raising if any error occurs

    This function is most useful in factory functions where it provides a
    clean way of ensuring that any Fortran is freed up in the event of an
    initialisation failure for any reason

    Parameters
    ----------
    inst
        Instance whose model index we will use when executing the functin

    func_to_try
        Function to try executing, must take ``inst``'s model index as its
        first argument

    *args
        Passed to ``func_to_try``

    **kwargs
        Passed to ``func_to_try``

    Returns
    -------
    Result of calling ``func_to_try(inst.instance_index, *args, **kwargs)``

    Raises
    ------
    Exception
        Any exception which occurs when calling ``func_to_try. Before the
        exception is raised, ``inst.finalize()`` is called.
    """
    try:
        return func_to_try(inst.instance_index, *args, **kwargs)
    except RuntimeError:
        # finalize the instance before raising
        inst.finalize()

        raise
