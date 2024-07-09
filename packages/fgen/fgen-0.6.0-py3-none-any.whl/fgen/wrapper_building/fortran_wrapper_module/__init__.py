"""
Generation of the Fortran wrapper module
"""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Union

from attrs import define, evolve, frozen

from fgen.data_models import Module, MultiReturn, Package, PackageSharedElements, Value
from fgen.jinja_environment import (
    JINJA_ENV,
    get_template_in_directory,
    post_process_jinja_rendering,
)
from fgen.wrapping_strategies import (
    WrappingStrategyLike,
    get_wrapping_strategy,
)
from fgen.wrapping_strategies.receiving_from_python_steps import (
    ReceivingFromPythonSteps,
)


@define
class FortranWrapperModuleBuilder:
    """
    Builder of a Fortran wrapper module
    """

    package: Package
    """
    Package for which the builder is building wrappers
    """

    module: Module
    """
    Module for which to build the wrapper
    """

    shared: PackageSharedElements
    """
    Elements which have to be shared across the package

    For example, the names of functions which are used in more than one wrapper module.
    """

    def get_wrapping_strategy(
        self, value: Union[MultiReturn, Value]
    ) -> WrappingStrategyLike:
        """
        Get wrapping strategy

        Parameters
        ----------
        value
            Value for which to get the wrapping strategy

        Returns
        -------
            Wrapping strategy to use with the value
        """
        return get_wrapping_strategy(value.definition.as_fortran_data_type())

    def get_module_level_docstring(self) -> str:
        """
        Get the module-level docstring

        Returns
        -------
            Module-level docstring
        """
        template = get_template_in_directory(
            "module-level-docstring.f90.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(module=self.module)

        return result

    def get_module_use_statements(self) -> str:
        """
        Get the module-level use statements

        Returns
        -------
            Module-level use statements
        """
        template = get_template_in_directory(
            "module-use-statements.f90.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(builder=self)

        return result

    def get_requirements_fortran_use_statements(self) -> str:
        """
        Get the Fortran ``use`` statements needed for the module

        Returns
        -------
            Fortran ``use`` statements needed for the module
        """
        requirements_template = get_template_in_directory(
            "module-use-requirements.f90.jinja", Path(__file__).parent, JINJA_ENV
        )

        required_use_statements = self.get_requirements_fortran_uses(self.module)

        out: list[str] = []
        for providing_module_name in sorted(required_use_statements.keys()):
            needed_type = required_use_statements[providing_module_name]

            if isinstance(needed_type.providing_module, Module):
                providing_module_manager_name = (
                    needed_type.providing_module.manager_module_name
                )
            else:
                providing_module_manager_name = needed_type.providing_module

            rendered = requirements_template.render(
                providing_module_name=providing_module_name,
                required_type=needed_type.name,
                requires_get_instance=needed_type.requires_get_instance,
                requires_get_free_instance_number=needed_type.requires_get_free_instance_number,
                providing_module_manager_name=providing_module_manager_name,
                shared=self.shared,
            )
            # Strip out blank and trailing new lines,
            # not sure how to make jinja behave so just using Python instead.
            out.append("\n".join([v for v in rendered.splitlines()]))

        return "\n".join(out)

    def get_requirements_fortran_uses(self, module: Module) -> dict[str, NeededType]:
        """
        Get the Fortran ``use``'s needed for the module

        Parameters
        ----------
        module
            Module for which to get the ``use``'s

        Returns
        -------
            Fortran ``use`` statements needed for the module
        """
        required_use_statements: dict[str, NeededType] = {}

        provided_type = module.provides
        provided_type_attributes = provided_type.exposed_attributes.values()
        provided_type_method_arguments = [
            argument
            for method in provided_type.methods.values()
            for argument in method.parameters.values()
        ]
        provided_type_method_return_values = [
            method.returns for method in provided_type.methods.values()
        ]
        for value, include_get_free_instance_number in [
            *[(v, True) for v in provided_type_attributes],
            *[(v, False) for v in provided_type_method_arguments],
            *[(v, True) for v in provided_type_method_return_values],
        ]:
            if self.requires_import(value, module):
                fdt = value.definition.as_fortran_data_type()

                if fdt.is_enum:
                    needed_type_str = fdt.equivalent_python_type

                elif fdt.is_array_of_derived_type:
                    needed_type_str = fdt.base_python_type

                else:
                    needed_type_str = value.definition.python_type_as_str()

                requirement = module.get_requirement_that_provides(needed_type_str)

                if (
                    not fdt.is_enum
                    and requirement.fortran_module in required_use_statements
                ):
                    if (
                        needed_type_str
                        != required_use_statements[requirement.fortran_module].name
                    ):
                        msg = (
                            "Each module should only provide one type. "
                            f"You are requesting {needed_type_str}, "
                            f"but have already said that {requirement} "
                            "provides "
                            f"{required_use_statements[requirement.fortran_module]}"
                        )
                        raise AssertionError(msg)

                    updated_requires_get_free_instance_number = (
                        include_get_free_instance_number
                        or required_use_statements[
                            requirement.fortran_module
                        ].requires_get_free_instance_number
                    )

                    required_use_statements[requirement.fortran_module] = evolve(
                        required_use_statements[requirement.fortran_module],
                        requires_get_free_instance_number=updated_requires_get_free_instance_number,
                    )

                else:
                    if fdt.is_enum:
                        needed_type = NeededType(
                            name=needed_type_str,
                            providing_module=requirement.fortran_module,
                            requires_get_instance=False,
                            requires_get_free_instance_number=False,
                        )

                    else:
                        requirement_providing_module = (
                            self.package.get_module_that_provides_values_type(value)
                        )
                        needed_type = NeededType(
                            name=needed_type_str,
                            providing_module=requirement_providing_module,
                            requires_get_instance=True,
                            requires_get_free_instance_number=include_get_free_instance_number,
                        )

                    required_use_statements[requirement.fortran_module] = needed_type

        return required_use_statements

    def requires_import(self, value: Union[Value, MultiReturn], module: Module) -> bool:
        """
        Return whether a value requires an import or not

        Parameters
        ----------
        value
            Value to check

        module
            Module in which the value is being used

        Returns
        -------
            ``True`` if this values requires an import, ``False`` otherwise.
        """
        fdt = value.definition.as_fortran_data_type()

        if fdt.is_derived_type or fdt.is_array_of_derived_type:
            # If the type we need is defined by the module, we don't need to import it
            return not (fdt.equivalent_python_type == module.provides.name)

        if fdt.is_enum:
            return True

        return False

    def get_statement_declarations_getters_and_setters(self) -> str:
        """
        Get the statement declarations for getters and setters

        Returns
        -------
            Statement declarations for the getters and setters
        """
        out: list[str] = []
        for attribute in self.module.provides.exposed_attributes.values():
            ws = self.get_wrapping_strategy(attribute)

            statement_declarations = (
                ws.get_fortran_wrapper_statement_declarations_getters_and_setters(
                    attribute
                )
            )
            out.extend(statement_declarations)

        return "\n".join(out)

    def get_statement_declarations_methods(self) -> str:
        """
        Get the statement declarations for methods

        Returns
        -------
            Statement declarations for the methods
            exposed by the derived type defined by this module.
        """
        out: list[str] = []
        for method in self.module.provides.methods.values():
            return_value = method.returns
            ws = self.get_wrapping_strategy(return_value)

            statement_declarations = ws.get_fortran_wrapper_statement_declarations_for_returning_method_result_to_python(  # noqa: E501
                method, prefix=self.shared.fortran_wrapper_method_prefix
            )
            out.extend(statement_declarations)

        return "\n".join(out)

    def get_provided_type_build_methods(self) -> str:
        """
        Get the provided type's build methods

        Returns
        -------
            Class methods
        """
        template = get_template_in_directory(
            "provided-type-method-no-return.f90.jinja", Path(__file__).parent, JINJA_ENV
        )

        receiving_from_python_steps = self.get_receiving_from_python_steps(
            self.module.provides.attributes.values()
        )
        input_params = (
            receiving_from_python_steps.fortran_wrapper_callable_parameter_names
        )

        result = template.render(
            builder=self,
            shared=self.shared,
            fortran_wrapper_callable=self.shared.fortran_build_callable_name,
            fortran_module_callable="instance % build",
            receiving_from_python_steps=receiving_from_python_steps,
            input_params=input_params,
        )

        return result

    def get_provided_type_getters_and_setters(self) -> str:
        """
        Get the provided type's getters and setters

        Returns
        -------
            Provided type's getters and setters
        """
        template_setter = get_template_in_directory(
            "provided-type-setter.f90.jinja",
            Path(__file__).parent,
            JINJA_ENV,
        )
        result: list[str] = []

        for att in self.module.provides.exposed_attributes.values():
            att_ws = self.get_wrapping_strategy(att)

            if (
                att.definition.as_fortran_data_type().is_derived_type
                or att.definition.as_fortran_data_type().is_array_of_derived_type
            ):
                att_providing_module = (
                    self.package.get_module_that_provides_values_type(att)
                )
                att_manager_get_free_instance_number = "_".join(
                    [
                        att_providing_module.manager_module_name,
                        self.shared.fortran_get_free_instance_number_callable_name,
                    ]
                )
                att_manager_get_instance = "_".join(
                    [
                        att_providing_module.manager_module_name,
                        self.shared.fortran_get_instance_callable_name,
                    ]
                )

            else:
                att_manager_get_free_instance_number = None
                att_manager_get_instance = None

            att_getter = att_ws.get_fortran_for_getter(
                value=att,
                class_being_wrapped=self.module.provides.name,
                value_manager_get_free_instance_number=att_manager_get_free_instance_number,
                value_manager_get_instance=att_manager_get_instance,
            )
            result.append(att_getter)

            receiving_from_python_steps = self.get_receiving_from_python_steps([att])
            if len(receiving_from_python_steps.fortran_module_callable_args) != 1:
                msg = (
                    "Only one value should be needed for the setter. We have: "
                    f"{receiving_from_python_steps.fortran_module_callable_args=}"
                )
                raise AssertionError(msg)

            fortran_module_attribute_to_set = (
                receiving_from_python_steps.fortran_module_callable_args[0]
            )
            setter_input_params = (
                receiving_from_python_steps.fortran_wrapper_callable_parameter_names
            )

            att_setter = template_setter.render(
                builder=self,
                fortran_wrapper_callable=att_ws.get_fortran_wrapper_module_setter(att),
                receiving_from_python_steps=receiving_from_python_steps,
                input_params=setter_input_params,
                fortran_module_attribute_to_set=fortran_module_attribute_to_set,
            )
            result.append(att_setter)

        return "\n\n".join(result)

    def get_provided_type_methods(self) -> str:
        """
        Get the provided type's methods

        Returns
        -------
            Provided type's methods
        """
        result: list[str] = []
        for method in self.module.provides.methods.values():
            method_returns = method.returns
            ws_method_returns = self.get_wrapping_strategy(method_returns)

            fdt_return = method_returns.definition.as_fortran_data_type()
            if fdt_return.is_derived_type or fdt_return.is_array_of_derived_type:
                method_returns_providing_module = (
                    self.package.get_module_that_provides_values_type(method_returns)
                )

                if method_returns_providing_module == self.module:
                    # TODO: remove hard-coding here and use shared instead.
                    # Also requires changes to module-use-statements.f90.jina.
                    method_returns_manager_get_free_instance_number = (
                        "manager_get_free_instance"
                    )
                    method_returns_manager_get_instance = "manager_get_instance"

                else:
                    method_returns_manager_get_free_instance_number = "_".join(
                        [
                            method_returns_providing_module.manager_module_name,
                            self.shared.fortran_get_free_instance_number_callable_name,
                        ]
                    )
                    method_returns_manager_get_instance = "_".join(
                        [
                            method_returns_providing_module.manager_module_name,
                            self.shared.fortran_get_instance_callable_name,
                        ]
                    )

            else:
                method_returns_manager_get_free_instance_number = None
                method_returns_manager_get_instance = None

            receiving_from_python_steps = self.get_receiving_from_python_steps(
                method.parameters.values()
            )
            method_fortran = ws_method_returns.get_fortran_for_method_returning_wrapped_type(  # noqa: E501
                fortran_wrapper_module_callable=f"{self.shared.fortran_wrapper_method_prefix}{method.name}",
                receiving_from_python_steps=receiving_from_python_steps,
                return_value=method_returns,
                class_being_wrapped=self.module.provides.name,
                method_name=method.name,
                return_value_manager_get_free_instance_number=method_returns_manager_get_free_instance_number,
                return_value_manager_get_instance=method_returns_manager_get_instance,
            )
            result.append(method_fortran)

        return "\n\n".join(result)

    def get_receiving_from_python_steps(
        self,
        arguments: Iterable[Union[MultiReturn, Value]],
    ) -> ReceivingFromPythonSteps:
        """
        Get receiving from Python steps for a set of arguments

        Parameters
        ----------
        arguments
            Arguments for which to get the receiving from Python steps

        Returns
        -------
            Steps for receiving the arguments from Python
        """
        postprocessing_fortran_calls_list = []
        fortran_wrapper_callable_parameters: list[
            tuple[str, str, Union[MultiReturn, Value]]
        ] = []
        fortran_module_callable_args: list[Union[MultiReturn, Value]] = []
        fortran_helper_variables: list[tuple[str, str]] = []

        for argument in arguments:
            ws = self.get_wrapping_strategy(argument)

            argument_steps = ws.get_receiving_from_python_steps(
                value=argument,
                providing_module=self.package.find_providing_module(argument),
                requesting_module=self.module,
                get_instance_callable_name=self.shared.fortran_get_instance_callable_name,
                # At the moment, dynamic unit doesn't affect
                # the name on the Fortran side
                # so we can simply always pass None here.
                dynamic_unit=None,
            )

            if argument_steps.postprocessing_fortran_calls is not None:
                postprocessing_fortran_calls_list.append(
                    argument_steps.postprocessing_fortran_calls
                )

            fortran_wrapper_callable_parameters.extend(
                argument_steps.fortran_wrapper_callable_parameters
            )

            fortran_module_callable_args.extend(
                argument_steps.fortran_module_callable_args
            )

            fortran_helper_variables.extend(argument_steps.fortran_helper_variables)

        if postprocessing_fortran_calls_list:
            postprocessing_fortran_calls = "\n".join(postprocessing_fortran_calls_list)
        else:
            postprocessing_fortran_calls = None

        return ReceivingFromPythonSteps(
            postprocessing_fortran_calls=postprocessing_fortran_calls,
            fortran_wrapper_callable_parameters=tuple(
                fortran_wrapper_callable_parameters
            ),
            fortran_module_callable_args=tuple(fortran_module_callable_args),
            fortran_helper_variables=tuple(fortran_helper_variables),
        )


@frozen
class NeededType:
    """
    Helper class for keeping track of the first-party types needed by the modle
    """

    name: str
    """Name of the needed type"""

    providing_module: Union[Module, str]
    """Module or name of the module which provides this type"""

    requires_get_instance: bool
    """
    Whether this needed type also requires its ``get_instance`` function
    """

    requires_get_free_instance_number: bool
    """
    Whether this needed type also requires its ``get_free_instance_number`` function
    """


def generate_fortran_wrapper_module(builder: FortranWrapperModuleBuilder) -> str:
    """
    Generate the Fortran wrapper module

    Parameters
    ----------
    builder
        Builder to use to generate the Fortran wrapper module

    Returns
    -------
        Fortran wrapper module as code
    """
    template = get_template_in_directory(
        "fortran-wrapper-module.f90.jinja", Path(__file__).parent, JINJA_ENV
    )

    result = post_process_jinja_rendering(
        # TODO: switch to passing in builder
        template.render(builder=builder, package=builder.package, module=builder.module)
    )

    return result
