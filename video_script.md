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

> Alright, I'm Noah. For the final in algorithms class we had to pick an algorithm to research, and I went with a Genetic Algorithm. I'm comparing it against Dynamic Programming on the 0/1 Knapsack Problem — both written in Python. Code's all up on GitHub. Over the next ten minutes or so I'll walk through what the problem is, how each algorithm works, what happened when I ran them, and what I got out of the class.

**[press key]**

---

## Section 2 — The Problem

**On screen:** Problem statement — definition + four bullet points.

> Okay so 0/1 Knapsack. You've got a bunch of items, each with a weight and a value, and you've got a knapsack with some weight limit. Pick which items to take so you get the most value without going over the limit. The "0/1" part just means you either take an item or you don't — no taking half a thing.

> This problem matters because it shows up everywhere — anytime you've got a budget and you're picking the best combination of stuff to spend it on, that's a knapsack underneath. Cargo loading, picking projects to fund, packing a backpack, whatever.

> And it's actually a hard problem. It's NP-hard, which basically means nobody's found a fast exact algorithm that works no matter how big you make it. Dynamic Programming gets close — it solves it in `n × W` time, where `W` is the capacity — but that `W` is the catch. If you double the capacity, the algorithm takes twice as long. So as the numbers get big, DP starts struggling, and that's the gap where a Genetic Algorithm can do better.

**[press key]**

---

## Section 3 — GA Main Loop

**On screen:** `ga/algorithm.py` — full file.

> Alright, the Genetic Algorithm. The whole idea is you simulate evolution. You start with a bunch of random guesses at the answer, score how good each one is, let the good ones "reproduce" to make the next generation, mix them up, randomly tweak them, and after enough generations the population converges on something pretty good. That's the concept.

> Up at the top is the config — population of 100, up to 500 generations, plus a few other knobs like crossover and mutation rates. I went with textbook default values on purpose — didn't want to tune them aggressively, because then I'd be making the GA look better than it really is out of the box.

> The main loop does five things every generation. One — copy the top two unchanged into the next generation, so we never lose ground. That's called elitism. Two — pick parents using tournament selection. Three — mix the parents to make children. Four — randomly flip some bits in the kids. Five — score the new population.

> And if nothing's gotten better for 100 generations straight, we just stop early. The whole algorithm is about 90 lines.

**[press key]**

---

## Section 4 — GA Operators

**On screen:** `ga/operators.py` — three functions.

> Three operators, three functions.

> Tournament selection grabs three random candidates and picks whichever one has the highest fitness. That's it. Do it again to get the next parent. Simple, and it works well even when the fitness numbers are weird.

> Uniform crossover takes two parents and makes two kids by going bit by bit and flipping a coin — that bit comes from parent A or parent B. We only do this 70% of the time; the other 30% the kids are just copies. The reason I'm using uniform instead of single-point crossover is that the order of items in the genome doesn't actually mean anything — item 5 isn't related to item 6 — so mixing them up randomly works better than slicing them.

> Bit-flip mutation flips each bit with some small probability. I'm using one over `n`, so on average each kid mutates exactly one bit.

> All three of these run on the whole population at once using NumPy, so it's fast.

**[press key]**

---

## Section 5 — GA Fitness

**On screen:** `ga/genome.py` — fitness, decode, packing helpers.

> The fitness function is where the actual rules of knapsack get baked in. For each candidate, you add up its total weight and total value. If the weight is under the capacity, fitness is the total value — higher's better. If the weight goes over, fitness is just zero.

> This is sometimes called a "death penalty." The idea is if a candidate is overweight, its fitness is zero, so it has zero chance of getting picked as a parent, so it doesn't reproduce — and the population just kind of naturally stays inside the legal range. No extra logic to repair bad solutions, no special handling. Simplest thing that works.

> The matrix multiplications you see — population times weights, population times values — those calculate the totals for every candidate in the population at once, which is way faster than doing it one at a time.

**[press key]**

---

## Section 6 — DP

**On screen:** `dp/knapsack_dp.py` — full file.

> Okay this is the other algorithm — Dynamic Programming. The textbook way to solve knapsack exactly.

> You build a table. Each cell answers a smaller version of the question — "what's the best value I can get using just the first `i` items with capacity `w`?" The recurrence in the inner loop is basically: for each item, you decide to either take it or skip it, and you take whichever decision leads to a higher value. That's the whole thing.

> The actual answer ends up in the bottom-right cell of the table. The little loop at the end walks back up through the table to figure out which items actually got picked.

> Time and space are both `n × W`. DP is provably correct — it gives you the real optimum every time. That's what I'm using as ground truth to score the GA. But that `W` in the complexity is what bites you. For my n=500 test cases, the capacity is around 25,000, so the table is 12.5 million cells. If you push capacity into the millions, DP runs out of memory. The GA wouldn't even notice.

**[press key]**

---

## Section 7 — Test suite

**On screen:** `pytest -v` running 28 tests.

> Real quick — the test suite. 28 tests.

> The most important ones check that DP actually returns the right answer. I wrote a brute-force solver that just tries every possible combination of items, and I run that against DP on small instances to make sure they match. The GA gets checked to make sure it never returns an overweight solution and never claims to beat DP — since DP's the true optimum, that should be impossible.

> Everything passes. So when you see numbers in the next section, you can trust them.

**[press key]**

---

## Section 8 — Benchmark sweep

**On screen:** `python run_benchmark.py` running. Takes ~25–30 seconds. Talk through it.

> And here's the actual benchmark. Five different sizes, five trials at each size, all three algorithms run on every instance.

> Each trial generates a random knapsack from a fixed seed — so it's reproducible — runs the GA, runs DP, runs greedy, and records the value and how long it took. Since DP gives the optimum, I can score the GA as a percentage. If the GA gets 99% of what DP got, that's 99% quality.

> While this is running — what I predicted going in was that DP would win on small problems because it doesn't have to mess around with populations of candidates, but the GA would catch up and pass DP at larger sizes, because DP's runtime depends on capacity and the GA's basically doesn't.

> The summary table at the end is sorted by size and algorithm. Look at the n=20 row — DP and the GA both find the exact right answer, but DP does it in a millisecond and the GA takes about 27. DP wins on small stuff. No surprise.

> Now look at the n=500 row. The GA finishes in 0.31 seconds. DP takes 0.84. So the GA is more than twice as fast as the optimal algorithm at this size, and it's still getting 99.4% of the optimal value.

> Greedy — the third row in each group — is basically free everywhere. I'll come back to that.

**[press key]**

---

## Section 9 — Results + reflection (outro)

**On screen:** Outro card with headline numbers and file paths.

> Alright, so the takeaway.

> On runtime — DP wins on small stuff, the GA catches up around n=200, and from n=500 on the gap keeps growing. The runtime plot shows it pretty clearly. DP curves up sharper because both `n` and `W` are growing. The GA stays flatter because it doesn't care about `W` at all.

> On quality — the GA gets the exact right answer at n=20 and n=50, then drifts down to about 99.4% of optimum by n=500. That's not the GA breaking — it's that the search space gets bigger and a fixed budget of 100 candidates over 500 generations can only cover so much ground.

> One thing I want to be straight about — greedy was way better than I thought it would be. At n=500 it's within 0.02% of optimal, beating my GA on quality. That's not greedy being amazing or the GA being bad. It's that the way I generated the test instances — weights and values both random and uniform — happens to be the easy case for greedy. If I'd built nastier instances where weights and values are correlated, or the capacity ratio is weird, greedy falls apart and the GA holds up. I didn't build those harder instances for this run, but I figure being upfront about that limitation makes the report better, not worse.

> Memory is the part nobody talks about but it's the most lopsided result. At n=500, the GA holds about 50,000 bits. DP allocates 12.5 million integer cells. So the GA is using less than half a percent of DP's memory at this size — and the gap only gets worse for DP as capacity grows.

> Bottom line — use DP when `n × W` fits in memory and you need the exact optimum. Use the GA when capacity is huge and you can live with being one or two percent off. Use greedy when you just need an answer fast and "probably fine" is good enough.

> Reflection — coming into this class I sort of thought algorithms were a list of tricks you memorize. The real thing the class actually taught me is head-to-head comparison. Take two algorithms, predict which one wins and why, run them on the same inputs, then look at why your prediction was right or wrong. We did this with mergesort versus quicksort, with two flavors of branch-and-bound on knapsack, and now with this. It's the same pattern every time, and that pattern — predict, measure, explain — is the actual skill.

> My favorite thing I learned was realizing a Genetic Algorithm is basically just search with a costume on. Once you strip out the biology words — chromosomes, fitness, mutation — what's actually happening is parallel local search. That made GAs feel a lot less mysterious. They're just one more tool in the same toolbox as backtracking or branch-and-bound.

> What I want to do next — couple things. First, polish my AviSim project. It's a real-time aviation sensor processing system in C++. There's a possible job lead at Tinker Air Force Base where it's directly relevant, so that's the top priority before I graduate in May. Second, I want to throw a Genetic Algorithm at EntropyEngine — that's a data efficiency analyzer I've been building. Right now it suggests fixes manually; a GA could explore optimizations a person wouldn't think to try. Natural follow-up to what I built today.

> Code's at github dot com slash Positivitty slash knapsack dash GA dash vs dash DP. Thanks for watching.

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
- **Read it like you're explaining it to a friend, not reciting an essay.** If a sentence feels stiff in your mouth, change a word. The script is a starting point, not a teleprompter.
