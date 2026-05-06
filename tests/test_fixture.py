from pathlib import Path

from benchmark.fixture import run_sweep, write_csv
from ga.algorithm import GAConfig


def test_run_sweep_returns_three_rows_per_trial(tmp_path):
    rows = run_sweep(
        sizes=[10],
        trials=2,
        ga_config=GAConfig(generations=20, pop_size=20, stagnation_limit=10),
    )
    # 2 trials * 3 algos = 6
    assert len(rows) == 6
    algos = {r.algo for r in rows}
    assert algos == {"ga", "dp", "greedy"}


def test_write_csv_creates_file(tmp_path):
    rows = run_sweep(
        sizes=[8],
        trials=1,
        ga_config=GAConfig(generations=10, pop_size=10, stagnation_limit=5),
    )
    out = tmp_path / "out.csv"
    write_csv(rows, out)
    text = out.read_text()
    assert "algo" in text.splitlines()[0]
    assert len(text.splitlines()) == len(rows) + 1
