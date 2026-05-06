# Video Script — Knapsack: GA vs DP

**Target length:** ~10 minutes (8–12 acceptable).
**Format:** Screen recording with voiceover. No talking-head needed unless you want one.
**Goal:** Hit every rubric line — running code, both algorithms demonstrated, report, meaningful analysis, conclusion, plus reflection.

**What to have open before you hit record (in order, on tabs / windows you can alt-tab between):**

1. **Browser** — `https://github.com/Positivitty/knapsack-ga-vs-dp` (the README renders nicely there)
2. **Editor** — VS Code or whatever, with these files in tabs in this order:
   - `ga/algorithm.py`
   - `ga/operators.py`
   - `dp/knapsack_dp.py`
   - `README.md` (preview pane if possible)
3. **Terminal** — already in `~/Projects/knapsack-ga-vs-dp/` with `.venv` activated. Pre-run `clear` so it starts clean.
4. **Image viewer** — `results/runtime_vs_size.png` and `results/quality_vs_size.png` open and ready

---

## [0:00 — 0:30] Cold open

**[SHOW: Browser tab on GitHub README, scrolled to the top]**

> Hey, I'm Noah Kerr. For our final reflection in algorithms class I built a head-to-head comparison of a **Genetic Algorithm** against **Dynamic Programming** on the **0/1 Knapsack Problem**, written in Python. Code, tests, and the full report are on GitHub at `Positivitty/knapsack-ga-vs-dp`. Over the next ten minutes I'll walk through the problem, both algorithms, the benchmark results, and what I learned.

---

## [0:30 — 2:00] The problem and why it matters

**[SHOW: Scroll down to "The Problem" section of the README]**

> The 0/1 Knapsack Problem is this: you have `n` items, each with a weight and a value, and a knapsack with capacity `W`. Pick a subset of items that maximizes total value without exceeding the capacity. Each item is either fully taken or left behind — no fractions.

> This problem matters because it's a **canonical NP-hard problem**. Every cargo-loading, budget-allocation, resource-scheduling problem you've ever heard of is a knapsack variant under the hood. And NP-hard means there is no known polynomial-time exact algorithm — so it's the perfect arena for comparing an exact approach against an approximate one.

> Specifically, Dynamic Programming solves it in `O(n × W)` — that looks polynomial but it's actually **pseudo-polynomial**. The runtime is linear in the *numeric value* of the capacity, not the number of bits. Double the capacity, double the runtime. That's the crack we're going to drive a Genetic Algorithm into.

---

## [2:00 — 4:00] Algorithm 1 — the Genetic Algorithm

**[SHOW: Editor — `ga/algorithm.py` on screen]**

> The Genetic Algorithm is a population-based metaheuristic. Instead of enumerating the search space, you simulate evolution on a population of candidate solutions. Fit individuals reproduce, offspring mix and mutate, and over generations the population concentrates on high-quality regions.

> Here's the structure. Every candidate solution is a length-`n` bitstring — bit `i` is 1 if item `i` is in the knapsack, 0 if it isn't. I'm using NumPy arrays so the whole population can be evaluated in one vectorized operation.

**[SHOW: Scroll to the main GA loop — `for gen in range(...)`]**

> Each generation does five things:
>
> 1. **Elitism** — copy the top 2 individuals into the next generation unchanged. This guarantees the best-so-far never regresses.
> 2. **Selection** — fill the rest of the parent pool by tournament selection: grab 3 random individuals, the fittest wins a slot. Repeat.
> 3. **Crossover** — pair adjacent parents and mix them. I'm using uniform crossover at probability 0.7. For every bit, flip a coin to decide which parent it comes from.
> 4. **Mutation** — flip every bit independently with probability `1/n`. So on average each child mutates one bit.
> 5. **Evaluate** — score everyone with the fitness function.

**[SHOW: Open `ga/genome.py`, scroll to the `fitness` function]**

> The fitness function is the part that bakes in the problem constraint. If a chromosome is feasible — total weight under capacity — its fitness is the sum of selected values. If it's infeasible, fitness is **zero**. This is called a "death penalty" — overweight chromosomes have no offspring, so the population stays inside the feasible region.

**[SHOW: Open `ga/operators.py` briefly, just to show the three operators side by side]**

> Tournament select, uniform crossover, bit-flip mutate. That's the entire GA in three operators plus a main loop. The whole thing is around 100 lines.

> **Complexity:** `O(G × P × n)` — generations times population times items. With my settings that's `500 × 100 × n`. **Memory:** `O(P × n)` — for n=500 that's 50,000 bits. Tiny.

---

## [4:00 — 5:30] Algorithm 2 — Dynamic Programming

**[SHOW: Editor — `dp/knapsack_dp.py`]**

> Dynamic Programming is the textbook **exact** solver. Build a table `T[i][w]` where each cell holds the best achievable value using only the first `i` items with capacity `w`. The recurrence:

**[SHOW: Highlight the `for i ... for w` loop and the max() line]**

> For each item, for each possible capacity, you decide: take this item and add its value to the best solution that uses the first `i-1` items with the leftover capacity, or don't take it and inherit the previous row's answer. Take whichever is bigger.

> The final answer is `T[n][W]`. Then I backtrack through the table to figure out *which* items were chosen.

> **Complexity:** `O(n × W)` time, `O(n × W)` space. Provably optimal — DP is the ground truth I'm measuring the GA against. But that `W` term is the catch. For my n=500 instances, `W` is around 25,000, which means the table has 12.5 million cells. Push `W` into the millions and DP runs out of memory; the GA wouldn't blink.

---

## [5:30 — 7:00] Live demo — running the code

**[SHOW: Terminal]**

> Let me actually run this.

**[TYPE: `python -m pytest -q`]**

> First, the test suite — 28 tests, including a brute-force check that DP matches the true optimum on small instances and a check that the GA always returns a feasible solution.

**[WAIT for "28 passed". Let it sit on screen for 2 seconds.]**

> All passing. Now the benchmark.

**[TYPE: `python run_benchmark.py --sizes 20,100,500 --trials 3`]**

> I'm running n=20, n=100, and n=500 with 3 trials each — for the video I want a quick demo, but the full sweep in the README does 5 trials at five sizes up to 500.

**[WAIT for it to finish. While it runs, narrate:]**

> The harness generates a deterministic random instance, runs the GA, runs the DP, runs greedy, records value and runtime, repeats. DP gives me the optimum, so I can express the GA's solution as a percentage of optimal — that's the headline quality metric.

**[WHEN it finishes, the summary table will be on screen. Pause.]**

> There are the numbers. Let me pull this up in the README where I have the full sweep with prettier formatting.

---

## [7:00 — 8:30] Results and analysis

**[SHOW: README "Results" section in browser]**

> The full sweep, 5 trials per size. Three things jump out.

**[POINT to the runtime column for n=20]**

> **First — DP is faster on small instances.** At n=20, DP finishes in a millisecond; the GA takes 27 milliseconds because of population overhead. DP is the right tool for tiny problems. No surprise.

**[POINT to the n=200 row, then n=500]**

> **Second — the curves cross.** At n=200, DP and GA are basically tied. At n=500, the GA finishes in 0.31 seconds — DP takes 0.84. The GA is **2.7 times faster than the optimal algorithm** at this scale, and growing.

**[OPEN `runtime_vs_size.png` full screen]**

> Here's the runtime curve on a log scale. DP's slope is steeper because both `n` and `W` are growing. The GA's slope is gentler because it doesn't depend on `W` at all — only on `n` and the hyperparameters.

**[OPEN `quality_vs_size.png`]**

> And here's quality. The GA finds the exact optimum at n=20 and n=50, then drifts down to about 99.4% of optimum at n=500.

**[BACK to the README, scroll to the "Analysis" section]**

> One honest finding worth calling out — **greedy was surprisingly competitive**. At n=500 it landed within 0.02% of the optimum. That's not the GA failing. It's because my random instances draw weights and values uniformly and independently, which makes greedy's value-per-weight heuristic almost ideal. On adversarial instances — correlated weights and values, or degenerate capacity ratios — greedy collapses while the GA holds up. I didn't construct those harder instances for this run, and I think the report is stronger for being upfront about that limitation.

**[POINT to the memory paragraph]**

> The unsung axis is memory. GA holds about 50,000 bits at n=500. DP allocates 12.5 million integer cells. **The GA uses 0.4% of DP's memory** at this scale, and the ratio gets worse for DP as `W` grows.

**[Scroll to "Conclusion"]**

> The conclusion lines up with what I expected going in. **Use DP** when n times W fits in memory and you need the proven optimum. **Use the GA** when W is large and you can tolerate one to two percent off optimum. **Use greedy** when fast and probably fine is the spec.

> The deeper takeaway — and this connects to the rest of the class — is that "best algorithm" isn't a property of a problem in isolation. It's a property of the problem, the instance distribution, the resource budget, and your quality tolerance. DP is correct. GA is flexible. Greedy is fast. The right tool depends on which of those three matters most that day.

---

## [8:30 — 10:00] Reflection

**[SHOW: A clean terminal, or the README scrolled to a neutral section. This is the talking part.]**

> Quick reflection to close out.

> **What I learned in this class** — I came in thinking algorithms were a catalog of tricks you memorize. The real skill the class taught me is **head-to-head comparison**: take two candidates, predict which one wins and why, run them on the same inputs, and confront your prediction with the data. We did this with mergesort versus quicksort, with FIFO versus best-first branch-and-bound on knapsack, and now with GA versus DP. The pattern is the same every time, and that pattern — predict, measure, explain the gap between prediction and reality — is the actual algorithmic literacy.

> **My favorite thing I learned** was the realization that **a Genetic Algorithm is just search wearing a costume**. Once you peel back the biology vocabulary — chromosomes, fitness, mutation — what you're really doing is parallel local search with periodic recombination. That reframing made GAs feel less mystical and more like one more tool in the same toolbox as backtracking, branch-and-bound, and simulated annealing.

> **What I'd do next** — two threads.

> First, I want to revisit my **AviSim** project — that's a real-time aviation sensor processing system in C++ with a FACE-inspired modular architecture. There's a possible job lead at Tinker Air Force Base where AviSim is directly relevant, so polishing that is the top priority before graduation in May.

> Second, I'd like to bolt a Genetic Algorithm onto **EntropyEngine** — a data efficiency analyzer I'm building. Right now it detects inefficiencies in datasets and suggests fixes manually. A GA could explore the space of possible data optimizations and converge on configurations a human wouldn't think to try. That's the natural next application of what I built today.

> That's it. Code is at `github.com/Positivitty/knapsack-ga-vs-dp`. Thanks for watching.

**[FADE / cut]**

---

## Rubric self-check

| Criterion | Where it's covered |
|---|---|
| Running code (25) | Live `pytest` and `run_benchmark.py` execution at 5:30. |
| First algorithm demonstrated (25) | GA walkthrough at 2:00 + GA columns in benchmark output. |
| Second algorithm demonstrated (25) | DP walkthrough at 4:00 + DP columns in benchmark output. |
| Report exists (25) | README on GitHub, shown throughout. |
| Meaningful analysis (25) | Analysis section called out at 7:30, including honest greedy finding + memory discussion. |
| Conclusion supported by report (25) | Conclusion read at 8:00, ties back to runtime/quality/memory data. |
| Video explains results (50) | This whole script. |

---

## Practical recording tips

- **Record at 1080p minimum.** Make sure your editor font is at least 14pt — squinting at code on YouTube is the #1 reason people bounce.
- **Don't speed up the demo.** When `pytest` finishes in 1.7 seconds, just say "all passing" and move on — you don't need to fill the silence.
- **One take is fine.** If you flub a section, pause for two seconds and start the sentence over — you can cut the dead air in your editor. Trying to nail a single perfect take wastes hours.
- **Audio matters more than video.** Use a wired mic if you have one, record in a quiet room, do a 10-second test before committing to the full take.
- **Render and watch it back at 1.5x.** If it makes sense at 1.5x, your pacing is fine at 1x. If it's confusing at 1.5x, you're talking too fast.
