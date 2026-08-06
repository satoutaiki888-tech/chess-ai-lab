from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EvaluationSnapshot:
    """
    評価関数の計算結果。

    total:
        重み適用後の最終評価値(cp)

    raw_features:
        Feature名 -> 生値
    """

    total: float
    raw_features: dict[str, float]