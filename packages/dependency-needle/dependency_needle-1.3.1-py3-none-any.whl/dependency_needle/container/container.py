from abc import ABC
from functools import wraps
from inspect import signature

from http.client import HTTPConnection as ClientHTTPConnection
from typing import Dict, Set, Callable
from requests import Request
from starlette.requests import HTTPConnection as StarlletteHTTPConnection

from dependency_needle.constants import ANNOTATIONS, RETURN
from dependency_needle.lifetime_enums import LifeTimeEnums
from dependency_needle.dependency_strategy import (
    IDependencyStrategyInterface,
    ScopedDependencyStrategy,
    TransientDependencyStrategy,
    SingeltonDependencyStrategy,
    JustInTimeDependencyStrategy
)


class Container:
    """Container used to build a class by automating the dependancy injection
    to obtain inversion of control"""

    request_class_types = [
        Request,
        StarlletteHTTPConnection,
        ClientHTTPConnection
    ]

    def __init__(self):
        self.__interface_registery_lookup = {}
        self.__singleton_lookup = {}
        self.__scoped_lookup = {}
        self.__just_in_time_lookup = self.__scoped_lookup
        self.__lifetime_meta_lookup = {
            LifeTimeEnums.SINGLETON: self.__singleton_lookup,
            LifeTimeEnums.SCOPED: self.__scoped_lookup,
            LifeTimeEnums.JUST_IN_TIME: self.__just_in_time_lookup,
            # Un-Used dictionaries.
            LifeTimeEnums.TRANSIENT: {},
        }
        self.__lifetime_strategy_lookup = {
            LifeTimeEnums.SINGLETON: SingeltonDependencyStrategy,
            LifeTimeEnums.TRANSIENT: TransientDependencyStrategy,
            LifeTimeEnums.JUST_IN_TIME: JustInTimeDependencyStrategy,
            # Un-Used dictionaries strategies.
            LifeTimeEnums.SCOPED: ScopedDependencyStrategy
        }

    def __gaurd_build_unregistered_interface(self, interface: ABC):
        """Throw 'KeyError' exception if interface is not registered."""
        if interface not in self.__interface_registery_lookup:
            raise KeyError(f"Interface: {interface} is not registered.")

    def __assert_implementation(self, interface: ABC, concrete_class) -> None:
        """Assert that the concrete class implements the interface
        being registered.

        :param interface: interface needed to be registered.
        :param concrete_class: concrete class implementing the interface.
        :return: None
        """

        if not issubclass(concrete_class, interface):
            raise TypeError(f"Concrete class: {concrete_class}"
                            f" has to implement interface: {interface}.")

    def __assert_abstract_class(self, interface: ABC) -> None:
        """Assert that the interface being registered is an abstract class.

        :param interface: interface needed to be registered.
        :return: None
        """
        if not issubclass(interface, ABC):
            raise TypeError(f"Interface: {interface}"
                            f" has to be an abstract class.")

    def __assert_proper_enum_used(self, enum: LifeTimeEnums) -> None:
        """Assert that the enum being passed is valid.

        :param enum: enum used to register dependency.
        :return: None
        """
        if enum not in LifeTimeEnums.__members__.values():
            raise KeyError(f"Enum: {enum} does not exist in 'LifeTimeEnums'.")

    def __assert_jit_interfaces_contained_in_annotations(
        self,
        jit_interfaces_set: Set,
        annotations: Dict,
    ) -> None:
        """Assert that JIT interfaces set exists within methods\
        annotations

        :param jit_interfaces_set: registered JIT interfaces set.
        :param annotations: decorated methods annotations.
        :return: None.
        """

        annotations_interfaces_set = set([
            interface for interface in annotations.values()
        ])

        if not jit_interfaces_set.issubset(annotations_interfaces_set):
            raise KeyError(f"Annotations: {annotations} "
                           "do not contain all JIT interfaces: "
                           f"{jit_interfaces_set} needed "
                           "for dependency builder decorated function."
                           )

    def __assert_jit_instance_contained_in_passed_kwargs(
        self,
        jit_interfaces_set: Set,
        annotations: Dict,
        kwargs: Dict
    ) -> None:
        """Assert that JIT interfaces set exists within passed kwargs

        :param jit_interfaces_set: registered JIT interfaces set.
        :param annotations: decorated methods annotations.
        :param kwargs: kwargs holding the passed arguments.
        :return: None.
        """
        for key, interface in annotations.items():
            if interface in jit_interfaces_set:
                if key not in kwargs:
                    raise KeyError(
                        f"interface: {interface} is not passed"
                        f" in the dependency builder decorated function"
                        f" kwargs:{kwargs}.")
                passed_kwarg = kwargs[key]
                instance_class = type(passed_kwarg)
                if not issubclass(instance_class, interface):
                    raise TypeError(
                        f"instance: {passed_kwarg} is of type {instance_class}"
                        f" and not of interface type: {interface}."
                    )

    def register_interface(self, interface: ABC,
                           concrete_class,
                           life_time: LifeTimeEnums) -> None:
        """Register interface with a corresponding concrete class to use.

        :param interface: interface needed to be registered.
        :param concrete_class: concrete class implementing the interface.
        :param life_time: life time enum specifying the lifetime of the class.
        :return: None
        """
        if life_time != LifeTimeEnums.JUST_IN_TIME:
            self.__assert_abstract_class(interface)
        self.__assert_implementation(interface, concrete_class)
        self.__assert_proper_enum_used(life_time)
        strategy: IDependencyStrategyInterface = (
            self.__lifetime_strategy_lookup[life_time]
        )

        lookup = self.__lifetime_meta_lookup[life_time]
        self.__interface_registery_lookup[interface] = strategy(
            lookup, interface, concrete_class)

    def build(self, interface: ABC, key_lookup) -> object:
        """Build an interface by utilizing the registery lookup.

        :param interface: interface needed to be built
        :param key_lookup: key_lookup that might be used to lookup\
        registered interfaces.
        :return object: concrete class that implemenets that interface
        """
        self.__gaurd_build_unregistered_interface(interface)
        interface_strategy_instance: IDependencyStrategyInterface = (
            self.__interface_registery_lookup[interface]
        )
        return interface_strategy_instance.build(
            self.__interface_registery_lookup,
            key_lookup
        )

    def clear(self, key_lookup):
        """Clear created dependencies for specific key

        :param key_lookup: immutable key to delete from\
        transient lookup.
        """
        lookups = [
            self.__scoped_lookup,
            self.__just_in_time_lookup,
        ]

        for lookup in lookups:
            if key_lookup in lookup:
                del lookup[key_lookup]

    def __register_jit_interface_instance(self,
                                          interface: ABC,
                                          instance: object,
                                          key_lookup: object) -> None:
        """Register JIT interface instance to container's\
        JIT dependencies lookup.

        :param interface: interface to register.
        :instance: instace value of regsitered interface.
        :key_lookup: key look up corresponding to interface registery.
        :return: None.
        """
        class_type = type(instance)
        life_time = LifeTimeEnums.JUST_IN_TIME
        self.register_interface(interface, class_type, life_time)

        if key_lookup in self.__just_in_time_lookup:
            self.__just_in_time_lookup[key_lookup][interface] = instance
        else:
            self.__just_in_time_lookup[key_lookup] = {
                interface: instance
            }

    def build_dependencies_decorator(self,
                                     jit_interfaces: Set = set()) -> Callable:
        """Build a method dependencies decorator to wrap\
        a given function to build its dependencies\
        if they are registered.

        :param jit_interfaces: List of JIT interfaces that should
        get injected in runtime.
        :return: dependencies builder decorator.
        """

        def dependencies_decorator(fn):
            """Wrap a given function to build its dependencies\
            if they are registered.

            :param fn: function with request/identifier as its\
            first parameter or an annotated parameter of type "Request".
            :return: wrapped function.
            """
            dependencies = {}

            if hasattr(fn, ANNOTATIONS):
                dependencies: dict = getattr(
                    fn,
                    ANNOTATIONS
                )

            self.__assert_jit_interfaces_contained_in_annotations(
                jit_interfaces,
                dependencies
            )

            @wraps(fn)
            def wrapper(*args, **kwargs):
                if dependencies:
                    # Get request from annotations if it exists.
                    request_kwarg_key = ''
                    for key, class_type in dependencies.items():
                        if any([
                            issubclass(class_type, request_type)
                            for request_type in Container.request_class_types
                            if key != RETURN
                        ]):
                            request_kwarg_key = key

                    built_dependencies = {}
                    if request_kwarg_key:
                        request_or_identifier = kwargs.pop(request_kwarg_key)
                        dependencies.pop(request_kwarg_key)
                        # Assign request to kwargs as it'll be passed
                        # as a kwarg if its annotated.
                        built_dependencies[request_kwarg_key] = (
                            request_or_identifier
                        )
                    else:
                        try:
                            request_or_identifier = args[0]
                        except IndexError:
                            raise IndexError(
                                "Request parameter doesn't exist as an"
                                " annotated parameter or first parameter."
                            )

                    self.__assert_jit_instance_contained_in_passed_kwargs(
                        jit_interfaces,
                        dependencies,
                        kwargs
                    )

                    # Register Just-In-Time dependencies.
                    for key, interface in dependencies.items():
                        try:
                            if interface in jit_interfaces:
                                instance = kwargs[key]
                                self.__register_jit_interface_instance(
                                    interface,
                                    instance,
                                    request_or_identifier
                                )
                        except KeyError:
                            continue

                    for key, interface in dependencies.items():
                        try:
                            if key != RETURN:
                                built_dependencies[key] = self.build(
                                    interface, request_or_identifier
                                )
                        except (KeyError, TypeError):
                            continue

                    kwargs.update(built_dependencies)

                try:
                    result = fn(*args, **kwargs)
                finally:
                    self.clear(request_or_identifier)

                return result

            func_signature = signature(wrapper)
            wrapper_signature = func_signature.replace(
                parameters=[
                    parameter for parameter
                    in func_signature.parameters.values()
                    if parameter.annotation
                    not in self.__interface_registery_lookup
                ]
            )
            wrapper.__signature__ = wrapper_signature
            return wrapper

        return dependencies_decorator
