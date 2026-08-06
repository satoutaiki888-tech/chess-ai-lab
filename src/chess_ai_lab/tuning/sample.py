from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PositionSample:
    """
    学習用局面。
    """

    fen: str
    target_cp: int
    source_depth: int