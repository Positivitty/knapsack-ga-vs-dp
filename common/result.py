from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AlgorithmResult:
    algo: str
    value: int
    weight: int
    chosen: list[int]
    runtime_s: float
    generations_used: int = 0
    extra: dict = field(default_factory=dict)
