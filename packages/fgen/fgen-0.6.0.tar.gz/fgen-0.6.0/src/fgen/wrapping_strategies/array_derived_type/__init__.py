"""
Wrapping strategy for arrays of derived types

These are tricky because f2py doesn't support derived types.
As a result, we pass arrays of integers, which act as pointers,
to the derived type instances across the Python-Fortran boundary.
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
class WrappingStrategyArrayDerivedType:
    """
    Wrapping strategy for arrays of derived types
    """

    no_setters_class_suffix: str = "NoSetters"
    """Suffix to add to the standard class when returning the no setters version"""

    instance_indexes_suffix: str = "_instance_indexes"
    """
    Suffix to use for variables that represent the instance indexes of the derived types
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
            msg = "Providing module must be provided"
            raise ValueError(msg)

        if get_instance_callable_name is None:
            msg = "get_instance_callable_name must be provided"
            raise ValueError(msg)

        variable_instance_indexes = (
            f"{value.definition.name}{self.instance_indexes_suffix}"
        )
        fdt = value.definition.as_fortran_data_type()
        variable_instance_indexes_type = (
            f"integer, {fdt.dimension_attribute_specification!s}"
        )
        loop_helper_variable = f"i_{variable_instance_indexes}"
        variable_intermediate = f"{value.definition.name}_tmp"
        # Always receive pointers from the managers
        variable_intermediate_type = (
            f"{value.definition.as_fortran_data_type().type_specification}, pointer"
        )

        template = get_template_in_directory(
            "fortran-for-receiving-from-python.f90.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        postprocessing_fortran_calls = template.render(
            variable_instance_indexes=variable_instance_indexes,
            variable=value.definition.name,
            variable_type_manager_get_instance="_".join(
                [providing_module.manager_module_name, get_instance_callable_name]
            ),
            variable_intermediate=variable_intermediate,
            loop_helper_variable=loop_helper_variable,
        )

        return ReceivingFromPythonSteps(
            postprocessing_fortran_calls=inject_wrapping_strategy_information(
                postprocessing_fortran_calls,
                value=value,
                wrapping_strategy=self,
                comment_character="!",
            ),
            fortran_wrapper_callable_parameters=(
                (
                    variable_instance_indexes,
                    variable_instance_indexes_type,
                    value,
                ),
            ),
            fortran_module_callable_args=(value,),
            fortran_helper_variables=(
                (loop_helper_variable, "integer"),
                (variable_intermediate, variable_intermediate_type),
            ),
        )

    # TODO: re-name to get_fortran_wrapper_module_type_attribute_declaration
    #       because this is the type to use in wrapper module land,
    #       which doesn't always match the type in the original module.
    def get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(  # noqa: D102
        self, value: Union[MultiReturn, Value]
    ) -> str:
        type_specification = value.definition.as_fortran_data_type().type_specification
        variable_instance_indexes = (
            f"{value.definition.name}{self.instance_indexes_suffix}"
        )

        # Intermediate is an array of the derived type, with a size that matches
        # the received value.
        return f"{type_specification}, dimension(size({variable_instance_indexes}))"

    def get_fortran_for_getter(  # noqa: D102
        self,
        value: Union[MultiReturn, Value],
        class_being_wrapped: str,
        value_manager_get_free_instance_number: Optional[str] = None,
        value_manager_get_instance: Optional[str] = None,
    ) -> str:
        derived_type_in_array = value.definition.as_fortran_data_type().base_python_type
        return_value_dimension_specification = str(
            value.definition.as_fortran_data_type().dimension_attribute_specification
        )

        template = get_template_in_directory(
            "fortran-for-getter.f90.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        result = template.render(
            return_value=value,
            return_value_dimension_specification=return_value_dimension_specification,
            wrapper_module_type_attribute_declaration=self.get_type_attribute_declaration_for_value_to_pass_to_original_fortran_module(
                value
            ),
            fortran_wrapper_module_callable=self.get_fortran_wrapper_module_getter(
                value
            ),
            class_being_wrapped=class_being_wrapped,
            derived_type_in_array=derived_type_in_array,
            manager_get_free_instance_number=value_manager_get_free_instance_number,
            manager_get_instance=value_manager_get_instance,
            fortran_module_attribute=value.definition.name,
            instance_indexes_suffix=self.instance_indexes_suffix,
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
        derived_type_in_array = (
            return_value.definition.as_fortran_data_type().base_python_type
        )

        template = get_template_in_directory(
            "fortran-for-method-returning-wrapped-type.f90.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        # TODO: think about better way to do this
        return_value_dimension_specification = str(
            return_value.definition.as_fortran_data_type().dimension_attribute_specification
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
            instance_index_suffix=self.instance_indexes_suffix,
            input_params=input_params,
            receiving_from_python_steps=receiving_from_python_steps,
            class_being_wrapped=class_being_wrapped,
            derived_type_in_array=derived_type_in_array,
            return_value_dimension_specification=return_value_dimension_specification,
            return_value_manager_get_free_instance_number=return_value_manager_get_free_instance_number,
            return_value_manager_get_instance=return_value_manager_get_instance,
            method_name=method_name,
            instance_indexes_suffix=self.instance_indexes_suffix,
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
        fdt = value.definition.as_fortran_data_type()
        base_type = fdt.python_equivalent_type_annotation

        if fdt.is_pointer:
            return base_type

        derived_type = fdt.base_python_type
        return base_type.replace(
            derived_type, f"{derived_type}{self.no_setters_class_suffix}"
        )

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
        return_type_inner = return_type.split("[")[-1].split("]")[0]
        derived_type = value.definition.as_fortran_data_type().base_python_type
        derived_type_no_setters = f"{derived_type}{self.no_setters_class_suffix}"

        template = get_template_in_directory(
            "python-for-fortran-return-value-processing.py.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )

        result = template.render(
            result_name=self.get_python_user_facing_name(value),
            fortran_module_callable=fortran_module_callable,
            fortran_module_callable_args=fortran_module_callable_args,
            instance_indexes_suffix=self.instance_indexes_suffix,
            return_type_inner=return_type_inner,
            derived_type_no_setters=derived_type_no_setters,
        )

        return inject_wrapping_strategy_information(
            result, value=value, wrapping_strategy=self, comment_character="#"
        )

    def get_passing_to_fortran_steps(  # noqa: D102
        self,
        value: Union[MultiReturn, Value],
        dynamic_unit: Optional[str],
    ) -> PassingToFortranSteps:
        argument_instance_indexes = (
            f"{value.definition.name}{self.instance_indexes_suffix}"
        )

        template = get_template_in_directory(
            "python-for-preparing-to-pass-to-fortran.py.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )
        preparatory_python_calls = template.render(
            argument_user_facing=self.get_python_user_facing_name(value),
            argument_instance_indexes=argument_instance_indexes,
        )

        return PassingToFortranSteps(
            preparatory_python_calls=inject_wrapping_strategy_information(
                preparatory_python_calls,
                value=value,
                wrapping_strategy=self,
                comment_character="#",
            ),
            fortran_module_callable_args=(
                (argument_instance_indexes, argument_instance_indexes),
            ),
        )
