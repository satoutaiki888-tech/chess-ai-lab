from __future__ import annotations

from dataclasses import dataclass

import chess
import numpy as np


@dataclass(slots=True, frozen=True)
class TrainingPosition:
    """
    学習時に使用する局面。

    feature_values は将来の学習高速化のために、
    Parquetへ保存された Feature の生値を保持する。

    Feature の順序は evaluation.features.FEATURES に従う。

    現在は None のまま使用し、
    Feature を保存するようになってから利用する。
    """

    board: chess.Board

    target_cp: int

    source_depth: int

    feature_values: np.ndarray | None = None