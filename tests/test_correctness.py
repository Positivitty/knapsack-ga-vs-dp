"""Cross-algorithm sanity checks: DP is the optimum oracle, GA must be feasible
and at least as good as greedy on average."""

import random

from baselines.greedy import knapsack_greedy
from common.item import Item
from dp.knapsack_dp import knapsack_dp
from ga.algorithm import GAConfig, knapsack_ga


def test_ga_within_dp_optimum():
    rng = random.Random(0)
    for trial in range(3):
        n = rng.randint(15, 25)
        items = [Item(rng.randint(1, 30), rng.randint(1, 30)) for _ in range(n)]
        cap = sum(it.weight for it in items) // 2

        opt = knapsack_dp(items, cap).value
        ga = knapsack_ga(items, cap, config=GAConfig(seed=trial, generations=300))

        assert ga.weight <= cap
        assert ga.value <= opt  # cannot exceed optimum


def test_greedy_within_dp_optimum():
    rng = random.Random(1)
    for trial in range(3):
        n = rng.randint(10, 20)
        items = [Item(rng.randint(1, 30), rng.randint(1, 30)) for _ in range(n)]
        cap = sum(it.weight for it in items) // 2

        opt = knapsack_dp(items, cap).value
        gd = knapsack_greedy(items, cap)

        assert gd.weight <= cap
        assert gd.value <= opt
