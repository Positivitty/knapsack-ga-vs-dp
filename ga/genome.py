from __future__ import annotations

import numpy as np

from common.item import Item


def random_population(rng: np.random.Generator, pop_size: int, n: int) -> np.ndarray:
    """Sample a random population of bitstrings, shape (pop_size, n) dtype uint8."""
    return rng.integers(0, 2, size=(pop_size, n), dtype=np.uint8)


def fitness(
    population: np.ndarray,
    weights: np.ndarray,
    values: np.ndarray,
    capacity: int,
) -> np.ndarray:
    """Vectorized fitness with death penalty for infeasible solutions.

    population: (P, n) uint8 bitstrings
    Returns: (P,) int array — sum of values if total weight <= capacity, else 0.
    """
    total_w = population @ weights
    total_v = population @ values
    feasible = total_w <= capacity
    return np.where(feasible, total_v, 0).astype(np.int64)


def decode(genome: np.ndarray) -> list[int]:
    """Convert a single bitstring into a sorted list of chosen indices."""
    return [int(i) for i in np.flatnonzero(genome)]


def items_to_arrays(items) -> tuple[np.ndarray, np.ndarray]:
    """Pack a sequence of Item into (weights, values) numpy arrays."""
    weights = np.array([it.weight for it in items], dtype=np.int64)
    values = np.array([it.value for it in items], dtype=np.int64)
    return weights, values
