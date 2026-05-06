from itertools import product

from common.item import Item
from dp.knapsack_dp import knapsack_dp


def _brute_force(items, capacity):
    n = len(items)
    best = 0
    for mask in product([0, 1], repeat=n):
        w = sum(items[i].weight for i in range(n) if mask[i])
        v = sum(items[i].value for i in range(n) if mask[i])
        if w <= capacity and v > best:
            best = v
    return best


def test_dp_textbook_example():
    items = [Item(2, 3), Item(3, 4), Item(4, 5), Item(5, 6)]
    res = knapsack_dp(items, capacity=5)
    assert res.value == 7  # take items 0 and 1
    assert res.weight == 5
    assert sorted(res.chosen) == [0, 1]


def test_dp_matches_brute_force_small():
    import random

    rng = random.Random(0)
    for trial in range(10):
        n = rng.randint(3, 12)
        items = [Item(rng.randint(1, 20), rng.randint(1, 20)) for _ in range(n)]
        cap = rng.randint(5, sum(it.weight for it in items))
        assert knapsack_dp(items, cap).value == _brute_force(items, cap)


def test_dp_zero_capacity():
    items = [Item(1, 10), Item(2, 20)]
    res = knapsack_dp(items, capacity=0)
    assert res.value == 0
    assert res.chosen == []


def test_dp_chosen_indices_consistent_with_value():
    items = [Item(2, 3), Item(3, 4), Item(4, 5), Item(5, 6)]
    res = knapsack_dp(items, capacity=10)
    assert sum(items[i].value for i in res.chosen) == res.value
    assert sum(items[i].weight for i in res.chosen) == res.weight
    assert res.weight <= 10
