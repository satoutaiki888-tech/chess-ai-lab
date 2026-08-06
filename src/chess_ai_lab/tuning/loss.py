from __future__ import annotations

import math


TEXEL_SCALE = 400.0


def cp_to_probability(cp: float) -> float:
    """
    評価値(cp)を勝率へ変換する。

    P = 1 / (1 + 10^(-cp / 400))
    """

    return 1.0 / (1.0 + math.pow(10.0, -cp / TEXEL_SCALE))


def texel_loss(
    predicted_cp: float,
    target_cp: float,
) -> float:
    """
    Texel Loss (二乗誤差)。

    target_cp は Stockfish の評価値。
    """

    predicted = cp_to_probability(predicted_cp)
    target = cp_to_probability(target_cp)

    return (predicted - target) ** 2