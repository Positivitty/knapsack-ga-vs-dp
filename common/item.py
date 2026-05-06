from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    weight: int
    value: int
