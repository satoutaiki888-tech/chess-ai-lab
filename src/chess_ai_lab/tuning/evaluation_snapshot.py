from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class EvaluationSnapshot:
    """
    評価関数の計算結果。

    total
        重み適用後の最終評価値(cp)

    raw_features
        Feature名 -> 生値

    feature_vector
        FEATURES の順番で並んだ Feature ベクトル
    """

    total: float

    raw_features: dict[str, float]

    feature_vector: np.ndarray