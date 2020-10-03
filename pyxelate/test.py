from copy import copy
from typing import List, Tuple, Union, Iterator


import numpy as np


class Size:
    def __init__(self, size: Union[int, None]):
        """
        Create a Size object with the given size. If the size passed
            in is None, then it is treated as infinite
        :param size: the size
        """
        self.size = size

    def is_infinite(self) -> bool:
        """
        Return True if this Size is infinite, and False otherwise
        :return: whether or not this Size is infinite
        """
        return self.size is None


class Rule:

    def __init__(self, window: np.ndarray, center: Tuple[int, ...], becomes: Union[0, 1]):
        """
        Create a single evolution rule
        :param window: matrix of dead (0) and alive (1) cells
        :param center: index of the target cell in the window
        :param becomes: what the target cell becomes in the next generation
        """
        if len(center) != len(window.shape):
            raise ValueError("Center must have the same dimensions as the window")

        self.window = window
        self.center = center
        self.becomes = becomes


class RuleList:

    def __init__(self, rules: Union[List[Rule], None] = None):
        """
        Create a complete set of evolution rules for the universe
        """
        self._rules = rules if rules is not None else []

    def add_rule(self, rule: Rule) -> None:
        """
        Add a Rule to the RuleList
        :param rule: the Rule
        :return: None
        """
        self._rules.append(rule)

    def __iter__(self) -> Iterator:
        """
        Get an iterator over all Rules in the RuleList
        :return: the Rule iterator
        """
        return iter(self._rules)


class Universe:

    def __init__(self, dimensions: int, size: Size):
        self._dimensions = dimensions
        self._size = size

        if size.is_infinite():
            raise ValueError("Infinite universes not yet supported")

        if dimensions == 1:
            self._universe = np.array([0] * size.size)
        elif dimensions == 2:
            self._universe = np.array([[0] * size.size for _ in range(size.size)])
        else:
            raise ValueError("Higher than 2-D universes not supported")

    def __repr__(self) -> str:
        if self._dimensions == 1:
            return ''.join(map(str, self._universe))
        else:
            print('\n'.join([''.join(map(str, row)) for row in self._universe]))

    def apply(self, rules: RuleList) -> None:
        """
        Apply an evolution rules to the cells in the universe
        :param rules: the rules to apply
        :return: None
        """
        for rule in rules:
            if len(rule.window.shape) != self._dimensions:
                raise ValueError("Rules must match the dimensions")

        new_universe = np.copy(self._universe)

        if self._dimensions == 1:
            padding = max((rule.window.shape[0] for rule in rules))
            old_universe = np.pad(self._universe, padding)
            for index in range(padding, self._size.size + padding):
                for rule in rules:
                    pass
        else:
            vertical_padding = max((rule.window.shape[0] for rule in rules))
            horizontal_padding = max((rule.window.shape[1] for rule in rules))


class Simulator:

    def __init__(self, universe: Universe, rule_list: RuleList):
        """

        :param universe:
        :param rule_list:
        """
        self._universe = universe
        self._rule_list = rule_list

    def step(self, num_steps: int = 1) -> None:
        """
        Go forward in the universe num_steps time steps
        :param num_steps: number of steps to advance the Universe
        :return: None
        """
