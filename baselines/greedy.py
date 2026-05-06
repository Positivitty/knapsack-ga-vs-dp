from __future__ import annotations

import time
from typing import Sequence

from common.item import Item
from common.result import AlgorithmResult


def knapsack_greedy(items: Sequence[Item], capacity: int) -> AlgorithmResult:
    """Greedy by value/weight ratio. Heuristic — not optimal in general."""
    start = time.perf_counter()

    order = sorted(
        range(len(items)),
        key=lambda i: items[i].value / items[i].weight if items[i].weight else 0.0,
        reverse=True,
    )

    chosen: list[int] = []
    total_value = 0
    total_weight = 0
    for i in order:
        if total_weight + items[i].weight <= capacity:
            chosen.append(i)
            total_value += items[i].value
            total_weight += items[i].weight

    chosen.sort()
    runtime = time.perf_counter() - start

    return AlgorithmResult(
        algo="greedy",
        value=total_value,
        weight=total_weight,
        chosen=chosen,
        runtime_s=runtime,
    )
