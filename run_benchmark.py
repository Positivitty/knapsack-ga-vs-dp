from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
from pathlib import Path

from tabulate import tabulate

from benchmark.fixture import BenchmarkRow, run_sweep, write_csv
from benchmark.plot import plot_quality, plot_runtime
from ga.algorithm import GAConfig


def _parse_sizes(value: str) -> list[int]:
    return [int(s) for s in value.split(",") if s.strip()]


def _summary_table(rows: list[BenchmarkRow]) -> str:
    by_key: dict[tuple[int, str], list[BenchmarkRow]] = defaultdict(list)
    for r in rows:
        by_key[(r.size, r.algo)].append(r)

    headers = ["size", "algo", "mean_value", "mean_quality_pct", "mean_runtime_s", "mean_gens"]
    table = []
    for (size, algo), group in sorted(by_key.items()):
        mean_v = sum(r.value for r in group) / len(group)
        mean_q = sum(r.quality_pct for r in group) / len(group)
        mean_rt = sum(r.runtime_s for r in group) / len(group)
        mean_g = sum(r.generations_used for r in group) / len(group)
        table.append(
            [
                size,
                algo,
                f"{mean_v:.1f}",
                f"{mean_q:.2f}",
                f"{mean_rt:.4f}",
                f"{mean_g:.1f}" if algo == "ga" else "-",
            ]
        )
    return tabulate(table, headers=headers, tablefmt="github")


def main() -> None:
    parser = argparse.ArgumentParser(description="GA vs DP knapsack benchmark sweep")
    parser.add_argument(
        "--sizes",
        type=_parse_sizes,
        default=[20, 50, 100, 200, 500],
        help="Comma-separated item counts",
    )
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pop-size", type=int, default=100)
    parser.add_argument("--generations", type=int, default=500)
    parser.add_argument("--stagnation-limit", type=int, default=100)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results") / f"benchmark_{date.today().isoformat()}.csv",
    )
    args = parser.parse_args()

    cfg = GAConfig(
        pop_size=args.pop_size,
        generations=args.generations,
        stagnation_limit=args.stagnation_limit,
    )

    print(f"Running sweep: sizes={args.sizes}, trials={args.trials}, seed={args.seed}")
    rows = run_sweep(args.sizes, args.trials, base_seed=args.seed, ga_config=cfg)

    write_csv(rows, args.out)
    print(f"\nWrote {args.out}")

    runtime_png = args.out.with_name("runtime_vs_size.png")
    quality_png = args.out.with_name("quality_vs_size.png")
    plot_runtime(rows, runtime_png)
    plot_quality(rows, quality_png)
    print(f"Wrote {runtime_png}")
    print(f"Wrote {quality_png}")

    print("\n" + _summary_table(rows))


if __name__ == "__main__":
    main()
