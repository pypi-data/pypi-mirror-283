"""
Generation of the Python wrapper module
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Union

from attrs import define

from fgen.data_models import (
    Method,
    Module,
    MultiReturn,
    Package,
    PackageSharedElements,
    Value,
)
from fgen.jinja_environment import (
    JINJA_ENV,
    get_template_in_directory,
    post_process_jinja_rendering,
)
from fgen.wrapper_building.formatting import format_python_code
from fgen.wrapping_strategies import (
    PassingToFortranSteps,
    WrappingStrategyLike,
    get_wrapping_strategy,
)


@define
class PythonWrapperModuleBuilder:
    """
    Builder of a Python wrapper module
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

    @property
    def requires_union(self) -> bool:
        """
        Whether the module being wrapped requires ``typing.Union``
        """

        def needs_union(val: Union[MultiReturn, Value]) -> bool:
            fdt = val.definition.as_fortran_data_type()
            return fdt.is_derived_type and not fdt.is_pointer

        attributes_require_union = any(
            needs_union(a) for a in self.module.provides.exposed_attributes.values()
        )

        methods_require_union = any(
            any(needs_union(p) for p in method.parameters.values())
            for method in self.module.provides.methods.values()
        )

        return attributes_require_union or methods_require_union

    @property
    def requires_np(self) -> bool:
        """
        Whether the module being wrapped requires ``numpy as np``
        """

        def needs_np(val: Union[MultiReturn, Value]) -> bool:
            fdt = val.definition.as_fortran_data_type()
            return fdt.is_deferred_array

        attributes_require_np = any(
            needs_np(a) for a in self.module.provides.exposed_attributes.values()
        )

        methods_require_np = any(
            needs_np(method.returns)
            or any(needs_np(p) for p in method.parameters.values())
            for method in self.module.provides.methods.values()
        )

        return attributes_require_np or methods_require_np

    @property
    def requires_npt(self) -> bool:
        """
        Whether the module being wrapped requires ``numpy.typing as npt``
        """

        def needs_npt(val: Union[MultiReturn, Value]) -> bool:
            fdt = val.definition.as_fortran_data_type()
            return (
                fdt.is_deferred_array
                and not fdt.is_array_of_derived_type
                and not val.dynamic_unit
            )

        attributes_require_npt = any(
            needs_npt(a) for a in self.module.provides.exposed_attributes.values()
        )

        methods_require_npt = any(
            needs_npt(method.returns)
            or any(needs_npt(p) for p in method.parameters.values())
            for method in self.module.provides.methods.values()
        )

        return attributes_require_npt or methods_require_npt

    @property
    def requires_quantity(self) -> bool:
        """
        Whether the module being wrapped requires ``pint``'s quantity to be exposed
        """

        def needs_quantity(val: Union[MultiReturn, Value]) -> bool:
            return bool(val.dynamic_unit)

        attributes_require_quantity = any(
            needs_quantity(a) for a in self.module.provides.exposed_attributes.values()
        )

        methods_require_quantity = any(
            needs_quantity(method.returns)
            or any(needs_quantity(p) for p in method.parameters.values())
            for method in self.module.provides.methods.values()
        )

        return attributes_require_quantity or methods_require_quantity

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
            "module-level-docstring.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(
            wrapper_module_name=self.module.wrapper_module_name,
            fortran_module_name=self.module.name,
        )

        return result

    def get_module_imports(self, extension: str) -> str:
        """
        Get the module's imports

        Parameters
        ----------
        extension
            The name of the overall extension module being built

        Returns
        -------
            Module ``import`` statements
        """
        template = get_template_in_directory(
            "module-imports.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(builder=self, extension=extension)

        return result

    def get_requirements_python_import_statements(self) -> str:
        """
        Get the Python ``import`` statements needed for the module's requirements

        These requirements are the requirements defined in
        ``self.module.requirements``.

        Returns
        -------
            Python ``import`` statements needed for the module
        """
        requirements_template = get_template_in_directory(
            "module-imports-requirements.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        required_imports = self.get_requirements_python_imports(self.module)

        out: list[str] = []
        for providing_module in sorted(required_imports.keys()):
            imports = sorted(required_imports[providing_module])
            imports_str = ", ".join(imports)

            rendered = requirements_template.render(
                providing_module=providing_module, imports_str=imports_str
            )
            out.append(rendered)
            out.append("\n")

        return "\n".join(out)

    def get_enum_python_import_statements(self) -> Optional[str]:
        """
        Get the Python ``import`` statements needed for enums used by ``self.module``

        Returns
        -------
            Python ``import`` statements needed for any enums used by ``self.module``.
            If no imports are required for enums, ``None`` is returned.
        """
        required_enums = []
        to_check = [
            self.module.provides.attributes.values(),
            *[
                method.parameters.values()
                for method in self.module.provides.methods.values()
            ],
            *[[method.returns] for method in self.module.provides.methods.values()],
        ]

        for to_check_group in to_check:
            for to_check_value in to_check_group:
                to_check_fdt = to_check_value.definition.as_fortran_data_type()
                if to_check_fdt.is_enum and to_check_value not in required_enums:
                    required_enums.append(to_check_value)

        if not required_enums:
            return None

        providers = defaultdict(list)
        out: list[str] = []
        for required_enum in required_enums:
            fdt = required_enum.definition.as_fortran_data_type()
            python_equivalent_type = fdt.python_equivalent_type_annotation
            providing_requirement = self.module.get_requirement_that_provides(
                python_equivalent_type
            )
            providers[providing_requirement.python_module].append(
                python_equivalent_type
            )

        for provider, provides in providers.items():
            out.append(f"from {provider} import {','.join(set(provides))}")

        return "\n".join(out)

    def get_requirements_python_imports(self, module: Module) -> dict[str, list[str]]:
        """
        Get the Python imports needed for the module's requirements

        These requirements are the requirements defined in
        ``self.module.requirements``.

        Parameters
        ----------
        module
            Module for which to get the ``import`` statements

        Returns
        -------
            Modules (keys) and the types to import from them (values)
        """
        required_imports: dict[str, list[str]] = defaultdict(list)

        provided_type_attributes = module.provides.exposed_attributes.values()
        provided_type_method_arguments = [
            argument
            for method in module.provides.methods.values()
            for argument in method.parameters.values()
        ]
        provided_type_method_return_values = [
            method.returns for method in module.provides.methods.values()
        ]
        for value, can_be_callable_argument in [
            *[(v, True) for v in provided_type_attributes],
            *[(v, True) for v in provided_type_method_arguments],
            *[(v, False) for v in provided_type_method_return_values],
        ]:
            if self.requires_import(value, module):
                base_type, needed_types = self.get_python_base_type_and_needed_types(
                    value, can_be_callable_argument=can_be_callable_argument
                )
                providing_requirement = module.get_requirement_that_provides(base_type)

                for needed_type in needed_types:
                    if (
                        needed_type
                        not in required_imports[providing_requirement.python_module]
                    ):
                        required_imports[providing_requirement.python_module].append(
                            needed_type
                        )

        return required_imports

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
        if not (fdt.is_derived_type or fdt.is_array_of_derived_type):
            return False

        if fdt.is_array_of_derived_type:
            needed_type_str = fdt.base_python_type

        else:
            needed_type_str = fdt.equivalent_python_type

        # If the type we need is defined by the module, we don't need to import it
        return not (needed_type_str == module.provides.name)

    @staticmethod
    def get_python_base_type_and_needed_types(
        value: Union[Value, MultiReturn],
        can_be_callable_argument: bool,
    ) -> tuple[str, tuple[str, ...]]:
        """
        Get the base type and the type we need to import

        Parameters
        ----------
        value
            Value for which to get the need type to import

        can_be_callable_argument
            Whether this value could be a callable's argument

        Returns
        -------
            Tuple. First element is the base type.
            The second type is the types that need to be imported.
        """
        vfdt = value.definition.as_fortran_data_type()
        if vfdt.is_array_of_derived_type:
            base_type = vfdt.base_python_type

        else:
            base_type = value.definition.python_type_as_str()

        no_setters_type = f"{base_type}NoSetters"

        if can_be_callable_argument:
            if vfdt.is_pointer:
                return (base_type, (base_type,))

            return (base_type, (base_type, no_setters_type))

        if vfdt.is_pointer:
            return (base_type, (base_type,))

        return (base_type, (no_setters_type,))

    def get_module_units(self) -> str:
        """
        Get the module's units declaration

        Returns
        -------
            Module's units declaration
        """
        template = get_template_in_directory(
            "module-units.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        units = {}
        units_multi_return = {}
        for k, v in self.module.provides.units.items():
            if isinstance(v, str):
                units[k] = v
            elif isinstance(v, tuple):
                units_multi_return[k] = v
            else:  # pragma: no cover
                # Should be impossible to get here, but just in case
                msg = f"We don't yet support units of type {type(v)} here"  # type: ignore[unreachable]
                raise NotImplementedError(msg)

        result = template.render(
            units=units,
            units_multi_return=units_multi_return,
        )

        return result

    def get_provided_type_docstring(self) -> str:
        """
        Get the provided type's docstring

        Returns
        -------
            Provided type's docstring
        """
        template = get_template_in_directory(
            "provided-type-docstring.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(
            provided_type=self.module.provides.name,
            provided_type_description=self.module.provides.description,
        )

        return result

    def get_verify_units_decorator(
        self,
        arguments: Iterable[Union[MultiReturn, Value]],
        return_value: Optional[Union[MultiReturn, Value]] = None,
        include_self_argument: bool = True,
    ) -> str:
        """
        Get the ``verify_units`` decorator for a callable

        Parameters
        ----------
        arguments
            Arguments for the callable

        return_value
            Return value from the callable

        include_self_argument
            Should we assume that there is a ``self`` argument to the callable too?

        Returns
        -------
            ``verify_units`` decorator for the callable
        """
        template = get_template_in_directory(
            "verify-units-decorator.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        arguments_info_for_verify_units: list[Union[str, None]] = []
        if include_self_argument:
            arguments_info_for_verify_units.append(None)

        for arg in arguments:
            if not self.include_in_python_callable_arguments(arg):
                continue

            if arg.unit:
                arguments_info_for_verify_units.append(
                    f'_UNITS["{self.get_python_user_facing_name(arg)}"]'
                )
            else:
                arguments_info_for_verify_units.append(None)

        return_info_for_verify_units: Union[None, str, list[str]] = None
        if (return_value is not None) and return_value.requires_units:
            if return_value.unit is None:  # pragma: no cover
                msg = (
                    "How did we get here? "
                    "Should have failed at initialisation of {return_value}"
                )
                raise AssertionError(msg)

            python_facing_name = self.get_python_user_facing_name(return_value)
            if isinstance(return_value, MultiReturn):
                return_info_for_verify_units = (
                    f'_UNITS_MULTI_RETURN["{python_facing_name}"]'
                )
            else:
                return_info_for_verify_units = f'_UNITS["{python_facing_name}"]'

        result = template.render(
            arguments_info_for_verify_units=arguments_info_for_verify_units,
            return_info_for_verify_units=return_info_for_verify_units,
        )

        return result

    def get_post_verify_units_argument_list(
        self, arguments: Iterable[Union[MultiReturn, Value]]
    ) -> str:
        r"""
        Get argument list to be used, assuming the ``verify_units`` decorator is applied

        The argument list includes the type hints that are expected.
        These type hints are created on the assumption that the ``verify_units``
        is being used on the callable.

        Parameters
        ----------
        arguments
            Arguments for which to generate the arguments list.

        Returns
        -------
            Arguments list, in the form "argument: type,\narg: type_arg\n..."
        """
        out = []
        for arg in arguments:
            if not self.include_in_python_callable_arguments(arg):
                continue

            ws = self.get_wrapping_strategy(arg)
            name = ws.get_python_user_facing_name(arg)
            type_hint = ws.get_python_post_verify_units_input_type_annotation(arg)
            out.append(f"{name}: {type_hint},")

        return "\n".join(out)

    def get_provided_type_repr_methods(self) -> str:
        """
        Get the provided type's representation relevant methods

        Returns
        -------
            Representation-relevant methods for the provided type
        """
        template = get_template_in_directory(
            "provided-type-str-repr-methods.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(
            exposed_attributes=self.module.provides.exposed_attributes,
        )

        return result

    def get_provided_type_class_methods(self, class_name: str) -> str:
        """
        Get the provided type's class methods

        Parameters
        ----------
        class_name
            Name of the class for which we are getting the class methods.

        Returns
        -------
            Class methods
        """
        template = get_template_in_directory(
            "provided-type-class-methods.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(
            builder=self,
            shared=self.shared,
            class_name=class_name,
        )

        return result

    def get_provided_type_getters_and_setters(
        self, include_setters: bool = True
    ) -> str:
        """
        Get the provided type's getters and setters

        Parameters
        ----------
        include_setters
            Should the setters be created too?

        Returns
        -------
            Provided type's getters and setters
        """
        template = get_template_in_directory(
            "getters-and-setters.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(
            builder=self,
            attributes=self.module.provides.exposed_attributes.values(),
            include_setters=include_setters,
        )

        return result

    def get_provided_type_methods(self) -> str:
        """
        Get the provided type's methods

        Returns
        -------
            Provided type's methods
        """
        template = get_template_in_directory(
            "methods.py.jinja", Path(__file__).parent, JINJA_ENV
        )

        result = template.render(
            builder=self, methods=self.module.provides.methods.values()
        )

        return result

    def get_fortran_wrapper_method(self, method: Method) -> str:
        """
        Get the name of the method in the Fotran wrapper

        Parameters
        ----------
        method
            Method for which to get the name

        Returns
        -------
            Name of the method in the Fortran wrapper
        """
        return f"i_{method.name}"

    def get_passing_to_fortran_steps(
        self,
        arguments: Iterable[Union[MultiReturn, Value]],
        dynamic_unit: Optional[str] = None,
    ) -> PassingToFortranSteps:
        """
        Get passing to Fortran steps for a set of arguments

        Parameters
        ----------
        arguments
            Arguments for the callable. We get the Fortran passing steps for these.

        dynamic_unit
            If provided, specifies the source of the units
            to which we want to convert the arguments.

        Returns
        -------
            Steps for passing the arguments to Fortran
        """
        preparatory_python_calls_list = []
        fortran_module_callable_args: list[tuple[str, str]] = []
        for argument in arguments:
            if not self.include_in_python_callable_arguments(argument):
                # Let wrappers handle this
                continue

            ws = self.get_wrapping_strategy(argument)
            if argument.dynamic_unit:
                if isinstance(argument.dynamic_unit, str):
                    dynamic_unit_argument = argument.dynamic_unit

                elif dynamic_unit is None:
                    msg = "If dynamic unit is True, the source must be provided"
                    raise AssertionError(msg)

                else:
                    dynamic_unit_argument = dynamic_unit

            else:
                dynamic_unit_argument = None

            argument_steps = ws.get_passing_to_fortran_steps(
                value=argument, dynamic_unit=dynamic_unit_argument
            )

            if argument_steps.preparatory_python_calls is not None:
                preparatory_python_calls_list.append(
                    argument_steps.preparatory_python_calls
                )

            fortran_module_callable_args.extend(
                argument_steps.fortran_module_callable_args
            )

        if not preparatory_python_calls_list:
            preparatory_python_calls = None
        else:
            preparatory_python_calls = "\n".join(preparatory_python_calls_list)

        return PassingToFortranSteps(
            preparatory_python_calls=preparatory_python_calls,
            fortran_module_callable_args=tuple(fortran_module_callable_args),
        )

    def get_python_user_facing_name(self, value: Union[MultiReturn, Value]) -> str:
        """
        Get the Python-user facing name of a value

        Parameters
        ----------
        value
            Value for which to get the Python user-facing name

        Returns
        -------
            Python user-facing name
        """
        ws = self.get_wrapping_strategy(value)
        return ws.get_python_user_facing_name(value)

    def include_in_python_callable_arguments(
        self, value: Union[MultiReturn, Value]
    ) -> bool:
        """
        Determine whether a value should be included as an argument to Python callables

        Parameters
        ----------
        value
            Value to check

        Returns
        -------
            ``True`` if the value should be included as an argument to Python callables,
            ``False`` otherwise.
        """
        return not value.definition.is_fortran_units_holder


def generate_python_wrapper_module(
    builder: PythonWrapperModuleBuilder, extension: str
) -> str:
    """
    Generate the Python wrapper module

    Parameters
    ----------
    builder
        Builder to use to generate the Python wrapper module

    extension
        Name of the extension module that will contain the compiled wrappers

    Returns
    -------
        Python wrapper module as code
    """
    template = get_template_in_directory(
        "python-wrapper-module.py.jinja", Path(__file__).parent, JINJA_ENV
    )

    result = post_process_jinja_rendering(
        template.render(
            builder=builder,
            extension=extension,
        )
    )

    return format_python_code(result)
