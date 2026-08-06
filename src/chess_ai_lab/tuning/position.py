from __future__ import annotations

from dataclasses import dataclass

import chess


@dataclass(slots=True, frozen=True)
class TrainingPosition:
    """
    学習時に使用する局面。
    """

    board: chess.Board
    target_cp: int
    source_depth: int