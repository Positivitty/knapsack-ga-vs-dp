from __future__ import annotations

import numpy as np


def tournament_select(
    rng: np.random.Generator,
    population: np.ndarray,
    fitnesses: np.ndarray,
    n_parents: int,
    k: int = 3,
) -> np.ndarray:
    """Tournament selection with replacement. Returns (n_parents, n) parent array."""
    pop_size = population.shape[0]
    contenders = rng.integers(0, pop_size, size=(n_parents, k))
    contender_fitness = fitnesses[contenders]
    winners = contenders[np.arange(n_parents), contender_fitness.argmax(axis=1)]
    return population[winners]


def uniform_crossover(
    rng: np.random.Generator,
    parents: np.ndarray,
    p_crossover: float = 0.7,
) -> np.ndarray:
    """Pair adjacent parents; with prob p_crossover do uniform crossover, else copy."""
    n_parents, n = parents.shape
    assert n_parents % 2 == 0, "need even number of parents"
    children = parents.copy()
    for i in range(0, n_parents, 2):
        if rng.random() < p_crossover:
            mask = rng.integers(0, 2, size=n, dtype=np.uint8)
            children[i] = np.where(mask, parents[i], parents[i + 1])
            children[i + 1] = np.where(mask, parents[i + 1], parents[i])
    return children


def bitflip_mutate(
    rng: np.random.Generator,
    population: np.ndarray,
    p_mutate: float,
) -> np.ndarray:
    """Flip each bit independently with probability p_mutate."""
    flips = rng.random(size=population.shape) < p_mutate
    return np.where(flips, 1 - population, population).astype(np.uint8)
