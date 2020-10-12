from itertools import permutations

import numpy as np

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pyxelate import Size, Rule, RuleList, Universe, Simulator


def get_life_rule_list() -> RuleList:
    from itertools import chain, combinations

    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    life = RuleList()

    states = []
    for subset in powerset(range(9)):
        state = np.zeros(9)
        for i in subset:
            state[i] = 1
        states.append(state.reshape(3, 3))

    for state in states:
        is_cell_alive = state[1, 1] == 1
        num_alive_neighbours = np.sum(state) - int(is_cell_alive)
        if is_cell_alive and num_alive_neighbours < 2:
            life.add_rule(Rule(state, (1, 1), 0))
        elif is_cell_alive and num_alive_neighbours > 3:
            life.add_rule(Rule(state, (1, 1), 0))
        elif not is_cell_alive and num_alive_neighbours == 3:
            life.add_rule(Rule(state, (1, 1), 1))

    return life


def life_sim(size: int = 20) -> None:
    life_rules = get_life_rule_list()
    universe = Universe(dimensions=2, size=Size(size))
    universe.transform([(2, 1), (3, 2), (1, 3), (2, 3), (3, 3)], state=1)

    simulator = Simulator(universe, life_rules)

    simulator.print_universe()
    for _ in range(10):
        simulator.step()
        simulator.print_universe()


if __name__ == '__main__':
    life_sim()
