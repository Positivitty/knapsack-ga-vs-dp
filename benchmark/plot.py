from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from benchmark.fixture import BenchmarkRow


_ALGOS = ("ga", "dp", "greedy")
_LABELS = {"ga": "GA", "dp": "DP (optimal)", "greedy": "Greedy"}
_MARKERS = {"ga": "o", "dp": "s", "greedy": "^"}


def _aggregate(rows: List[BenchmarkRow]):
    """Returns dict[algo][size] -> (mean_runtime, mean_quality)."""
    buckets = defaultdict(lambda: defaultdict(list))
    for r in rows:
        buckets[r.algo][r.size].append(r)
    out = {}
    for algo, by_size in buckets.items():
        out[algo] = {}
        for size, group in by_size.items():
            mean_rt = sum(r.runtime_s for r in group) / len(group)
            mean_q = sum(r.quality_pct for r in group) / len(group)
            out[algo][size] = (mean_rt, mean_q)
    return out


def plot_runtime(rows: List[BenchmarkRow], path: Path) -> None:
    agg = _aggregate(rows)
    fig, ax = plt.subplots(figsize=(8, 5))
    for algo in _ALGOS:
        if algo not in agg:
            continue
        sizes = sorted(agg[algo].keys())
        runtimes = [agg[algo][s][0] for s in sizes]
        ax.plot(sizes, runtimes, marker=_MARKERS[algo], label=_LABELS[algo])
    ax.set_xlabel("Number of items (n)")
    ax.set_ylabel("Mean runtime (seconds, log scale)")
    ax.set_yscale("log")
    ax.set_title("Runtime vs. instance size")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_quality(rows: List[BenchmarkRow], path: Path) -> None:
    agg = _aggregate(rows)
    fig, ax = plt.subplots(figsize=(8, 5))
    for algo in _ALGOS:
        if algo not in agg:
            continue
        sizes = sorted(agg[algo].keys())
        quality = [agg[algo][s][1] for s in sizes]
        ax.plot(sizes, quality, marker=_MARKERS[algo], label=_LABELS[algo])
    ax.set_xlabel("Number of items (n)")
    ax.set_ylabel("Solution quality (% of optimum)")
    ax.set_ylim(0, 105)
    ax.set_title("Solution quality vs. instance size")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
