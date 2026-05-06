from baselines.greedy import knapsack_greedy
from common.item import Item


def test_greedy_picks_best_ratio_first():
    items = [Item(10, 10), Item(1, 5)]  # ratios 1.0 vs 5.0
    res = knapsack_greedy(items, capacity=10)
    # greedy picks index 1 first (ratio 5), then can't fit index 0 (weight 10 > 9 left)
    assert res.chosen == [1]
    assert res.value == 5


def test_greedy_respects_capacity():
    items = [Item(5, 10), Item(5, 10), Item(5, 10)]
    res = knapsack_greedy(items, capacity=12)
    assert res.weight <= 12
    assert len(res.chosen) == 2


def test_greedy_can_be_suboptimal():
    # classic suboptimal-greedy instance: high ratio item blocks the optimum
    items = [Item(1, 2), Item(5, 9), Item(5, 9)]  # ratios: 2.0, 1.8, 1.8
    res = knapsack_greedy(items, capacity=10)
    # greedy: takes ratio-2.0 item (value 2), then one ratio-1.8 item (value 9) → 11
    # optimum: take both ratio-1.8 items (value 18)
    assert res.value == 11
