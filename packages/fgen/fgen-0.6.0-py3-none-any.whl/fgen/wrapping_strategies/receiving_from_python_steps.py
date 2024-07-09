"""
Data model for how we receive data from Python in Fortran
"""
from __future__ import annotations

from typing import Optional, Union

from attrs import define, field

from fgen.data_models import MultiReturn, Value


@define
class ReceivingFromPythonSteps:
    """
    Container for holding the steps required to receive data from Python
    """

    postprocessing_fortran_calls: Optional[str]
    """Calls required to process the data received from Python"""

    fortran_wrapper_callable_parameters: tuple[
        tuple[str, str, Union[MultiReturn, Value]], ...
    ]
    """
    Parameters of the Fortran wrapper callable

    The first element of each tuple is the parameter name
    as it appears in the declaration of the Fortran wrapper callable.
    The second element of each tuple is the type used
    when passing this variable to Fortran
    (which may differ from the variable type in Fortran).
    The third element of each tuple is the data model of the parameter,
    which makes it available for docstrings etc.
    """

    fortran_module_callable_args: tuple[Union[MultiReturn, Value], ...]
    """
    Arguments to pass to the (original) Fortran module callable

    These just take the data model of the (original) Fortran module callable's argument.
    Hence these must match what is expected by the Fortran module exactly,
    there can be no different naming, types etc.
    (different types wouldn't compile anyway,
    avoiding different names is done for clarity and simplicity).
    """

    fortran_helper_variables: tuple[tuple[str, str], ...] = field(factory=tuple)
    """
    Helper variables required to pass the value from Python to Fortran

    The first element of each tuple is the helper variable's name,
    the second element is its type declaration.
    """

    @property
    def fortran_wrapper_callable_parameter_names(self) -> list[str]:
        """
        Names of the Fortran wrapper callable's parameters

        Note that this may not be the entire parameter list,
        it is only the calls for the parameters managed by ``self``.
        """
        return [v[0] for v in self.fortran_wrapper_callable_parameters]

    @property
    def fortran_module_callable_args_names(self) -> list[str]:
        """
        Argument list to use when calling a callable in the (original) Fortran module

        Note that this may not be the entire argument list,
        it is only the calls for the arguments managed by ``self``.
        """
        return [v.definition.name for v in self.fortran_module_callable_args]

    @property
    def not_directly_passed_fortran_module_callable_args_type_declarations(
        self,
    ) -> list[tuple[str, str]]:
        """
        Type declarations for the argument list that aren't directly passed from Python.

        These type declarations are only required
        because these arguments for the (original) Fortran callable
        cannot be directly passed from Python,
        i.e. these arguments are not parameters of the wrapper module's callable
        (i.e. would otherwise be undefined).

        The first element of each returned tuple is the argument's name,
        the second is the type declaration.

        The argument list is the argument list that is used
        when calling a callable in the (original) Fortran module.

        Note that this may not be the entire argument list,
        it is only the calls for the arguments managed by ``self``.
        """
        out = [
            (
                v.definition.name,
                get_type_declaration_for_passing_value_to_fortran_callable(v),
            )
            for v in self.not_directly_passed_fortran_module_callable_args
        ]

        return out

    @property
    def not_directly_passed_fortran_module_callable_args(
        self,
    ) -> list[Union[MultiReturn, Value]]:
        """
        Fortran module callable arguments that aren't directly passed from Python

        These arguments will have intermediate steps,
        hence the arguments need to be declared as variables separately
        from the callable parameter declarations.

        Note that this is only for the arguments managed by ``self``,
        not necessarily all arguments of the callable.
        """
        out = [
            v
            for v in self.fortran_module_callable_args
            if v.definition.name not in self.fortran_wrapper_callable_parameter_names
        ]

        return out


def get_type_declaration_for_passing_value_to_fortran_callable(
    value: Union[MultiReturn, Value],
) -> str:
    """
    Get the type declaration for ``value`` when passing to the (original) Fortran.

    This is the type expected by the (original) Fortran
    when receiving ``value`` as an argument to callables.

    Parameters
    ----------
    value
        Value for which to get the type declaration

    Returns
    -------
        The type declaration for ``value``
    """
    # Lazy import to avoid circular dependency
    from fgen.wrapping_strategies import get_wrapping_strategy

    wrapping_strategy = get_wrapping_strategy(value.definition.as_fortran_data_type())

    return wrapping_strategy.get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(  # noqa: E501
        value
    )
