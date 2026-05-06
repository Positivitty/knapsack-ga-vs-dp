#!/usr/bin/env bash
# Demo script for the video. Press any key to advance between sections.
# Run from the project root with the venv already activated.

set -e

pause() {
    echo
    echo
    read -n 1 -s -r -p "▶ press any key to continue"
    echo
}

section() {
    clear
    echo "═══════════════════════════════════════════════════════════════════"
    echo " $1"
    echo "═══════════════════════════════════════════════════════════════════"
    echo
}

# ─── 1. Banner ────────────────────────────────────────────────────────
clear
cat <<'BANNER'

  ╔═══════════════════════════════════════════════════════════════╗
  ║                                                               ║
  ║         KNAPSACK: GENETIC ALGORITHM vs DYNAMIC PROGRAMMING    ║
  ║                                                               ║
  ║         Final Reflection — Algorithms                         ║
  ║         Noah Kerr                                             ║
  ║         github.com/Positivitty/knapsack-ga-vs-dp              ║
  ║                                                               ║
  ╚═══════════════════════════════════════════════════════════════╝

BANNER
pause

# ─── 2. Problem statement ─────────────────────────────────────────────
section "THE PROBLEM — 0/1 Knapsack"
cat <<'PROBLEM'
  Given n items, each with a weight and a value, and a knapsack with
  capacity W, pick a subset of items that maximizes total value while
  keeping total weight ≤ W. Each item is either fully taken or left
  behind (0/1 — not fractional).

  Why it matters:

    • Canonical NP-hard problem
    • Models cargo loading, budget allocation, resource scheduling
    • DP solves it in O(n · W) — pseudo-polynomial, not true poly
    • Perfect arena to compare an EXACT solver against an APPROXIMATE one

PROBLEM
pause

# ─── 3. GA — main loop ────────────────────────────────────────────────
section "ALGORITHM 1 — Genetic Algorithm  ·  ga/algorithm.py"
cat ga/algorithm.py
pause

# ─── 4. GA — operators ────────────────────────────────────────────────
section "GA Operators — selection / crossover / mutation  ·  ga/operators.py"
cat ga/operators.py
pause

# ─── 5. GA — fitness ──────────────────────────────────────────────────
section "GA Fitness — vectorized, with death penalty for infeasible  ·  ga/genome.py"
cat ga/genome.py
pause

# ─── 6. DP ────────────────────────────────────────────────────────────
section "ALGORITHM 2 — Dynamic Programming  ·  dp/knapsack_dp.py"
cat dp/knapsack_dp.py
pause

# ─── 7. Tests ─────────────────────────────────────────────────────────
section "TEST SUITE — 28 tests, including DP-vs-brute-force correctness"
python -m pytest -v
pause

# ─── 8. Benchmark ─────────────────────────────────────────────────────
section "BENCHMARK SWEEP — n ∈ {20, 50, 100, 200, 500}, 5 trials each"
python run_benchmark.py
pause

# ─── 9. Outro ─────────────────────────────────────────────────────────
section "RESULTS"
cat <<'OUTRO'
  Headline:

    • At n=20:  DP wins   (0.001s vs GA 0.027s, both find optimum)
    • At n=200: tied      (~0.14s each)
    • At n=500: GA wins   (0.31s vs DP 0.84s, GA at 99.4% of optimum)

  GA crosses DP between n=200 and n=500 — and uses ~0.4% of DP's
  memory at n=500.

  Plots and CSV:

    results/runtime_vs_size.png
    results/quality_vs_size.png
    results/benchmark_*.csv

  Full report:

    README.md  (also rendered at github.com/Positivitty/knapsack-ga-vs-dp)

OUTRO
pause
clear
