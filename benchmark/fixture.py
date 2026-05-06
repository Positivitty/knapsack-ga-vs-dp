from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from baselines.greedy import knapsack_greedy
from benchmark.generate import generate_instance
from dp.knapsack_dp import knapsack_dp
from ga.algorithm import GAConfig, knapsack_ga


@dataclass
class BenchmarkRow:
    size: int
    trial: int
    algo: str
    value: int
    optimal_value: int
    quality_pct: float
    runtime_s: float
    generations_used: int


def run_sweep(
    sizes: Iterable[int],
    trials: int,
    base_seed: int = 42,
    ga_config: GAConfig | None = None,
) -> List[BenchmarkRow]:
    rows: List[BenchmarkRow] = []
    for size in sizes:
        for trial in range(trials):
            instance_seed = base_seed + 1000 * size + trial
            items, capacity = generate_instance(size, seed=instance_seed)

            dp_res = knapsack_dp(items, capacity)
            optimal = dp_res.value

            greedy_res = knapsack_greedy(items, capacity)

            cfg = ga_config or GAConfig()
            cfg = GAConfig(**{**cfg.__dict__, "seed": instance_seed})
            ga_res = knapsack_ga(items, capacity, config=cfg)

            for res in (ga_res, dp_res, greedy_res):
                quality = 100.0 * res.value / optimal if optimal > 0 else 100.0
                rows.append(
                    BenchmarkRow(
                        size=size,
                        trial=trial,
                        algo=res.algo,
                        value=res.value,
                        optimal_value=optimal,
                        quality_pct=quality,
                        runtime_s=res.runtime_s,
                        generations_used=res.generations_used,
                    )
                )
    return rows


def write_csv(rows: List[BenchmarkRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "size",
                "trial",
                "algo",
                "value",
                "optimal_value",
                "quality_pct",
                "runtime_s",
                "generations_used",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    r.size,
                    r.trial,
                    r.algo,
                    r.value,
                    r.optimal_value,
                    f"{r.quality_pct:.4f}",
                    f"{r.runtime_s:.6f}",
                    r.generations_used,
                ]
            )
