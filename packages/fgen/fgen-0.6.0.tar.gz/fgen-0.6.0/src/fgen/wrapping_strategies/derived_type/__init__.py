"""
Wrapping strategy for derived types

These are tricky because f2py doesn't support derived types.
As a result, we pass pointers to the derived type instances
across the Python-Fortran boundary.
This requires careful, custom handling on both sides.
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
class WrappingStrategyDerivedType:
    """
    Wrapping strategy for derived types
    """

    no_setters_class_suffix: str = "NoSetters"
    """Suffix to add to the standard class when returning the no setters version"""

    instance_index_suffix: str = "_instance_index"
    """
    Suffix to add to a variable name when using its instance index

    Often, this is needed to distinguish from using the variable itself.
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
        if providing_module is None:
            msg = "providing_module must be provided"
            raise ValueError(msg)

        if get_instance_callable_name is None:
            msg = "get_instance_callable_name must be provided"
            raise ValueError(msg)

        if requesting_module is None:
            msg = "requesting_module must be provided"
            raise ValueError(msg)

        variable_instance_index = f"{value.definition.name}{self.instance_index_suffix}"

        template = get_template_in_directory(
            "fortran-for-receiving-from-python.f90.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        if requesting_module == providing_module:
            # TODO: remove hard-coding here and use shared instead.
            # Will require some thinking.
            variable_type_manager_get_instance = "manager_get_instance"

        else:
            variable_type_manager_get_instance = "_".join(
                [providing_module.manager_module_name, get_instance_callable_name]
            )

        postprocessing_fortran_calls = template.render(
            variable_instance_index=variable_instance_index,
            variable=value.definition.name,
            variable_type_manager_get_instance=variable_type_manager_get_instance,
        )

        return ReceivingFromPythonSteps(
            postprocessing_fortran_calls=inject_wrapping_strategy_information(
                postprocessing_fortran_calls,
                value=value,
                wrapping_strategy=self,
                comment_character="!",
            ),
            fortran_wrapper_callable_parameters=(
                (variable_instance_index, "integer", value),
            ),
            fortran_module_callable_args=(value,),
        )

    # TODO: re-name to get_fortran_wrapper_module_type_attribute_declaration
    #       because this is the type to use in wrapper module land,
    #       which doesn't always match the type in the original module.
    def get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        # Intermediate is always a pointer because that's what the managers expect.
        # The allocation in the original Fortran handles any copying of data needed.
        type_spec = value.definition.as_fortran_data_type().type_specification
        return f"{type_spec}, pointer"

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
            wrapper_module_type_attribute_declaration=self.get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(
                value
            ),
            fortran_wrapper_module_callable=self.get_fortran_wrapper_module_getter(
                value
            ),
            class_being_wrapped=class_being_wrapped,
            manager_get_free_instance_number=value_manager_get_free_instance_number,
            manager_get_instance=value_manager_get_instance,
            fortran_module_attribute=value.definition.name,
            instance_index_suffix=self.instance_index_suffix,
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
            wrapper_module_type_attribute_declaration=self.get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(
                return_value
            ),
            instance_index_suffix=self.instance_index_suffix,
            input_params=input_params,
            receiving_from_python_steps=receiving_from_python_steps,
            class_being_wrapped=class_being_wrapped,
            return_value_manager_get_free_instance_number=return_value_manager_get_free_instance_number,
            return_value_manager_get_instance=return_value_manager_get_instance,
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
        fdt = value.definition.as_fortran_data_type()
        python_equivalent_type_annotation = fdt.python_equivalent_type_annotation
        if fdt.is_pointer:
            return python_equivalent_type_annotation

        return "\n".join(
            [
                "Union[",
                f"    {python_equivalent_type_annotation}, ",
                f"    {python_equivalent_type_annotation}{self.no_setters_class_suffix},",  # noqa: E501
                "]",
            ]
        )

    def get_python_return_type_annotation(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        fdt = value.definition.as_fortran_data_type()
        base_type = fdt.python_equivalent_type_annotation

        if fdt.is_pointer:
            return base_type

        return f"{base_type}{self.no_setters_class_suffix}"

    def get_python_argument_declaration_type_annotation(  # noqa: D102
        self, value: Value
    ) -> str:
        return value.definition.as_fortran_data_type().python_equivalent_type_annotation

    def get_python_getter_docstring(self, value: Value) -> str:  # noqa: D102
        template = get_template_in_directory(
            "python-getter-docstring.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(
            attribute=value,
            is_pointer=value.definition.as_fortran_data_type().is_pointer,
        )

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
        argument_instance_index = f"{value.definition.name}{self.instance_index_suffix}"

        template = get_template_in_directory(
            "python-for-preparing-to-pass-to-fortran.py.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )
        preparatory_python_calls = template.render(
            argument_user_facing=self.get_python_user_facing_name(value),
            argument_instance_index=argument_instance_index,
        )

        return PassingToFortranSteps(
            preparatory_python_calls=inject_wrapping_strategy_information(
                preparatory_python_calls,
                value=value,
                wrapping_strategy=self,
                comment_character="#",
            ),
            fortran_module_callable_args=(
                (argument_instance_index, argument_instance_index),
            ),
        )
