from __future__ import annotations

import time
from typing import Sequence

from common.item import Item
from common.result import AlgorithmResult


def knapsack_dp(items: Sequence[Item], capacity: int) -> AlgorithmResult:
    """Solve 0/1 Knapsack exactly via O(n*W) tabulation.

    Returns the optimal value, total weight, and the indices chosen.
    """
    start = time.perf_counter()

    n = len(items)
    # table[i][w] = best value using first i items with capacity w
    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wi = items[i - 1].weight
        vi = items[i - 1].value
        row = table[i]
        prev = table[i - 1]
        for w in range(capacity + 1):
            if wi <= w:
                row[w] = max(prev[w], prev[w - wi] + vi)
            else:
                row[w] = prev[w]

    chosen: list[int] = []
    w = capacity
    for i in range(n, 0, -1):
        if table[i][w] != table[i - 1][w]:
            chosen.append(i - 1)
            w -= items[i - 1].weight
    chosen.reverse()

    total_value = table[n][capacity]
    total_weight = sum(items[i].weight for i in chosen)
    runtime = time.perf_counter() - start

    return AlgorithmResult(
        algo="dp",
        value=total_value,
        weight=total_weight,
        chosen=chosen,
        runtime_s=runtime,
    )
