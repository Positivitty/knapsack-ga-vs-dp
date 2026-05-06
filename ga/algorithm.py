from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from common.item import Item
from common.result import AlgorithmResult
from ga.genome import decode, fitness, items_to_arrays, random_population
from ga.operators import bitflip_mutate, tournament_select, uniform_crossover


@dataclass
class GAConfig:
    pop_size: int = 100
    generations: int = 500
    tournament_k: int = 3
    p_crossover: float = 0.7
    p_mutate: float | None = None  # default 1/n
    elitism: int = 2
    stagnation_limit: int = 100
    seed: int | None = None


def knapsack_ga(
    items: Sequence[Item],
    capacity: int,
    config: GAConfig | None = None,
) -> AlgorithmResult:
    cfg = config or GAConfig()
    n = len(items)
    p_mutate = cfg.p_mutate if cfg.p_mutate is not None else 1.0 / n

    rng = np.random.default_rng(cfg.seed)
    weights, values = items_to_arrays(items)

    start = time.perf_counter()
    population = random_population(rng, cfg.pop_size, n)
    fits = fitness(population, weights, values, capacity)

    best_idx = int(fits.argmax())
    best_genome = population[best_idx].copy()
    best_value = int(fits[best_idx])
    stagnant = 0
    gens_used = 0

    for gen in range(1, cfg.generations + 1):
        gens_used = gen
        elite_idx = np.argsort(fits)[-cfg.elitism:]
        elites = population[elite_idx].copy()

        n_offspring = cfg.pop_size - cfg.elitism
        # ensure even number of parents for paired crossover
        n_parents = n_offspring + (n_offspring % 2)
        parents = tournament_select(rng, population, fits, n_parents, k=cfg.tournament_k)
        children = uniform_crossover(rng, parents, p_crossover=cfg.p_crossover)
        children = bitflip_mutate(rng, children, p_mutate=p_mutate)
        children = children[:n_offspring]

        population = np.vstack([elites, children])
        fits = fitness(population, weights, values, capacity)

        gen_best = int(fits.max())
        if gen_best > best_value:
            best_value = gen_best
            best_genome = population[int(fits.argmax())].copy()
            stagnant = 0
        else:
            stagnant += 1
            if stagnant >= cfg.stagnation_limit:
                break

    chosen = decode(best_genome)
    total_weight = int(sum(items[i].weight for i in chosen))
    runtime = time.perf_counter() - start

    return AlgorithmResult(
        algo="ga",
        value=best_value,
        weight=total_weight,
        chosen=chosen,
        runtime_s=runtime,
        generations_used=gens_used,
        extra={
            "pop_size": cfg.pop_size,
            "p_crossover": cfg.p_crossover,
            "p_mutate": p_mutate,
            "tournament_k": cfg.tournament_k,
            "elitism": cfg.elitism,
            "stagnation_limit": cfg.stagnation_limit,
        },
    )
