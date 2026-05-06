# Video Script — Knapsack: GA vs DP

**Setup:** Two windows. Left/main = a terminal running `./demo.sh`. Right/second = this file, scrolled along as you go. No tab switching. The demo pauses after every section — press any key to advance when you're ready.

**Recording:**
1. Open a fresh terminal in `~/Projects/knapsack-ga-vs-dp/`
2. Run `source .venv/bin/activate`
3. Maximize the terminal, bump the font to 16pt+ (the readers of your video will thank you)
4. Hit record
5. Run `./demo.sh`
6. Read the script section by section. Press any key when you're ready to move on.

Target length: ~10 minutes. Anything from 8 to 12 is fine.

---

## Section 1 — Banner (cold open)

**On screen:** ASCII banner with project title.

> Hey, I'm Noah Kerr. For our final reflection in algorithms class I built a head-to-head comparison of a **Genetic Algorithm** against **Dynamic Programming** on the **0/1 Knapsack Problem**, in Python. Code, tests, and the full report are on GitHub at `Positivitty/knapsack-ga-vs-dp`. Over the next ten minutes I'll walk through the problem, both algorithms, the benchmark results, and what I took away from the class.

**[press key]**

---

## Section 2 — The Problem

**On screen:** Problem statement — definition + four bullet points.

> The 0/1 Knapsack Problem is this: you have `n` items, each with a weight and a value, and a knapsack with capacity `W`. Pick a subset of items that maximizes total value without exceeding the capacity. Each item is either fully taken or left behind — no fractions.

> This problem matters because it's a **canonical NP-hard problem**. Every cargo-loading, budget-allocation, resource-scheduling problem you've ever heard of is some variant of knapsack under the hood. NP-hard means there is no known polynomial-time exact algorithm, so it's the perfect arena for comparing an exact approach against an approximate one.

> Specifically, Dynamic Programming solves this in `O(n × W)` — that looks polynomial but it's actually **pseudo-polynomial**. Runtime is linear in the *numeric value* of the capacity, not the number of bits. Double the capacity, double the runtime. That's the crack we're going to drive a Genetic Algorithm into.

**[press key]**

---

## Section 3 — GA Main Loop

**On screen:** `ga/algorithm.py` — full file.

> This is my Genetic Algorithm. The Genetic Algorithm is a population-based metaheuristic — instead of enumerating the search space, you simulate evolution on a population of candidate solutions. Fit individuals reproduce, offspring mix and mutate, and over generations the population concentrates on high-quality regions of the search space.

> Up at the top is the configuration: population of 100, up to 500 generations, tournament size 3, crossover probability 0.7, mutation rate of 1 over n, elitism of 2, and an early stop if the global best hasn't improved in 100 generations. These are textbook starting values — I deliberately didn't hand-tune them, so the comparison stays fair.

> Down in the main loop, every generation does five things:
>
> One — **elitism**: the top 2 individuals get copied unchanged into the next generation. This guarantees the best-so-far never regresses.
>
> Two — **selection**: fill the rest of the parent pool by tournament selection.
>
> Three — **crossover**: mix adjacent parents to make children.
>
> Four — **mutation**: randomly flip bits in the children.
>
> Five — **evaluate**: score the new population.

> If the global best improves, reset the stagnation counter. Otherwise increment it. When it hits the limit, break out early. That's the whole GA in about 90 lines.

**[press key]**

---

## Section 4 — GA Operators

**On screen:** `ga/operators.py` — three functions.

> Three operators, three functions.

> **Tournament selection** grabs `k` random individuals from the population — I'm using k=3 — and the fittest one wins a parent slot. It's robust to weird fitness distributions and trivial to implement.

> **Uniform crossover** pairs adjacent parents. With probability 0.7 we mix them: for every bit, flip a coin to decide which parent it comes from. Otherwise the children are exact copies. Uniform crossover mixes more aggressively than single-point crossover, which matters here because nearby bits in our genome aren't correlated — item ordering in the input is arbitrary.

> **Bit-flip mutation** flips every bit independently with probability `p`. I'm using `p = 1/n`, so on average each child mutates exactly one bit.

> All three are vectorized over the entire population using NumPy, so a generation costs about the same regardless of population size.

**[press key]**

---

## Section 5 — GA Fitness

**On screen:** `ga/genome.py` — fitness, decode, packing helpers.

> The fitness function is the part that bakes in the problem constraint. For each chromosome we compute total weight and total value. If the chromosome is feasible — total weight is at most the capacity — its fitness is the sum of selected values. If it's infeasible, fitness is **zero**.

> This is called a "death penalty." Overweight chromosomes have no offspring, so the population stays inside the feasible region without any explicit repair logic. It's the simplest possible constraint handling, and I argue for it in the report — repair operators are more complex and harder to defend as fair when comparing to DP.

> Note the matrix multiplications — `population @ weights` computes total weight for every individual in one shot. The whole fitness function is three lines of NumPy.

**[press key]**

---

## Section 6 — DP

**On screen:** `dp/knapsack_dp.py` — full file.

> This is the **exact** solver — Dynamic Programming. The textbook approach.

> Build a table where each cell `T[i][w]` holds the best achievable value using only the first `i` items with capacity `w`. The recurrence in the inner loop says: for the i-th item, you decide — take it and inherit `T[i-1][w - weight_i] + value_i`, or don't take it and inherit `T[i-1][w]`. Take whichever is bigger.

> The optimum is `T[n][W]`, the bottom-right cell. The backtracking loop at the end walks the table backwards to figure out *which* items were chosen.

> **Complexity:** `O(n × W)` time and `O(n × W)` space. Provably optimal — DP is the ground truth I'm measuring the GA against. But that `W` term is the catch. For my n=500 instances, capacity is around 25,000, so the table has 12.5 million cells. Push capacity into the millions and DP runs out of memory long before the GA would even feel it.

**[press key]**

---

## Section 7 — Test suite

**On screen:** `pytest -v` running 28 tests.

> Real quick — the test suite. 28 tests covering correctness of both algorithms.

> The most important ones are in `test_correctness.py` and `test_dp.py` — DP's output is checked against a brute-force solver on small instances, which proves the DP code is finding the actual optimum. The GA is checked to always return a feasible solution and to never exceed DP's optimum. The operator tests pin down edge-case behavior at probability zero and probability one.

> All passing. So when you see numbers in the next section, you can trust them.

**[press key]**

---

## Section 8 — Benchmark sweep

**On screen:** `python run_benchmark.py` running. Takes ~25–30 seconds. Talk through it.

> And here's the actual benchmark — five sizes, five trials each, all three algorithms on every instance.

> The harness generates a deterministic random knapsack instance from a seed, runs the GA, runs DP, runs greedy, records value and runtime, then repeats. Because DP gives the optimum, I can express the GA's solution as a percentage of optimal — that's the headline quality metric.

> While it runs — a quick word on what to expect. I predicted DP would win on small `n` because exact algorithms have no per-individual overhead, and the GA would overtake DP at large `n` because GA scales linearly in `n` while DP scales in `n × W`, and `W` here grows with `n`.

> Pause for whatever the benchmark is finishing up. The summary table at the end is sorted by size and algorithm. Each row shows mean value, mean quality as a percent of optimum, mean runtime in seconds, and for the GA, the mean number of generations actually used before early-stop kicked in.

> Look at the n=20 row — both DP and GA find the exact optimum, but DP does it in a millisecond while the GA takes about 27. DP wins on tiny problems, no surprise.

> Now look at n=500. The GA finishes in 0.31 seconds. DP takes 0.84. **The GA is 2.7 times faster than the optimal algorithm at this scale**, and it's still delivering 99.4% of optimal value.

> Greedy — the third row in each group — is essentially free everywhere. I'll come back to that in a second.

**[press key]**

---

## Section 9 — Results + reflection (outro)

**On screen:** Outro card with headline numbers and file paths.

> So here's the full story.

> **Runtime** — DP wins on small instances, the GA crosses over between n=200 and n=500, and from n=500 onward the gap widens. The runtime plot makes this obvious — DP has a steeper slope on the log scale because both `n` and `W` are growing, while the GA's slope is gentler because it doesn't depend on `W` at all.

> **Quality** — the GA finds the exact optimum at n=20 and n=50, then drifts down to about 99.4% of optimum at n=500. That's not the GA failing; it's exactly what you'd expect from a fixed hyperparameter budget against a growing search space.

> **The honest finding I want to call out** — greedy was surprisingly competitive on these instances. It got within 0.02% of optimum at n=500, beating my GA on quality. That's not a flaw in the GA — it's a property of how I generated the instances. Weights and values were independently uniform, which makes the value-per-weight heuristic almost ideal. On adversarial instances — correlated weights and values, or pathological capacity ratios — greedy can be arbitrarily bad while the GA holds up. I didn't build those harder instances for this run, but I think the report is stronger for being upfront about it.

> **Memory** is the unsung axis. At n=500, the GA holds about 50,000 bits. DP allocates 12.5 million integer cells. **The GA uses about 0.4% of DP's memory** at this scale, and the ratio gets dramatically worse for DP as capacity grows.

> **The conclusion**: use DP when `n × W` fits comfortably in memory and you need the proven optimum. Use the GA when `W` is large and you can tolerate one to two percent off optimum. Use greedy when "fast and probably fine" is the spec.

> **Reflection** — I came into this class thinking algorithms were a catalog of tricks you memorize. The real skill the class taught me is **head-to-head comparison**: take two candidates, predict which one wins and why, run them on the same inputs, then confront your prediction with the data. We did this with mergesort versus quicksort, with FIFO versus best-first branch-and-bound on knapsack, and now with GA versus DP. The pattern is the same every time — predict, measure, explain the gap — and that pattern is the actual algorithmic literacy.

> My **favorite thing I learned** was the realization that **a Genetic Algorithm is just search wearing a costume**. Once you peel back the biology vocabulary — chromosomes, fitness, mutation — what's actually happening is parallel local search with periodic recombination. That reframing made GAs feel less mystical and more like one more tool in the same toolbox as backtracking, branch-and-bound, and simulated annealing.

> **What I'd do next** — two threads. First, polish my **AviSim** project — that's a real-time aviation sensor processing system in C++ with a FACE-inspired modular architecture. There's a possible job opportunity at Tinker Air Force Base where AviSim is directly relevant, so that's the top priority before I graduate in May. Second, I'd like to bolt a Genetic Algorithm onto **EntropyEngine** — a data efficiency analyzer I'm building. Right now it detects inefficiencies and suggests fixes by hand. A GA could explore the space of possible data optimizations and converge on configurations a human wouldn't think to try. That's the natural next application of what I built today.

> Code's at `github.com/Positivitty/knapsack-ga-vs-dp`. Thanks for watching.

**[press key — clear screen — stop recording]**

---

## Cheat sheet

| # | What's on screen | Roughly how long |
|---|---|---|
| 1 | Banner | 0:30 |
| 2 | Problem statement | 1:00 |
| 3 | `ga/algorithm.py` | 1:30 |
| 4 | `ga/operators.py` | 0:45 |
| 5 | `ga/genome.py` | 0:45 |
| 6 | `dp/knapsack_dp.py` | 1:00 |
| 7 | pytest output | 0:30 |
| 8 | benchmark running | 1:30 (track it — sweep takes ~25s) |
| 9 | outro card + reflection | 2:30 |

That sums to ~10 minutes. If you blow past that on any section, just trim the next one.

## Rubric self-check

| Criterion | Where it's covered |
|---|---|
| Running code (25) | Sections 7 & 8 — pytest then live benchmark |
| First algorithm (GA) demonstrated (25) | Sections 3, 4, 5 + GA columns in benchmark |
| Second algorithm (DP) demonstrated (25) | Section 6 + DP columns in benchmark |
| Report exists (25) | README on GitHub, called out in section 1 and section 9 |
| Meaningful analysis (25) | Section 9 — runtime/quality/memory + honest greedy finding |
| Conclusion supported (25) | Section 9 — three-way conclusion ties back to the data |
| Video explains results (50) | The whole script |

## Recording tips

- **One take.** If you flub a sentence, pause two seconds and start the sentence over. Cut dead air in your editor afterward — way faster than retakes.
- **Audio matters more than video.** Quiet room, wired mic if you have one. Do a 30-second test before committing.
- **Don't race the demo.** The whole point of pause-on-keystroke is that you control pacing. If you need 20 seconds longer on a section, take it.
- **Don't speed up the benchmark.** When pytest finishes in 1.7 seconds, just say "all passing" and hit the key. You don't need to fill silence.
