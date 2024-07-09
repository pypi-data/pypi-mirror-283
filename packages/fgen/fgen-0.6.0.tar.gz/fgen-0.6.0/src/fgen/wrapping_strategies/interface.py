"""
Interface definition for wrapping strategies
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import Optional, Protocol, Union

from fgen.data_models import Method, Module, MultiReturn, Value
from fgen.wrapping_strategies.passing_to_fortran_steps import (
    PassingToFortranSteps,
)
from fgen.wrapping_strategies.receiving_from_python_steps import (
    ReceivingFromPythonSteps,
)


class WrappingStrategyLike(Protocol):
    """
    Wrapping strategy interface
    """

    def get_fortran_wrapper_module_getter(
        self, value: Union[MultiReturn, Value]
    ) -> str:
        """
        Get the name of the getter in the Fortran wrapper module

        Parameters
        ----------
        value
            Value for which to get the getter

        Returns
        -------
            Name of the getter in the Fortran wrapper module
        """
        ...

    def get_fortran_wrapper_module_setter(
        self, value: Union[MultiReturn, Value]
    ) -> str:
        """
        Get the name of the setter in the Fortran wrapper module

        Parameters
        ----------
        value
            Value for which to get the getter

        Returns
        -------
            Name of the getter in the Fortran wrapper module
        """
        ...

    def get_fortran_wrapper_statement_declarations_getters_and_setters(
        self, value: Union[MultiReturn, Value]
    ) -> list[str]:
        """
        Get statement declarations for the getters/setters in the Fortran wrapper module

        Parameters
        ----------
        value
            Value for which to get the statement declarations

        Returns
        -------
            Statement declarations for the getters and setters
            in the Fortran wrapper module.
        """
        ...

    def get_fortran_wrapper_statement_declarations_for_returning_method_result_to_python(  # noqa: E501
        self, method: Method, prefix: str
    ) -> list[str]:
        """
        Get statement declarations for the returning a method's result to Python

        Parameters
        ----------
        method
            Method for which to get the statement declarations.

        prefix
            Prefix to use when naming the method in Fortran.

        Returns
        -------
            Statement declarations for the returning a method's result to Python.
        """
        ...

    def get_receiving_from_python_steps(  # noqa: PLR0913
        self,
        value: Union[MultiReturn, Value],
        dynamic_unit: Optional[str] = None,
        providing_module: Optional[Module] = None,
        requesting_module: Optional[Module] = None,
        get_instance_callable_name: Optional[str] = None,
    ) -> ReceivingFromPythonSteps:
        """
        Get the steps required to receive the value from Python

        Parameters
        ----------
        value
            Value to receive from Python

        dynamic_unit
            The source of the dynamic unit, if this value has one.

        providing_module
            The module that provides ``value``'s type, if it is not intrinsic.

        requesting_module
            The module that is requesting ``value``'s type, if it is not intrinsic.

        get_instance_callable_name
            The name of the callable used to get instances of wrapped derived types
            (typically comes from
            :py:attr:`fgen.wrapper_building.fortran_wrapper_module.FortranWrapperModuleBuilder.shared`).

        Returns
        -------
            Steps required to receive the value from Python
        """
        ...

    def get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(
        self, value: Union[MultiReturn, Value]
    ) -> str:
        """
        Get the type attribute declaration for the value used to pass information to the original Fortran module

        This is not always the same as the type used by the original Fortran module,
        particularly when allocatable types are involved.

        For the definition of a type attribute declaration,
        see :py:mod:`fgen.fortran_parsing`.


        Parameters
        ----------
        value
            Value for which to get the type attribute declaration
            for the value to pass to the original Fortran.

        Returns
        -------
            Type attribute declaration
            for the value to use to pass ``value`` to the original Fortran.
        """  # noqa: E501
        ...

    def get_fortran_for_getter(
        self,
        value: Union[MultiReturn, Value],
        class_being_wrapped: str,
        value_manager_get_free_instance_number: Optional[str] = None,
        value_manager_get_instance: Optional[str] = None,
    ) -> str:
        """
        Get the Fortran for the wrapper module's getter.

        Parameters
        ----------
        value
            Value returned from the getter.

        class_being_wrapped
            Derived type being wrapped.

        value_manager_get_free_instance_number
            Callable which gets a free instance number
            for objects of the type of ``value``.

        value_manager_get_instance
            Callable which gets an instance for objects of the type of ``value``.

        Returns
        -------
            Fortran for the wrapper module's getter.
        """
        ...

    def get_fortran_for_method_returning_wrapped_type(  # noqa: PLR0913
        self,
        fortran_wrapper_module_callable: str,
        receiving_from_python_steps: ReceivingFromPythonSteps,
        return_value: Union[MultiReturn, Value],
        class_being_wrapped: str,
        method_name: str,
        return_value_manager_get_free_instance_number: Optional[str],
        return_value_manager_get_instance: Optional[str],
    ) -> str:
        """
        Get the Fortran for a method which returns the wrapped type

        Parameters
        ----------
        fortran_wrapper_module_callable
            The Fortran wrapper module's callable's name

        receiving_from_python_steps
            Steps to receive the callable's inputs from Python

        return_value
            The (original) Fortran module callable's return value

        class_being_wrapped
            The name of the Fortran derived type being wrapped

        method_name
            The name of the method being wrapped

        return_value_manager_get_free_instance_number
            Callable which gets a free instance number
            for objects of the type of ``return_value``.

        return_value_manager_get_instance
            Callable which gets an instance for objects of the type of ``return_value``.

        Returns
        -------
            Fortran for wrapping the method
        """
        ...

    def get_python_user_facing_name(self, value: Union[MultiReturn, Value]) -> str:
        """
        Get the name that Python users will use for this value

        For example, when naming attributes
        or using this value as an argument in a function/method.

        Parameters
        ----------
        value
            Name that Python users will use for this value

        Returns
        -------
            Name to use for the Python attribute
        """
        ...

    def get_python_post_verify_units_input_type_annotation(
        self, value: Union[MultiReturn, Value]
    ) -> str:
        """
        Get input type annotation, assuming the ``verify_units`` decorator is applied.

        The type annotation is for when ``value``
        is used as an input to a Python callable.

        Parameters
        ----------
        value
            Value for which to get the type annotation

        Returns
        -------
            Type annotation for the value,
            assuming the ``verify_units`` decorator is applied.
        """
        ...

    def get_python_return_type_annotation(
        self, value: Union[MultiReturn, Value]
    ) -> str:
        """
        Get the return type annotation for the Python attribute

        Parameters
        ----------
        value
            Value for which to get the return type annotation for the Python attribute

        Returns
        -------
            Return type annotation for the Python attribute
        """
        ...

    def get_python_argument_declaration_type_annotation(self, value: Value) -> str:
        """
        Get the type annotation to use in Python user-facing declarations

        Parameters
        ----------
        value
            Value for which to get the type annotation

        Returns
        -------
            Type annotation to use in the Python argument declaration
        """
        ...

    def get_python_getter_docstring(self, value: Value) -> str:
        """
        Get docstring for the Python getter for the value

        Parameters
        ----------
        value
            Value for which to get the Python getter docstring

        Returns
        -------
            Python getter docstring
        """
        ...

    def get_python_setter_docstring(self, value: Value) -> str:
        """
        Get docstring for the Python setter for the value

        Parameters
        ----------
        value
            Value for which to get the Python setter docstring

        Returns
        -------
            Python setter docstring
        """
        ...

    def generate_python_for_fortran_return_value_processing(
        self,
        value: Union[MultiReturn, Value],
        fortran_module_callable: str,
        fortran_module_callable_args: Iterable[str],
        dynamic_unit: Optional[str],
    ) -> str:
        """
        Generate the Python code that processes the value returned from Fortran

        Parameters
        ----------
        value
            Value for which to generate the Python code for processing
            the value returned from Fortran

        fortran_module_callable
            The Fortran module callable to call

        fortran_module_callable_args
            The arguments to pass to the Fortran module callable
            (sometimes these need to be supplemented, hence we pass them separately).

        dynamic_unit
            If provided, specifies where to retrieve the dynamic unit of ``value`` from.

        Returns
        -------
            Python code that calls the callable and processes the results
            into the expected Python type.
        """
        ...

    def get_passing_to_fortran_steps(
        self,
        value: Union[MultiReturn, Value],
        dynamic_unit: Optional[str],
    ) -> PassingToFortranSteps:
        """
        Get the steps required to pass this value to the Fortran

        Parameters
        ----------
        value
            Value to pass into Fortran

        dynamic_unit
            If provided, specifies the dynamic units to convert values to.

        Returns
        -------
            Steps required to pass the value into the Fortran
        """
        ...
