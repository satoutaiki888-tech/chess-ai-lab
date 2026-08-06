from __future__ import annotations

import math

from chess_ai_lab.tuning.evaluation_snapshot import EvaluationSnapshot

TEXEL_SCALE = 400.0
LN10 = math.log(10.0)


def compute_gradients(
    snapshot: EvaluationSnapshot,
    target_cp: float,
) -> dict[str, float]:
    """
    1局面分のTexel勾配を計算する。

    Returns
    -------
    dict[feature_name, gradient]
    """

    predicted = 1.0 / (
        1.0 + math.pow(10.0, -snapshot.total / TEXEL_SCALE)
    )

    target = 1.0 / (
        1.0 + math.pow(10.0, -target_cp / TEXEL_SCALE)
    )

    dloss_dprob = 2.0 * (predicted - target)

    dprob_dcp = (
        LN10
        / TEXEL_SCALE
        * predicted
        * (1.0 - predicted)
    )

    coefficient = dloss_dprob * dprob_dcp

    gradients = {}

    for name, raw in snapshot.raw_features.items():
        gradients[name] = coefficient * raw

    return gradients

def accumulate_gradients(
    snapshot: EvaluationSnapshot,
    target_cp: float,
    gradients: dict[str, float],
) -> None:
    """
    1局面分のTexel勾配を gradients に加算する。

    Parameters
    ----------
    snapshot
        Evaluator.snapshot() の結果

    target_cp
        Stockfish評価値

    gradients
        Feature名 -> 勾配合計
    """

    predicted = 1.0 / (
        1.0 + math.pow(10.0, -snapshot.total / TEXEL_SCALE)
    )

    target = 1.0 / (
        1.0 + math.pow(10.0, -target_cp / TEXEL_SCALE)
    )

    dloss_dprob = 2.0 * (predicted - target)

    dprob_dcp = (
        LN10
        / TEXEL_SCALE
        * predicted
        * (1.0 - predicted)
    )

    coefficient = dloss_dprob * dprob_dcp

    for name, raw in snapshot.raw_features.items():
        gradients[name] += coefficient * raw