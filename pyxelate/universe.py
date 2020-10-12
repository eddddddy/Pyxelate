from copy import copy
from typing import List, Tuple, Union, Iterator, Iterable


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

    def __init__(self, window: np.ndarray, center: Union[int, Tuple[int, ...]], becomes: int):
        """
        Create a single evolution rule
        :param window: matrix of dead (0) and alive (1) cells
        :param center: index of the target cell in the window
        :param becomes: what the target cell becomes in the next generation
        """
        if isinstance(center, int):
            center = (center,)
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

    def __init__(self, dimensions: int, size: Union[Size, None] = None, initial: Union[np.ndarray, None] = None):
        """
        Create a (initially static) universe with cells that can be either dead (0) or alive (1)
        :param dimensions: the dimensionality of the universe; can currently only
                           be 1 or 2
        :param size: the size of the universe; currently cannot be infinite, and does not
                     have to be provided if initial state is provided
        :param initial: the initial state of the universe; if not provided, then all
                        cells start off dead
        """
        Universe.__check_dimensions(dimensions)
        self._dimensions = dimensions

        if (size is None and initial is None) or (size is not None and initial is not None):
            raise ValueError("Exactly one of size or initial must be provided")

        if size is not None:
            if size.is_infinite():
                raise ValueError("Infinite universes not yet supported")

            self._size = size

            if dimensions == 1:
                self._universe = np.array([0] * size.size)
            elif dimensions == 2:
                self._universe = np.array([[0] * size.size for _ in range(size.size)])
        else:
            Universe.__check_initial(initial, dimensions)
            self._size = initial.shape[0]

            self._universe = np.copy(initial)

    @staticmethod
    def __check_dimensions(dimensions: int) -> None:
        if dimensions <= 0:
            raise ValueError("Universes must have at least one dimension")
        elif dimensions > 2:
            raise ValueError("Higher than two-dimensional universe not supported")

    @staticmethod
    def __check_initial(initial: np.ndarray, dimensions: int) -> None:
        if len(initial.shape) != dimensions:
            raise ValueError("Initial universe must have the same number of dimensions provided")
        size = initial.shape[0]
        if not np.all(initial.shape == size):
            raise ValueError("Initial universe must have the same size across all dimensions")

    def __repr__(self) -> str:
        if self._dimensions == 1:
            return ''.join(map(str, self._universe))
        else:
            return '\n'.join([''.join(map(str, row)) for row in self._universe])

    def transform(self, location: Union[int, Tuple[int, ...], Iterable[int], Iterable[Tuple[int, ...]]], state: int) -> None:
        """
        Change the cell at the specified location(s) to the specified state
        :param location: position of the cell to transform; if an iterable, then transform
                         all cells in the iterable
        :param state: new state of the cell
        :return: None
        """
        if isinstance(location, int) or isinstance(location, tuple):
            if isinstance(location, int):
                location = (location,)
            if len(location) != self._dimensions:
                raise ValueError("Location must have the same number of dimensions as the universe")

            self._universe[location] = state
        else:
            for loc in location:
                if isinstance(loc, int):
                    loc = (loc,)
                if len(loc) != self._dimensions:
                    raise ValueError("Location must have the same number of dimensions as the universe")

                self._universe[loc] = state

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
                    center = rule.center[0]
                    if np.all(old_universe[index - center:index - center + rule.window.shape[0]] == rule.window):
                        new_universe[index - padding] = rule.becomes
                        break
        else:
            vertical_padding = max((rule.window.shape[0] for rule in rules))
            horizontal_padding = max((rule.window.shape[1] for rule in rules))
            old_universe = np.pad(self._universe, ((vertical_padding, vertical_padding), (horizontal_padding, horizontal_padding)))
            for row_index in range(vertical_padding, self._size.size + vertical_padding):
                for col_index in range(horizontal_padding, self._size.size + vertical_padding):
                    for rule in rules:
                        vertical_center, horizontal_center = rule.center
                        if np.all(old_universe[
                                  row_index - vertical_center:row_index - vertical_center + rule.window.shape[0],
                                  col_index - horizontal_center:col_index - horizontal_center + rule.window.shape[1]
                                  ] == rule.window):
                            new_universe[row_index - vertical_padding, col_index - horizontal_padding] = rule.becomes

        self._universe = new_universe


class Simulator:

    def __init__(self, universe: Universe, rule_list: RuleList):
        """
        Create a Simulator starting with the given Universe and RuleList
        :param universe: the universe to start with
        :param rule_list: the rules to evolve the universe
        """
        self._universe = universe
        self._rule_list = rule_list

    def step(self, num_steps: int = 1) -> None:
        """
        Go forward in the universe num_steps time steps
        :param num_steps: number of steps to advance the Universe
        :return: None
        """
        for _ in range(num_steps):
            self._universe.apply(self._rule_list)

    def print_universe(self) -> None:
        """
        Print the current universe
        :return: None
        """
        print(f"{self._universe}\n")
