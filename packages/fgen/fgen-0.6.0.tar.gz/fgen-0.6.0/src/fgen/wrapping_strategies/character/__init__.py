"""
Wrapping strategy for characters (strings in Python world)

Doesn't cover characters with a deferred length.
For that, see
:mod:`~fgen.wrapping_strategies.character_deferred_size`.
"""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Union

from attrs import define

from fgen.data_models import Method, Module, MultiReturn, Value
from fgen.jinja_environment import (
    JINJA_ENV,
    get_template_in_directory,
)
from fgen.wrapping_strategies.information_injection import (
    inject_wrapping_strategy_information,
)
from fgen.wrapping_strategies.passing_to_fortran_steps import (
    PassingToFortranSteps,
)
from fgen.wrapping_strategies.receiving_from_python_steps import (
    ReceivingFromPythonSteps,
)


@define
class WrappingStrategyCharacter:
    """
    Wrapping strategy for characters (strings in Python world)

    Doesn't cover characters with a deferred length.
    For that, see
    :class:`~fgen.wrapping_strategies.character_deferred_size.WrappingStrategyCharacterDeferredSize`.
    """

    def get_fortran_wrapper_module_getter(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        return f"iget_{value.definition.name}"

    def get_fortran_wrapper_module_setter(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        return f"iset_{value.definition.name}"

    def get_fortran_wrapper_statement_declarations_getters_and_setters(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> list[str]:
        return [
            f"public :: {method_name}"
            for method_name in (
                self.get_fortran_wrapper_module_getter(value),
                self.get_fortran_wrapper_module_setter(value),
            )
        ]

    def get_fortran_wrapper_statement_declarations_for_returning_method_result_to_python(  # noqa: E501, D102
        self, method: Method, prefix: str
    ) -> list[str]:
        return [f"public :: {prefix}{method.name}"]

    def get_receiving_from_python_steps(  # noqa: D102, PLR0913
        self,
        value: Union[MultiReturn, Value],
        dynamic_unit: Optional[str] = None,
        providing_module: Optional[Module] = None,
        requesting_module: Optional[Module] = None,
        get_instance_callable_name: Optional[str] = None,
    ) -> ReceivingFromPythonSteps:
        return ReceivingFromPythonSteps(
            postprocessing_fortran_calls=None,
            fortran_wrapper_callable_parameters=(
                (
                    value.definition.name,
                    value.definition.as_fortran_data_type().fortran_type_attribute_declaration,
                    value,
                ),
            ),
            fortran_module_callable_args=(value,),
        )

    def get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        return (
            value.definition.as_fortran_data_type().fortran_type_attribute_declaration
        )

    def get_fortran_for_getter(  # noqa: D102
        self,
        value: Union[MultiReturn, Value],
        class_being_wrapped: str,
        value_manager_get_free_instance_number: Optional[str] = None,
        value_manager_get_instance: Optional[str] = None,
    ) -> str:
        template = get_template_in_directory(
            "fortran-for-getter.f90.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        result = template.render(
            return_value=value,
            fortran_wrapper_module_callable=self.get_fortran_wrapper_module_getter(
                value
            ),
            class_being_wrapped=class_being_wrapped,
            fortran_module_attribute=value.definition.name,
        )

        return inject_wrapping_strategy_information(
            result, value=value, wrapping_strategy=self, comment_character="!"
        )

    def get_fortran_for_method_returning_wrapped_type(  # noqa: D102, PLR0913
        self,
        fortran_wrapper_module_callable: str,
        receiving_from_python_steps: ReceivingFromPythonSteps,
        return_value: Union[MultiReturn, Value],
        class_being_wrapped: str,
        method_name: str,
        return_value_manager_get_free_instance_number: Optional[str],
        return_value_manager_get_instance: Optional[str],
    ) -> str:
        template = get_template_in_directory(
            "fortran-for-method-returning-wrapped-type.f90.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        input_params = (
            receiving_from_python_steps.fortran_wrapper_callable_parameter_names
        )

        result = template.render(
            fortran_wrapper_module_callable=fortran_wrapper_module_callable,
            return_value=return_value,
            input_params=input_params,
            receiving_from_python_steps=receiving_from_python_steps,
            class_being_wrapped=class_being_wrapped,
            method_name=method_name,
        )

        return inject_wrapping_strategy_information(
            result, value=return_value, wrapping_strategy=self, comment_character="!"
        )

    def get_python_user_facing_name(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        return value.definition.name

    def get_python_post_verify_units_input_type_annotation(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        return value.definition.as_fortran_data_type().python_equivalent_type_annotation

    def get_python_return_type_annotation(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        return value.definition.as_fortran_data_type().python_equivalent_type_annotation

    def get_python_argument_declaration_type_annotation(  # noqa: D102
        self, value: Value
    ) -> str:
        return value.definition.as_fortran_data_type().python_equivalent_type_annotation

    def get_python_getter_docstring(self, value: Value) -> str:  # noqa: D102
        template = get_template_in_directory(
            "python-getter-docstring.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(attribute=value)

        return result

    def get_python_setter_docstring(self, value: Value) -> str:  # noqa: D102
        return f"Setter for ``{value.definition.name}``"

    def generate_python_for_fortran_return_value_processing(  # noqa: D102
        self,
        value: Union[MultiReturn, Value],
        fortran_module_callable: str,
        fortran_module_callable_args: Iterable[str],
        dynamic_unit: Optional[str],
    ) -> str:
        return_type = self.get_python_return_type_annotation(value)

        template = get_template_in_directory(
            "python-for-fortran-return-value-processing.py.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        result = template.render(
            result_name=self.get_python_user_facing_name(value),
            fortran_module_callable=fortran_module_callable,
            fortran_module_callable_args=fortran_module_callable_args,
            return_type=return_type,
        )

        return inject_wrapping_strategy_information(
            result, value=value, wrapping_strategy=self, comment_character="#"
        )

    def get_passing_to_fortran_steps(  # noqa: D102
        self,
        value: Union[MultiReturn, Value],
        dynamic_unit: Optional[str],
    ) -> PassingToFortranSteps:
        return PassingToFortranSteps(
            preparatory_python_calls=None,
            fortran_module_callable_args=(
                (value.definition.name, self.get_python_user_facing_name(value)),
            ),
        )
