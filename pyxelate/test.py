from typing import List, Tuple, Union


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


class Universe:

    def __init__(self, dimensions: int, size: Size):
        self._dimensions = dimensions
        self._size = size

        if dimensions == 1:
            if not size.is_infinite():
                self._universe = np.array([0] * size.size)
            else:
                self._universe = np.array([0])
        elif dimensions == 2:
            if not size.is_infinite():
                self._universe = np.array([[0] * size.size for _ in range(size.size)])
            else:
                self._universe = np.array([[0]])
        else:
            raise ValueError("Higher than 2-D universes not supported")

    def __repr__(self) -> str:
        if self._dimensions == 1:
            return ''.join(map(str, self._universe))
        else:
            print('\n'.join([''.join(map(str, row)) for row in self._universe]))


class Rule:

    def __init__(self, window: np.ndarray, center: Tuple[int, ...], becomes: Union[0, 1]):
        """
        Create a single evolution rule
        :param window: matrix of dead (0) and alive (1) cells
        :param center: index of the target cell in the window
        :param becomes: what the target cell becomes in the next generation
        """
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


class Simulator:

    def __init__(self, universe: Universe, rule_list: RuleList):
        """

        :param universe:
        :param rule_list:
        """
