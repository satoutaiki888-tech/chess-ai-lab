from __future__ import annotations

import math

import numpy as np
from chess_ai_lab.evaluation.snapshot import EvaluationSnapshot

TEXEL_SCALE = 400.0
LN10 = math.log(10.0)


def _gradient_coefficient(
    snapshot: EvaluationSnapshot,
    target_cp: float,
) -> float:
    """
    Texel Loss の勾配係数を計算する。
    """

    predicted = 1.0 / (
        1.0 + math.pow(
            10.0,
            -snapshot.total / TEXEL_SCALE,
        )
    )

    target = 1.0 / (
        1.0 + math.pow(
            10.0,
            -target_cp / TEXEL_SCALE,
        )
    )

    dloss_dprob = 2.0 * (
        predicted - target
    )

    dprob_dcp = (
        LN10
        / TEXEL_SCALE
        * predicted
        * (1.0 - predicted)
    )

    return dloss_dprob * dprob_dcp


def compute_gradient_array(
    snapshot: EvaluationSnapshot,
    target_cp: float,
) -> np.ndarray:
    """
    1局面分の勾配を NumPy 配列で返す。
    """

    coefficient = _gradient_coefficient(
        snapshot,
        target_cp,
    )

    return (
        coefficient
        * snapshot.feature_vector
    )


def compute_gradients(
    snapshot: EvaluationSnapshot,
    target_cp: float,
) -> dict[str, float]:
    """
    1局面分のTexel勾配を計算する。
    """

    coefficient = _gradient_coefficient(
        snapshot,
        target_cp,
    )

    gradients = (
        coefficient
        * snapshot.feature_vector
    )

    return {
        name: float(value)
        for (name, _), value in zip(
            snapshot.raw_features.items(),
            gradients,
        )
    }


def accumulate_gradients(
    snapshot: EvaluationSnapshot,
    target_cp: float,
    gradients: dict[str, float],
) -> None:
    """
    1局面分のTexel勾配を gradients に加算する。
    """

    coefficient = _gradient_coefficient(
        snapshot,
        target_cp,
    )

    gradient_vector = (
        coefficient
        * snapshot.feature_vector
    )

    for (name, _), value in zip(
        snapshot.raw_features.items(),
        gradient_vector,
    ):
        gradients[name] += float(value)