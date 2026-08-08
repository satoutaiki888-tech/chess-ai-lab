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

    feature_values は Parquet に保存された Feature の生値を保持する。
    旧形式のデータセットとの互換性のため None の場合もある。
    """
    """
    board

    feature_values が存在しないデータセットとの互換性のため保持する。

    feature_values が利用可能な場合は None のことがある。
    """

    board: chess.Board | None

    target_cp: int

    source_depth: int

    feature_values: np.ndarray | None = None