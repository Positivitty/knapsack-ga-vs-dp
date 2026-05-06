import random

from common.item import Item
from ga.algorithm import GAConfig, knapsack_ga


def test_ga_returns_feasible():
    items = [Item(2, 3), Item(3, 4), Item(4, 5), Item(5, 6)]
    res = knapsack_ga(items, capacity=5, config=GAConfig(seed=0, generations=50))
    assert res.weight <= 5
    assert res.value == sum(items[i].value for i in res.chosen)


def test_ga_finds_optimum_on_textbook():
    # textbook 4-item instance, optimum = 7 (take items 0 and 1)
    items = [Item(2, 3), Item(3, 4), Item(4, 5), Item(5, 6)]
    res = knapsack_ga(items, capacity=5, config=GAConfig(seed=0))
    assert res.value == 7


def test_ga_always_feasible_random_instances():
    rng = random.Random(0)
    for trial in range(5):
        n = rng.randint(10, 30)
        items = [Item(rng.randint(1, 20), rng.randint(1, 20)) for _ in range(n)]
        cap = rng.randint(10, sum(it.weight for it in items) // 2)
        res = knapsack_ga(items, cap, config=GAConfig(seed=trial, generations=100))
        assert res.weight <= cap


def test_ga_records_generations_used():
    items = [Item(2, 3), Item(3, 4), Item(4, 5), Item(5, 6)]
    res = knapsack_ga(
        items,
        capacity=5,
        config=GAConfig(seed=0, generations=200, stagnation_limit=10),
    )
    assert res.generations_used > 0
    assert res.generations_used <= 200
