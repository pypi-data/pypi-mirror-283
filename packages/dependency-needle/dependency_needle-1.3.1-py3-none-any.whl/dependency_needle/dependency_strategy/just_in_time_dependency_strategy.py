from abc import ABC
from typing import Optional
from dependency_needle.dependency_strategy.\
    dependency_strategy_interface import IDependencyStrategyInterface


class JustInTimeDependencyStrategy(IDependencyStrategyInterface):
    """Scoped strategy for dependency building."""

    def _custom_post_build_strategy(self, interface: ABC,
                                    concrete_class: object,
                                    key_lookup: object) -> None:
        """Just in time post build strategy"""
        return None

    def _custom_pre_build_strategy(self,
                                   interface: ABC,
                                   key_lookup: object) -> Optional[object]:
        """Scoped pre build strategy"""
        if (key_lookup not in self._interface_lifetime_registery_lookup or
            interface not in self._interface_lifetime_registery_lookup
                [key_lookup]):
            raise KeyError(f"interface: {interface} has no registered "
                           "instance for key lookup: {key_lookup}")

        return self._interface_lifetime_registery_lookup[key_lookup][interface]
