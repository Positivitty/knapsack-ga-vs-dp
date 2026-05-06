from __future__ import annotations

import random
from typing import List, Tuple

from common.item import Item


def generate_instance(
    n: int,
    seed: int,
    weight_range: Tuple[int, int] = (1, 100),
    value_range: Tuple[int, int] = (1, 100),
    capacity_ratio: float = 0.5,
) -> Tuple[List[Item], int]:
    """Generate a reproducible knapsack instance.

    Capacity = capacity_ratio * sum(weights). Default 0.5 yields
    medium-tightness instances (the regime where 0/1 knapsack is hardest
    in practice).
    """
    rng = random.Random(seed)
    items = [
        Item(
            weight=rng.randint(*weight_range),
            value=rng.randint(*value_range),
        )
        for _ in range(n)
    ]
    capacity = int(capacity_ratio * sum(it.weight for it in items))
    return items, capacity
