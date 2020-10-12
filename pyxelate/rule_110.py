import numpy as np

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pyxelate import Size, Rule, RuleList, Universe, Simulator


def rule_110_sim(size: int = 50) -> None:
    rule_110 = RuleList()
    rule_110.add_rule(Rule(np.array([0, 0, 1]), 1, becomes=1))
    rule_110.add_rule(Rule(np.array([1, 0, 1]), 1, becomes=1))
    rule_110.add_rule(Rule(np.array([1, 1, 1]), 1, becomes=0))

    universe = Universe(dimensions=1, size=Size(size))
    universe.transform([10, 12, 13, 14, 16, 17, 20, 22, 24, 25, 27, 30, 32], state=1)

    simulator = Simulator(universe, rule_110)

    simulator.print_universe()
    for _ in range(10):
        simulator.step()
        simulator.print_universe()


if __name__ == '__main__':
    rule_110_sim()
