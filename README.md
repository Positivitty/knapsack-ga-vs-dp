# Knapsack: GA vs DP

Genetic Algorithm vs. Dynamic Programming on the 0/1 Knapsack Problem. A greedy value/weight-ratio heuristic rides along as a third baseline for context.

This is the final-project comparison for SWOSU's algorithms class — a reflection on the trade-off between **exact** and **approximate** approaches to an NP-hard problem.

## The Problem

Given `n` items, each with a weight and a value, and a knapsack with capacity `W`, select a subset of items that maximizes total value while keeping total weight ≤ `W`. Each item is either fully taken or left behind (0/1, not fractional).

The 0/1 Knapsack Problem is **NP-hard**. There's no known polynomial-time exact algorithm in `n` and `W` together — DP solves it in `O(n·W)` which is *pseudo-polynomial* (linear in the numeric value of `W`, exponential in the number of bits needed to encode it). For large `W`, exact solving becomes painful, and approximate methods earn their keep.

## The Two Algorithms

### Genetic Algorithm

A population-based metaheuristic inspired by natural selection. Candidate solutions are encoded as bitstrings; "fit" individuals are more likely to reproduce; offspring are mixed (crossover) and randomly perturbed (mutation). Over generations the population concentrates on high-quality regions of the search space without ever enumerating it.

This implementation:

- **Representation:** length-`n` bitstring; bit `i` is 1 iff item `i` is selected (`numpy.uint8` arrays for vectorized fitness).
- **Fitness:** sum of selected values if the chromosome is feasible (total weight ≤ `W`); **zero** if infeasible. This "death penalty" is the simplest way to keep the GA inside the feasible region — overweight chromosomes have no offspring.
- **Selection:** **tournament selection**, k=3. Three random individuals fight; the fittest wins a slot in the parent pool. Tournament selection is robust to fitness scaling and easy to implement.
- **Crossover:** **uniform crossover**, p=0.7. For each bit, flip a coin: child A inherits from parent A or parent B; child B gets the other. Uniform crossover mixes more aggressively than single-point on bitstrings, which matters because nearby bits in our genome are *not* correlated (item ordering is arbitrary).
- **Mutation:** independent **bit-flip** at rate `p = 1/n`. The classical default. On average, each child mutates one bit.
- **Elitism:** the top **2** individuals are copied unchanged into the next generation. Elitism guarantees the best-so-far never regresses.
- **Termination:** **500 generations** maximum, with **early stopping** if the global best hasn't improved in 100 generations.

### Dynamic Programming

The textbook exact solver. Build a table `T[i][w]` where each cell holds the best achievable value using only the first `i` items with capacity `w`. The recurrence:

```
T[i][w] = T[i-1][w]                                    if items[i-1].weight > w
        = max(T[i-1][w], T[i-1][w - w_i] + v_i)        otherwise
```

The optimum is `T[n][W]`. Backtracking through the table reconstructs which items were chosen. DP is **provably optimal** — its result is the ground truth against which we measure GA quality.

### Greedy (baseline)

Sort items by value/weight ratio descending, take items in that order while they still fit. Fast and often surprisingly good, but **arbitrarily bad in the worst case** — a small high-ratio item can block much better solutions.

## Complexity

| | GA | DP | Greedy |
|---|---|---|---|
| Time | `O(G · P · n)` | `O(n · W)` | `O(n log n)` |
| Space | `O(P · n)` | `O(n · W)` | `O(n)` |
| Optimality | Approximate (no guarantee) | Exact | Heuristic, no bound |

`G` = generations, `P` = population size, `W` = capacity (numeric value, not bits). DP's `O(n·W)` looks polynomial but is pseudo-polynomial — if you double the capacity values, runtime doubles. GA's runtime is independent of `W` entirely; only `n` (and your hyperparameters) matter.

## Predicted Winner (before running)

- **DP wins on small `n` and small `W`** — exact, fast, simple.
- **GA crosses over DP at large `n`** because GA scales `O(G·P·n)` while DP scales `O(n·W)`, and `W` here grows with `n` (capacity = 0.5 × Σ weights). Once `W` is large enough, DP's pseudo-polynomial blowup beats GA's roughly linear growth.
- **Greedy is essentially free** and competitive on uniformly random instances, but the gap to optimum is unbounded in the worst case.

I expected GA to land 95–99% of optimum and to overtake DP somewhere in the n=500–1000 range. Greedy I expected to be in the 90s on quality.

## Running It

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Full default sweep: n ∈ {20, 50, 100, 200, 500}, 5 trials each
python run_benchmark.py

# Quick sanity run
python run_benchmark.py --sizes 20,50 --trials 2
```

Outputs land in `results/`:
- `benchmark_YYYY-MM-DD.csv` — raw per-run data
- `runtime_vs_size.png` — mean runtime vs `n`, log scale
- `quality_vs_size.png` — solution quality (% of optimum) vs `n`

## Tests

```bash
python -m pytest -q
```

28 tests covering: DP correctness vs brute force on small instances, GA always returns feasible solutions, GA ≤ DP optimum, operator behavior at edge cases (`p=0` and `p=1`), instance generator determinism, benchmark fixture row counts.

## Results

Default sweep, 5 trials per size, seed = 42:

| size | algo   | mean value | quality vs DP | mean runtime (s) | mean GA gens |
|-----:|--------|-----------:|--------------:|-----------------:|-------------:|
|   20 | DP     |      831.4 |       100.00% |           0.0011 | —            |
|   20 | GA     |      831.4 |       100.00% |           0.0265 | 113.4        |
|   20 | greedy |      826.4 |        99.38% |           0.0000 | —            |
|   50 | DP     |     2042.0 |       100.00% |           0.0078 | —            |
|   50 | GA     |     2042.0 |       100.00% |           0.0405 | 162.4        |
|   50 | greedy |     2040.4 |        99.93% |           0.0000 | —            |
|  100 | DP     |     4032.8 |       100.00% |           0.0310 | —            |
|  100 | GA     |     4021.2 |        99.72% |           0.0660 | 233.0        |
|  100 | greedy |     4028.4 |        99.89% |           0.0000 | —            |
|  200 | DP     |     8136.0 |       100.00% |           0.1402 | —            |
|  200 | GA     |     8104.4 |        99.61% |           0.1372 | 366.6        |
|  200 | greedy |     8129.8 |        99.92% |           0.0001 | —            |
|  500 | DP     |    20080.2 |       100.00% |           0.8360 | —            |
|  500 | GA     |    19959.6 |        99.40% |           0.3120 | 500.0        |
|  500 | greedy |    20075.8 |        99.98% |           0.0002 | —            |

![Runtime vs size](results/runtime_vs_size.png)

![Quality vs size](results/quality_vs_size.png)

## Analysis

**Runtime** matches the predicted shape. DP grows aggressively — `0.001s → 0.836s` is roughly an **800× slowdown** for a 25× size increase, because both `n` and `W` are growing. GA grows much more gently — `0.027s → 0.312s`, about **12×**. The two curves cross between n=200 (essentially tied) and n=500, where GA finishes in ~37% of DP's time. The crossover point is exactly the inflection where GA stops being "the slow approximate option" and starts being the practical choice.

**Quality** also matches expectations *qualitatively* — GA finds the optimum exactly on small instances (n ≤ 50), then drifts down to 99.4% by n=500 as the search space outgrows what 100 individuals × 500 generations can fully explore. The honest surprise is **greedy**, which beats GA on quality from n=100 onward and only loses ~0.02% to DP at n=500. This is not a flaw in the GA — it's a property of the instance distribution. With weights and values both drawn IID uniform on `[1, 100]` and capacity at half total weight, value/weight ratios are well-spread and the greedy heuristic happens to make near-optimal decisions. On adversarial instances (correlated weights and values, or pathological capacity ratios) greedy can be arbitrarily bad while GA stays competitive — that's a known result, but this benchmark didn't construct such instances.

**Memory** is the unsung axis. DP allocates an `(n+1) × (W+1)` table — for n=500 that's roughly `500 × 25,000 = 12.5M` integer cells. GA holds `100 × 500 = 50,000` bits. **GA uses ~0.4% of DP's memory** at this scale and the ratio gets dramatically worse for DP as `W` grows. If we'd pushed to instances with `W` in the millions, DP would have OOMed long before GA blinked.

**Why the GA wasn't tuned harder.** The hyperparameters (pop=100, gens=500, p_xover=0.7, p_mut=1/n, tournament k=3) are textbook defaults. They weren't search-tuned for this problem. A grid-searched GA could likely match greedy's quality on these instances — the point of this comparison is to show GA's *out-of-the-box* behavior versus DP's deterministic optimum, not to win a tuning competition.

## Conclusion

For 0/1 Knapsack on these instances:

- **Use DP** when `n · W` is small enough to fit comfortably in memory and you need the proven optimum. It's simple, deterministic, and unbeatable when it's tractable.
- **Use GA** when `W` is large (memory pressure or runtime blowup makes DP impractical) and you can tolerate ~99% of optimum. GA's runtime is `W`-independent — it scales with `n` and your hyperparameter budget, full stop.
- **Use greedy** when "fast and probably fine" is the spec. On uniform-random instances it's almost free and almost optimal. Don't trust it on adversarial inputs.

The deeper lesson is that "best algorithm" is not a property of a problem in isolation — it's a property of (problem, instance distribution, resource budget, quality tolerance). DP is unambiguously *correct*; GA is unambiguously *flexible*; greedy is unambiguously *fast*. The right tool depends on which of those three matters most in the moment.
